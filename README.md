# WhatsApp Cloud API Message Limit Bot

A fully automated WhatsApp bot built with Node.js and Express that manages group messages, enforces daily message limits, and provides admin controls.

## 🌟 Features

- ✅ **Message Limiting**: Set daily message limits per user (default: 5 messages/day)
- 🚫 **Auto-removal**: Automatically removes users who exceed the daily limit
- 👮 **Admin Commands**: Control the bot via WhatsApp commands
- 📊 **Dashboard**: Web-based monitoring dashboard with real-time statistics
- 🔄 **Auto-reset**: Daily message counts reset automatically at midnight
- ⛔ **Ban System**: Ban/unban users permanently
- 📈 **Statistics**: Track message counts and user activity

## 📋 Admin Commands

Use these commands directly in WhatsApp (admin only):

| Command | Description | Example |
|---------|-------------|---------|
| `/limit <number>` | Change daily message limit | `/limit 10` |
| `/reset` | Reset all message counts | `/reset` |
| `/stats` | Show message statistics | `/stats` |
| `/ban <number>` | Ban a user permanently | `/ban 15551234567` |
| `/unban <number>` | Unban a user | `/unban 15551234567` |
| `/help` | Show help message | `/help` |

## 🚀 Quick Start

### Prerequisites

- Node.js 18 or higher
- WhatsApp Business Account
- Meta Developer Account
- WhatsApp Cloud API access

### Installation

1. **Clone or download this project**
   ```bash
   cd whatsapp-limit-bot
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```env
   WHATSAPP_TOKEN=your_whatsapp_access_token
   PHONE_NUMBER_ID=your_phone_number_id
   WEBHOOK_VERIFY_TOKEN=verify123
   MESSAGE_LIMIT=5
   ADMIN_NUMBERS=15551234567,15557654321
   ```

4. **Run the bot**
   ```bash
   npm start
   ```
   
   For development with auto-reload:
   ```bash
   npm run dev
   ```

5. **Access the dashboard**
   ```
   http://localhost:3000/dashboard
   ```

## 🔧 Configuration

### Getting WhatsApp Credentials

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create a new app or select existing one
3. Add WhatsApp product
4. Get your credentials from the API Setup page:
   - **Access Token** (`WHATSAPP_TOKEN`)
   - **Phone Number ID** (`PHONE_NUMBER_ID`)

### Setting Up Webhook

1. In Meta Developer Console, go to WhatsApp > Configuration
2. Set webhook URL:
   ```
   https://your-domain.com/webhook
   ```
3. Set verify token: `verify123` (or your custom token)
4. Subscribe to messages webhook field

## 📦 Deployment

### Deploy to Render (Recommended - Free)

1. **Create GitHub repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin your-repo-url
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Create new Web Service
   - Connect your GitHub repository
   - Set environment variables in Render dashboard
   - Deploy!

3. **Configure webhook in Meta**
   - Use your Render URL: `https://your-app.onrender.com/webhook`
   - Verify token: `verify123`

### Environment Variables on Render

Set these in Render dashboard under Environment:

```
WHATSAPP_TOKEN=your_token
PHONE_NUMBER_ID=your_phone_id
WEBHOOK_VERIFY_TOKEN=verify123
MESSAGE_LIMIT=5
ADMIN_NUMBERS=15551234567,15557654321
PORT=3000
```

### Deploy to Railway

1. Install Railway CLI or use web interface
2. Create new project from GitHub
3. Add environment variables
4. Deploy automatically on push

### Deploy to Your VPS

1. SSH into your server
2. Install Node.js 18+
3. Clone repository
4. Install dependencies
5. Use PM2 for process management:
   ```bash
   npm install -g pm2
   pm2 start src/index.js --name whatsapp-bot
   pm2 startup
   pm2 save
   ```

## 📊 Dashboard Features

Access the web dashboard at `/dashboard` to see:

- 📈 Real-time message statistics
- 👥 Active users count
- 📊 Message counts per user
- 🚫 List of banned users
- ⚙️ Current configuration
- 🔄 Auto-refresh every 30 seconds

## 🛠️ Project Structure

```
whatsapp-limit-bot/
├── src/
│   └── index.js          # Main application file
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── package.json         # Project dependencies
└── README.md           # This file
```

## 🔒 Security Notes

- Never commit `.env` file to Git
- Keep your WhatsApp token secret
- Use HTTPS in production
- Regularly update dependencies
- Implement rate limiting for production

## 🐛 Troubleshooting

### Bot not receiving messages
- Check webhook is properly configured in Meta Developer Console
- Verify webhook URL is accessible publicly
- Check server logs for errors

### Messages not sending
- Verify `WHATSAPP_TOKEN` is correct and not expired
- Check `PHONE_NUMBER_ID` matches your WhatsApp Business number
- Ensure bot has permission to send messages

### Auto-removal not working
- Bot must be admin in the group
- Check group ID is being received in webhook payload
- Verify permissions in WhatsApp Business settings

## 📝 License

MIT License - feel free to use this project for any purpose.

## 🤝 Support

For issues or questions:
- Check the troubleshooting section
- Review Meta's WhatsApp Cloud API documentation
- Check server logs for errors

## 🚀 Next Steps & Advanced Features

Want to add more features? Consider:

1. **Database Integration**: Use MongoDB or PostgreSQL instead of in-memory storage
2. **Multi-group Support**: Manage multiple WhatsApp groups with separate limits
3. **Role-based Limits**: Different limits for admins, VIP, and regular members
4. **Message Logging**: Store all messages for analytics
5. **Scheduled Messages**: Send automated messages at specific times
6. **Custom Responses**: Auto-reply based on keywords
7. **Analytics**: Advanced statistics and reporting
8. **API Integration**: Connect with external services

## 📚 Resources

- [WhatsApp Cloud API Documentation](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [Express.js Documentation](https://expressjs.com/)
- [Node.js Documentation](https://nodejs.org/)
- [Render Deployment Guide](https://render.com/docs)

---

Made with ❤️ for WhatsApp group management
