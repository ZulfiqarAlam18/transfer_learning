# 📖 Project Overview - WhatsApp Limit Bot

## 🎯 What This Project Does

This is a **fully automated WhatsApp bot** that helps you manage WhatsApp group conversations by:

1. **Limiting messages per user** - Set a daily message limit (e.g., 5 messages/day)
2. **Auto-removing violators** - Automatically removes users who exceed the limit
3. **Admin controls** - Manage the bot via WhatsApp commands
4. **Real-time monitoring** - Beautiful web dashboard to track activity
5. **Ban system** - Permanently ban problematic users

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     WhatsApp Cloud API                      │
│              (Meta Developer Platform)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Webhook (HTTPS)
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Your Bot Server                           │
│              (Node.js + Express)                            │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   Webhook    │  │    Admin     │  │   Dashboard     │  │
│  │   Handler    │  │   Commands   │  │   (Web UI)      │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
│         │                  │                   │           │
│         └──────────┬───────┴───────────────────┘           │
│                    ▼                                        │
│         ┌────────────────────┐                             │
│         │  Message Counter   │                             │
│         │  & Limit Enforcer  │                             │
│         └────────────────────┘                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
whatsapp-limit-bot/
│
├── src/
│   └── index.js              # Main application logic
│
├── .env.example              # Environment variables template
├── .env                      # Your actual config (git-ignored)
├── .gitignore               # Git ignore rules
│
├── package.json             # Dependencies and scripts
├── setup.sh                 # Automated setup script
│
├── README.md                # Full documentation
├── QUICKSTART.md            # 5-minute setup guide
├── DEPLOYMENT.md            # Production deployment guide
├── API.md                   # API reference
└── PROJECT_OVERVIEW.md      # This file
```

---

## 🔧 Technology Stack

### Backend
- **Node.js** (v18+) - Runtime environment
- **Express.js** (v4) - Web framework
- **Axios** - HTTP client for API calls
- **dotenv** - Environment variable management
- **body-parser** - Parse incoming requests

### Frontend
- **HTML/CSS** - Dashboard UI
- **JavaScript** - Interactive features

### APIs
- **WhatsApp Cloud API** - Send/receive messages
- **Meta Graph API** - Manage groups

---

## 🚀 How It Works

### 1. Message Receiving Flow

```
User sends WhatsApp message
    ↓
WhatsApp sends POST to /webhook
    ↓
Bot parses message data
    ↓
Check if user is banned → YES → Ignore message
    ↓ NO
Check if admin command → YES → Execute command
    ↓ NO
Increment user's message count
    ↓
Count > limit? → YES → Warn + Remove from group
    ↓ NO
Count == limit? → YES → Send warning
    ↓
Return 200 OK
```

### 2. Admin Command Flow

```
Admin sends /limit 10
    ↓
Bot receives message
    ↓
Verify sender in ADMIN_NUMBERS
    ↓
Parse command (/limit) and args (10)
    ↓
Validate input (is number > 0?)
    ↓
Update MESSAGE_LIMIT = 10
    ↓
Send confirmation to admin
    ↓
New limit active immediately
```

### 3. Daily Reset Flow

```
Every minute, check current time
    ↓
Is it midnight (00:00)?
    ↓ YES
Reset dailyCount = {}
    ↓
Log reset action
    ↓
