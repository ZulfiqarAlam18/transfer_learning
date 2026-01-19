# 🚀 Quick Start Guide

Get your WhatsApp bot running in 5 minutes!

## 📋 Prerequisites

Before you start, make sure you have:

- ✅ Node.js 18+ installed ([Download here](https://nodejs.org/))
- ✅ WhatsApp Business Account
- ✅ Meta Developer Account ([Sign up here](https://developers.facebook.com/))
- ✅ Text editor (VS Code recommended)

## 🎯 Step-by-Step Setup

### 1️⃣ Get WhatsApp API Credentials

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Click **"My Apps"** → **"Create App"**
3. Choose **"Business"** type
4. Fill in app details and create

5. Add **WhatsApp** product to your app:
   - In your app dashboard, click **"Add Product"**
   - Select **"WhatsApp"** → **"Set Up"**

6. Get your credentials:
   - Go to **WhatsApp** → **"API Setup"**
   - Copy **"Temporary Access Token"** → This is your `WHATSAPP_TOKEN`
   - Copy **"Phone number ID"** → This is your `PHONE_NUMBER_ID`

   **⚠️ Important**: Temporary token expires in 24 hours. For production, create a permanent token:
   - Go to **Settings** → **"Business Settings"** → **"System Users"**
   - Create a system user and generate permanent token

### 2️⃣ Install the Bot

1. **Download/Clone the project** (you already have it!)

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Create environment file**:
   ```bash
   cp .env.example .env
   ```

4. **Edit `.env` file** with your credentials:
   ```env
   WHATSAPP_TOKEN=EAAxxxxxxxxxxxxxxxxx
   PHONE_NUMBER_ID=123456789012345
   WEBHOOK_VERIFY_TOKEN=verify123
   MESSAGE_LIMIT=5
   ADMIN_NUMBERS=15551234567,15557654321
   PORT=3000
   ```

   Replace:
   - `EAAxxxxxxxxxxxxxxxxx` with your WhatsApp token
   - `123456789012345` with your phone number ID
   - `15551234567,15557654321` with admin phone numbers (with country code, no +)

### 3️⃣ Test Locally

1. **Start the bot**:
   ```bash
   npm start
   ```

   You should see:
   ```
   🚀 WhatsApp Limit Bot Server Started
   📡 Server running on port 3000
   🌐 Dashboard: http://localhost:3000/dashboard
   ```

2. **Open dashboard** in browser:
   ```
   http://localhost:3000/dashboard
   ```

3. **Test webhook**:
   ```
   http://localhost:3000/webhook?hub.mode=subscribe&hub.verify_token=verify123&hub.challenge=test123
   ```
   Should return: `test123`

### 4️⃣ Expose Locally (For Testing)

To test WhatsApp integration locally, you need a public URL:

**Option A: Using ngrok**
```bash
# Install ngrok: https://ngrok.com/download
ngrok http 3000
```
Copy the `https` URL (e.g., `https://abc123.ngrok.io`)

**Option B: Using localtunnel**
```bash
npm install -g localtunnel
lt --port 3000
```

### 5️⃣ Configure WhatsApp Webhook

1. Go to [Meta Developer Console](https://developers.facebook.com/)
2. Select your app → **WhatsApp** → **"Configuration"**
3. Click **"Edit"** next to Webhook

4. Enter:
   - **Callback URL**: `https://your-ngrok-url.ngrok.io/webhook`
   - **Verify Token**: `verify123`

5. Click **"Verify and Save"**

6. Subscribe to **messages** webhook field

### 6️⃣ Test Your Bot!

1. **Send a test message** to your WhatsApp Business number
2. **Check server logs** - you should see the message received
3. **Check dashboard** - message count should update
4. **Test admin commands** (send from admin number):
   ```
   /help
   /stats
   /limit 3
   ```

## 🎉 Success!

Your bot is now working! Here's what happens:

- ✅ Users can send up to 5 messages per day (configurable)
- ✅ Bot warns users approaching limit
- ✅ Auto-removes users who exceed limit
- ✅ Admins can control bot via commands
- ✅ Dashboard shows real-time statistics
- ✅ Counts reset at midnight

## 🚀 Next Steps

### Deploy to Production

For 24/7 operation, deploy to a hosting platform:

1. **[Render](https://render.com)** (Recommended - Free tier available)
   - See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guide
   - Takes ~10 minutes

2. **[Railway](https://railway.app)** (Easy alternative)
   - Good free tier
   - Auto-deploys from GitHub

3. **Your own VPS** (Full control)
   - DigitalOcean, AWS, etc.
   - Requires more setup

**👉 Follow [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide**

## 📚 Learn More

### Admin Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `/limit <number>` | Change daily limit | `/limit 10` |
| `/reset` | Reset all counts | `/reset` |
| `/stats` | View statistics | `/stats` |
| `/ban <number>` | Ban a user | `/ban 15551234567` |
| `/unban <number>` | Unban a user | `/unban 15551234567` |
| `/help` | Show help | `/help` |

### Project Structure

```
whatsapp-limit-bot/
├── src/
│   └── index.js          # Main application
├── .env                  # Your config (don't commit!)
├── .env.example         # Config template
├── package.json         # Dependencies
├── README.md           # Full documentation
├── DEPLOYMENT.md       # Deployment guide
└── QUICKSTART.md       # This file
```

### Useful Links

- 📖 **Full README**: [README.md](README.md)
- 🚀 **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- 📘 **WhatsApp API Docs**: https://developers.facebook.com/docs/whatsapp
- 💬 **Express.js Docs**: https://expressjs.com/

## 🐛 Troubleshooting

### Issue: `npm install` fails
**Solution**: Make sure Node.js 18+ is installed:
```bash
node --version  # Should be v18.0.0 or higher
```

### Issue: Webhook verification fails
**Solution**: 
- Check verify token matches in `.env` and Meta Console
- Ensure server is running and accessible
- Check URL is correct (https required for production)

### Issue: Messages not received
**Solution**:
- Verify webhook is configured in Meta Console
- Check "messages" field is subscribed
- Look at server logs for errors
- Test webhook with Meta's test button

### Issue: Can't remove users from group
**Solution**:
- Bot must be admin in the WhatsApp group
- Add your WhatsApp Business number to group
- Make it admin before testing removal

### Issue: Admin commands don't work
**Solution**:
- Check phone number format in `ADMIN_NUMBERS` (no + sign, with country code)
- Example: `15551234567` not `+1-555-123-4567`
- Restart server after changing `.env`

## ⚡ Quick Commands Reference

```bash
# Install dependencies
npm install

# Start server
npm start

# Development mode (auto-reload)
npm run dev

# View logs (if using PM2)
pm2 logs whatsapp-bot

# Restart server (PM2)
pm2 restart whatsapp-bot
```

## 🎯 Testing Checklist

Before deploying, test these features:

- [ ] Server starts without errors
- [ ] Dashboard loads and displays correctly
- [ ] Webhook verification succeeds
- [ ] Bot receives test messages
- [ ] Message count increases correctly
- [ ] Warning sent at limit
- [ ] User removed after exceeding limit
- [ ] Admin commands work (`/help`, `/stats`, etc.)
- [ ] Ban/unban functionality works
- [ ] Dashboard updates in real-time

## 💡 Tips

1. **Use a test group** before deploying to your main group
2. **Start with higher limit** (10-20) while testing
3. **Make yourself admin** in test group
4. **Monitor logs** during initial testing
5. **Backup your config** before making changes

## 🎊 You're All Set!

You now have a fully functional WhatsApp bot! 

**Want more features?** Check the README.md for ideas:
- Database integration
- Multi-group support
- Custom auto-replies
- Advanced analytics
- Scheduled messages

**Need help?** Review the troubleshooting section or check WhatsApp API docs.

Happy botting! 🤖💬
