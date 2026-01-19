require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
app.use(bodyParser.json());

// Configuration from environment variables
const WHATSAPP_TOKEN = process.env.WHATSAPP_TOKEN;
const PHONE_NUMBER_ID = process.env.PHONE_NUMBER_ID;
const WEBHOOK_VERIFY_TOKEN = process.env.WEBHOOK_VERIFY_TOKEN || 'verify123';
const PORT = process.env.PORT || 3000;

// Bot Configuration
let MESSAGE_LIMIT = parseInt(process.env.MESSAGE_LIMIT) || 5;
const ADMINS = process.env.ADMIN_NUMBERS ? process.env.ADMIN_NUMBERS.split(',').map(n => n.trim()) : [];

// In-memory storage (use database in production)
let dailyCount = {}; // { phoneNumber: count }
let bannedUsers = []; // [phoneNumber1, phoneNumber2, ...]
let groupInfo = {}; // Store group information

// Reset daily counts at midnight
setInterval(() => {
  const now = new Date();
  if (now.getHours() === 0 && now.getMinutes() === 0) {
    console.log('Resetting daily message counts...');
    dailyCount = {};
  }
}, 60000); // Check every minute

// Function to send WhatsApp message
async function sendMessage(to, text) {
  try {
    await axios.post(
      `https://graph.facebook.com/v20.0/${PHONE_NUMBER_ID}/messages`,
      {
        messaging_product: 'whatsapp',
        to: to,
        text: { body: text }
      },
      {
        headers: {
          Authorization: `Bearer ${WHATSAPP_TOKEN}`,
          'Content-Type': 'application/json'
        }
      }
    );
    console.log(`Message sent to ${to}: ${text.substring(0, 50)}...`);
  } catch (error) {
    console.error('Error sending message:', error.response?.data || error.message);
  }
}

// Function to remove user from group
async function removeUserFromGroup(groupId, phoneNumber) {
  try {
    await axios.post(
      `https://graph.facebook.com/v20.0/${groupId}/participants`,
      {
        messaging_product: 'whatsapp',
        action: 'remove',
        participant: phoneNumber
      },
      {
        headers: {
          Authorization: `Bearer ${WHATSAPP_TOKEN}`,
          'Content-Type': 'application/json'
        }
      }
    );
    console.log(`Removed ${phoneNumber} from group ${groupId}`);
  } catch (error) {
    console.error('Error removing user from group:', error.response?.data || error.message);
  }
}