Continue monitoring
```

---

## 🎨 Features Breakdown

### Core Features

#### 1. Message Limiting
- Tracks messages per user per day
- Configurable limit (default: 5)
- Warns users approaching limit
- Counts reset at midnight

#### 2. Auto-Removal
- Removes users exceeding limit
- Sends warning before removal
- Works only if bot is group admin

#### 3. Admin Commands
- `/limit` - Change message limit
- `/reset` - Reset all counts
- `/stats` - View statistics
- `/ban` - Ban a user
- `/unban` - Unban a user
- `/help` - Show help

#### 4. Dashboard
- Real-time statistics
- User message counts
- Progress bars
- Banned users list
- Auto-refresh every 30s

#### 5. Ban System
- Permanent user blocking
- Manual ban/unban via commands
- Ignored messages from banned users

---

## 🔐 Security Features

1. **Environment Variables** - Sensitive data not in code
2. **Webhook Verification** - Validates incoming webhooks
3. **Admin Authorization** - Commands only from authorized numbers
4. **HTTPS Required** - Secure communication (production)
5. **Token Hiding** - Never exposes API tokens

---

## 📊 Data Storage

### Current Implementation (In-Memory)
- ✅ Simple and fast
- ✅ No database setup needed
- ❌ Data lost on restart
- ❌ Not suitable for large scale

### Production Recommendation
Use a database for persistent storage:
- **MongoDB** - NoSQL, easy integration
- **PostgreSQL** - Relational, robust
- **Redis** - Fast, for caching

Example migration to MongoDB:
```javascript
// Instead of:
let dailyCount = {};

// Use:
const DailyCount = mongoose.model('DailyCount', {
  phoneNumber: String,
  count: Number,
  date: Date
});
```

---

## 🎯 Use Cases

### 1. Community Management
- Prevent spam in large groups
- Ensure equal participation
- Reduce message overload

### 2. Customer Support
- Limit support requests per day
- Manage ticket volumes
- Prevent abuse

### 3. Educational Groups
- Control student messages
- Maintain focused discussions
- Enforce participation rules

### 4. Event Management
- Limit announcements
- Control group activity
- Manage RSVPs

---

## 📈 Scalability Considerations

### Current Limitations
- **In-memory storage** - Data lost on restart
- **Single server** - No horizontal scaling
- **No queue** - Messages processed sequentially
- **No caching** - API calls on every message

### Scaling Solutions

#### Small Scale (100-1000 users)
- ✅ Current setup works fine
- Add Redis for session storage
- Use PM2 for process management

#### Medium Scale (1000-10,000 users)
- Add database (MongoDB/PostgreSQL)
- Implement message queue (Bull/RabbitMQ)
- Add caching layer (Redis)
- Multiple server instances behind load balancer

#### Large Scale (10,000+ users)
- Microservices architecture
- Distributed message queue (Kafka)
- Database sharding
- CDN for dashboard
- Auto-scaling infrastructure

---

## 🔄 Workflow Examples

### New User Sends First Message

```
1. User (15551234567) joins group
2. User sends: "Hello everyone!"
3. Bot receives webhook
4. dailyCount["15551234567"] = 1
5. Bot logs: "User 15551234567 sent message 1/5"
6. No action needed (under limit)
```

### User Reaches Limit

```
1. User sends 5th message
2. dailyCount["15551234567"] = 5
3. Bot sends: "⚠️ You've reached your limit (5/5)"
4. User sends 6th message
5. dailyCount["15551234567"] = 6
6. Bot sends: "You'll be removed from group"
7. Bot calls removeUserFromGroup()
8. User removed from group
```

### Admin Changes Limit

```
1. Admin sends: "/limit 10"
2. Bot verifies admin status
3. Bot parses: command="/limit", arg="10"
4. Bot validates: 10 > 0 ✓
5. MESSAGE_LIMIT = 10
6. Bot replies: "✅ Limit updated to 10"
7. New limit applies to all users
```

---

## 🧪 Testing Strategy

### Unit Tests (Not Implemented Yet)
```javascript
// Example tests to add:
test('increments message count', () => {
  expect(incrementCount('15551234567')).toBe(1);
});