// Webhook endpoint - Receive messages
app.post('/webhook', async (req, res) => {
  try {
    // Debug logging to verify delivery and payload shape
    try {
      console.log('Incoming webhook payload:', JSON.stringify(req.body));
    } catch (e) {
      console.log('Incoming webhook payload (non-JSON printable)');
    }

    const entry = req.body.entry?.[0];
    const changes = entry?.changes?.[0];
    const value = changes?.value;
    const messageData = value?.messages?.[0];

    if (!messageData) {
      return res.sendStatus(200);
    }

    const from = messageData.from; // User phone number
    // Support multiple message types: text, button, interactive
    let text = messageData.text?.body;
    if (!text && messageData.type === 'button') {
      text = messageData.button?.text;
    }
    if (!text && messageData.type === 'interactive') {
      const interactive = messageData.interactive;
      text = interactive?.button_reply?.title || interactive?.list_reply?.title || interactive?.nfm_reply?.response_json || interactive?.caption;
    }

    const groupId = messageData.context?.group_id || undefined;

    // Store group info (best effort)
    if (value?.metadata?.display_phone_number && value?.metadata?.phone_number_id) {
      const pnid = value.metadata.phone_number_id;
      if (!groupInfo[pnid]) {
        groupInfo[pnid] = { id: pnid, name: value.metadata.display_phone_number };
      }
    }

    console.log(`Received message from ${from}: ${text ?? '[non-text message]'}`);

    // Check if user is banned
    if (bannedUsers.includes(from)) {
      console.log(`Ignored message from banned user: ${from}`);
      return res.sendStatus(200);
    }

    // Check if message is from admin
    const isAdmin = ADMINS.includes(from);

    // Handle admin commands
    if (isAdmin && text?.startsWith('/')) {
      await handleAdminCommand(from, text, groupId);
      return res.sendStatus(200);
    }

    // Increase message count for user
    dailyCount[from] = (dailyCount[from] || 0) + 1;
    console.log(`User ${from} sent message number ${dailyCount[from]}/${MESSAGE_LIMIT}`);

    // Check if user exceeded limit
    if (dailyCount[from] > MESSAGE_LIMIT) {
      await sendMessage(
        from,
        `⚠️ You have reached today's limit of ${MESSAGE_LIMIT} messages. You will be removed from the group.`
      );

      // Remove user from group if groupId is available
      if (groupId) {
        await removeUserFromGroup(groupId, from);
      }

      return res.sendStatus(200);
    }

    // Warn user when approaching limit
    if (dailyCount[from] === MESSAGE_LIMIT) {
      await sendMessage(
        from,
        `⚠️ Warning: You have sent ${MESSAGE_LIMIT} messages today. This is your limit. Next message will result in removal.`
      );
    } else if (dailyCount[from] === MESSAGE_LIMIT - 1) {
      await sendMessage(
        from,
        `ℹ️ You have sent ${dailyCount[from]} messages. You have ${MESSAGE_LIMIT - dailyCount[from]} message remaining today.`
      );
    }

    res.sendStatus(200);
  } catch (error) {
    console.error('Error in webhook:', error);
    res.sendStatus(500);
  }
});

// Handle admin commands
async function handleAdminCommand(from, text, groupId) {
  const parts = text.trim().split(/\s+/);
  const command = parts[0].toLowerCase();
  const args = parts.slice(1);

  console.log(`Admin command received: ${command} from ${from}`);

  switch (command) {
    case '/limit':
      if (args[0] && !isNaN(parseInt(args[0])) && parseInt(args[0]) > 0) {
        MESSAGE_LIMIT = parseInt(args[0]);
        await sendMessage(from, `✅ Daily message limit updated to ${MESSAGE_LIMIT}.`);
      } else {
        await sendMessage(from, '❌ Invalid limit. Usage: /limit <number>');
      }
      break;

    case '/reset':
      dailyCount = {};
      await sendMessage(from, '✅ All message counts have been reset.');
      break;

    case '/stats':
      let stats = '📊 *Message Statistics*\n\n';
      if (Object.keys(dailyCount).length === 0) {
        stats += 'No messages today.';
      } else {
        for (const user in dailyCount) {
          const status = dailyCount[user] >= MESSAGE_LIMIT ? '🔴' : '🟢';
          stats += `${status} ${user}: ${dailyCount[user]}/${MESSAGE_LIMIT}\n`;
        }
      }
      await sendMessage(from, stats);
      break;

    case '/ban':
      if (args[0]) {
        const userToBan = args[0];
        if (!bannedUsers.includes(userToBan)) {
          bannedUsers.push(userToBan);
          await sendMessage(from, `✅ ${userToBan} has been banned.`);
          
          // Optionally remove from group
          if (groupId) {
            await removeUserFromGroup(groupId, userToBan);
          }
        } else {
          await sendMessage(from, `ℹ️ ${userToBan} is already banned.`);
        }
      } else {
        await sendMessage(from, '❌ Usage: /ban <phone_number>');
      }
      break;

    case '/unban':
      if (args[0]) {
        const userToUnban = args[0];
        const index = bannedUsers.indexOf(userToUnban);
        if (index > -1) {
          bannedUsers.splice(index, 1);
          await sendMessage(from, `✅ ${userToUnban} has been unbanned.`);
        } else {
          await sendMessage(from, `ℹ️ ${userToUnban} is not banned.`);
        }
      } else {
        await sendMessage(from, '❌ Usage: /unban <phone_number>');
      }
      break;

    case '/help':
      const helpText = `
📋 *Admin Commands*

/limit <number> - Change daily message limit
/reset - Reset all message counts
/stats - Show message statistics
/ban <number> - Ban a user
/unban <number> - Unban a user
/help - Show this help message

Current limit: ${MESSAGE_LIMIT} messages/day
      `.trim();
      await sendMessage(from, helpText);
      break;

    default:
      await sendMessage(from, '❌ Unknown command. Type /help for available commands.');
  }
}

// Webhook verification endpoint
app.get('/webhook', (req, res) => {
  const mode = req.query['hub.mode'];
  const token = req.query['hub.verify_token'];
  const challenge = req.query['hub.challenge'];

  if (mode === 'subscribe' && token === WEBHOOK_VERIFY_TOKEN) {
    console.log('Webhook verified successfully!');
    res.status(200).send(challenge);
  } else {
    console.error('Webhook verification failed!');
    res.sendStatus(403);
  }
});

// Dashboard endpoint
app.get('/dashboard', (req, res) => {
  let html = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="refresh" content="30">
  <title>WhatsApp Bot Dashboard</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 20px;
      min-height: 100vh;
    }
    .container {
      max-width: 1200px;
      margin: 0 auto;
      background: white;
      border-radius: 10px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.2);
      padding: 30px;
    }
    h1 {
      color: #333;
      margin-bottom: 10px;
      font-size: 2em;
    }
    .subtitle {
      color: #666;
      margin-bottom: 30px;
      font-size: 0.9em;
    }
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      margin-bottom: 30px;
    }
    .stat-card {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 20px;
      border-radius: 8px;
      text-align: center;
    }
    .stat-value {
      font-size: 2.5em;
      font-weight: bold;
      margin-bottom: 5px;
    }
    .stat-label {
      font-size: 0.9em;
      opacity: 0.9;
    }
    h2 {
      color: #333;
      margin: 30px 0 15px 0;
      font-size: 1.5em;
      border-bottom: 2px solid #667eea;
      padding-bottom: 10px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 30px;
    }
    th, td {
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }
    th {
      background-color: #667eea;
      color: white;
      font-weight: 600;
    }
    tr:hover {
      background-color: #f5f5f5;
    }
    .status-ok {
      color: #10b981;
      font-weight: bold;
    }
    .status-warning {
      color: #f59e0b;
      font-weight: bold;
    }
    .status-limit {
      color: #ef4444;
      font-weight: bold;
    }
    .badge {
      display: inline-block;
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 0.85em;
      font-weight: 600;
    }
    .badge-success { background: #d1fae5; color: #065f46; }
    .badge-warning { background: #fed7aa; color: #92400e; }
    .badge-danger { background: #fee2e2; color: #991b1b; }
    ul {
      list-style: none;
      padding: 0;
    }
    li {
      padding: 10px;
      margin: 5px 0;
      background: #f9fafb;
      border-radius: 5px;
      border-left: 3px solid #ef4444;
    }
    .info-box {
      background: #eff6ff;
      border-left: 4px solid #3b82f6;
      padding: 15px;
      border-radius: 5px;
      margin-top: 20px;
    }
    .timestamp {
      text-align: center;
      color: #999;
      margin-top: 20px;
      font-size: 0.85em;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>📱 WhatsApp Bot Dashboard</h1>
    <p class="subtitle">Real-time monitoring and statistics • Auto-refresh every 30 seconds</p>
    
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">${Object.keys(dailyCount).length}</div>
        <div class="stat-label">Active Users Today</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">${MESSAGE_LIMIT}</div>
        <div class="stat-label">Daily Message Limit</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">${Object.values(dailyCount).reduce((a, b) => a + b, 0)}</div>
        <div class="stat-label">Total Messages Today</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">${bannedUsers.length}</div>
        <div class="stat-label">Banned Users</div>
      </div>
    </div>

    <h2>📊 Daily Message Counts</h2>
  `;

  if (Object.keys(dailyCount).length === 0) {
    html += '<p style="padding: 20px; text-align: center; color: #999;">No messages received today yet.</p>';
  } else {
    html += `
    <table>
      <thead>
        <tr>
          <th>User Phone Number</th>
          <th>Messages Sent</th>
          <th>Progress</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
    `;

    for (const user in dailyCount) {
      const count = dailyCount[user];
      const percentage = Math.min((count / MESSAGE_LIMIT) * 100, 100);
      let statusClass, statusText, badgeClass;

      if (count > MESSAGE_LIMIT) {
        statusClass = 'status-limit';
        statusText = '🔴 Limit Exceeded';
        badgeClass = 'badge-danger';
      } else if (count === MESSAGE_LIMIT) {
        statusClass = 'status-warning';
        statusText = '⚠️ At Limit';
        badgeClass = 'badge-warning';
      } else if (count >= MESSAGE_LIMIT * 0.8) {
        statusClass = 'status-warning';
        statusText = '⚠️ Near Limit';
        badgeClass = 'badge-warning';
      } else {
        statusClass = 'status-ok';
        statusText = '✅ OK';
        badgeClass = 'badge-success';
      }

      html += `
        <tr>
          <td><code>${user}</code></td>
          <td><strong>${count}</strong> / ${MESSAGE_LIMIT}</td>
          <td>
            <div style="background: #e5e7eb; border-radius: 10px; height: 20px; overflow: hidden;">
              <div style="background: ${percentage > 100 ? '#ef4444' : percentage >= 80 ? '#f59e0b' : '#10b981'}; height: 100%; width: ${Math.min(percentage, 100)}%; transition: width 0.3s;"></div>
            </div>
          </td>
          <td><span class="badge ${badgeClass}">${statusText}</span></td>
        </tr>
      `;
    }

    html += '</tbody></table>';
  }

  html += '<h2>🚫 Banned Users</h2>';

  if (bannedUsers.length === 0) {
    html += '<p style="padding: 20px; text-align: center; color: #999;">No banned users.</p>';
  } else {
    html += '<ul>';
    bannedUsers.forEach(user => {
      html += `<li><code>${user}</code></li>`;
    });
    html += '</ul>';
  }

  html += `
    <div class="info-box">
      <strong>ℹ️ Information:</strong><br>
      • Daily counts reset automatically at midnight<br>
      • Users exceeding the limit are automatically removed from the group<br>
      • Admins: ${ADMINS.length > 0 ? ADMINS.join(', ') : 'None configured'}<br>
      • Dashboard refreshes every 30 seconds
    </div>

    <p class="timestamp">Last updated: ${new Date().toLocaleString()}</p>
  </div>
</body>
</html>
  `;

  res.send(html);
});

// Health check endpoint
app.get('/', (req, res) => {
  res.json({
    status: 'running',
    service: 'WhatsApp Limit Bot',
    timestamp: new Date().toISOString(),
    config: {
      messageLimit: MESSAGE_LIMIT,
      adminCount: ADMINS.length,
      activeUsers: Object.keys(dailyCount).length,
      bannedUsers: bannedUsers.length
    }
  });
});

// Start server
app.listen(PORT, () => {
  console.log('='.repeat(50));
  console.log('🚀 WhatsApp Limit Bot Server Started');
  console.log('='.repeat(50));
  console.log(`📡 Server running on port ${PORT}`);
  console.log(`🌐 Dashboard: http://localhost:${PORT}/dashboard`);
  console.log(`🔗 Webhook: http://localhost:${PORT}/webhook`);
  console.log(`📊 Message Limit: ${MESSAGE_LIMIT} messages/day`);
  console.log(`👥 Admins configured: ${ADMINS.length}`);
  console.log('='.repeat(50));
});