test('removes user when limit exceeded', async () => {
  await removeUserFromGroup('GROUP_ID', 'USER_ID');
  expect(mockAxios).toHaveBeenCalled();
});
```

### Integration Tests
- Test webhook endpoint
- Test admin commands
- Test dashboard rendering
- Test WhatsApp API integration

### Manual Testing Checklist
- [ ] Send message to bot
- [ ] Message count increases
- [ ] Warning at limit
- [ ] Removal after limit
- [ ] Admin commands work
- [ ] Dashboard updates
- [ ] Ban/unban works
- [ ] Midnight reset works

---

## 🚀 Deployment Options Comparison

| Platform | Cost | Difficulty | Best For |
|----------|------|------------|----------|
| **Render** | Free tier available | ⭐ Easy | Beginners, testing |
| **Railway** | Free tier | ⭐⭐ Easy | Quick deployments |
| **Vercel** | Free tier | ⭐ Very Easy | Serverless (limited) |
| **Heroku** | Paid only | ⭐⭐ Medium | Traditional apps |
| **DigitalOcean** | $5/month | ⭐⭐⭐ Advanced | Full control |
| **AWS** | Variable | ⭐⭐⭐⭐ Complex | Enterprise |

**Recommendation**: Start with Render (free), upgrade to VPS when needed.

---

## 📝 Configuration Examples

### Minimal Setup (.env)
```env
WHATSAPP_TOKEN=your_token
PHONE_NUMBER_ID=your_phone_id
```

### Recommended Setup (.env)
```env
WHATSAPP_TOKEN=EAAxxxxxxxxx
PHONE_NUMBER_ID=123456789
WEBHOOK_VERIFY_TOKEN=my_secret_token_123
MESSAGE_LIMIT=5
ADMIN_NUMBERS=15551234567,15557654321
PORT=3000
```

### Production Setup (.env)
```env
WHATSAPP_TOKEN=permanent_token_here
PHONE_NUMBER_ID=production_phone_id
WEBHOOK_VERIFY_TOKEN=strong_secret_token
MESSAGE_LIMIT=10
ADMIN_NUMBERS=admin1,admin2,admin3
PORT=3000
NODE_ENV=production
DATABASE_URL=mongodb://...
REDIS_URL=redis://...
```

---

## 🎓 Learning Resources

### WhatsApp Cloud API
- [Official Documentation](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [Getting Started Guide](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started)
- [API Reference](https://developers.facebook.com/docs/whatsapp/cloud-api/reference)

### Node.js & Express
- [Express.js Guide](https://expressjs.com/en/guide/routing.html)
- [Node.js Documentation](https://nodejs.org/docs/)
- [Axios Documentation](https://axios-http.com/docs/intro)

### Deployment
- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [PM2 Documentation](https://pm2.keymetrics.io/docs/)

---

## 🔮 Future Enhancements

### Planned Features
- [ ] Database integration (MongoDB)
- [ ] Multi-group support
- [ ] Role-based limits (admin/VIP/regular)
- [ ] Message logging and analytics
- [ ] Scheduled messages
- [ ] Custom auto-replies
- [ ] User statistics export
- [ ] Advanced dashboard with charts

### Advanced Ideas
- [ ] AI-powered spam detection
- [ ] Sentiment analysis
- [ ] Automated moderation
- [ ] Integration with other platforms
- [ ] Mobile app for management
- [ ] Multi-language support

---

## ❓ FAQ

**Q: Does this work with regular WhatsApp?**
A: No, you need WhatsApp Business Account and Cloud API access.

**Q: Is this free?**
A: The bot code is free. WhatsApp Cloud API has conversation-based pricing.

**Q: Can I use this for multiple groups?**
A: Current version tracks all groups together. Multi-group support is planned.

**Q: What happens if the server restarts?**
A: Message counts reset (in-memory storage). Use database for persistence.

**Q: Can users bypass the limit?**
A: No, unless they use a different phone number.

**Q: Do I need a dedicated server?**
A: No, you can use free hosting platforms like Render.

**Q: Is my WhatsApp token secure?**
A: Yes, if you keep it in .env and never commit to Git.

---

## 📞 Support

For help with:
- **Setup issues**: See [QUICKSTART.md](QUICKSTART.md)
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **API details**: See [API.md](API.md)
- **WhatsApp API**: Meta Developer Support

---

## 📄 License

MIT License - Free to use, modify, and distribute.

---

## 🙏 Credits

Built with:
- WhatsApp Cloud API by Meta
- Express.js web framework
- Node.js runtime
- Love and coffee ☕

---

**Ready to get started?** → Read [QUICKSTART.md](QUICKSTART.md)

**Need to deploy?** → Read [DEPLOYMENT.md](DEPLOYMENT.md)

**Want API details?** → Read [API.md](API.md)
