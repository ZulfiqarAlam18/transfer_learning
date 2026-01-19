# Deployment Guide - WhatsApp Limit Bot

This guide will walk you through deploying your WhatsApp bot to production.

## 📋 Table of Contents

1. [Render Deployment (Recommended)](#render-deployment)
2. [Railway Deployment](#railway-deployment)
3. [VPS Deployment](#vps-deployment)
4. [WhatsApp Configuration](#whatsapp-configuration)
5. [Post-Deployment Checklist](#post-deployment-checklist)

---

## 🚀 Render Deployment (Recommended - Free)

Render is the easiest platform for deploying Node.js applications with a generous free tier.

### Step 1: Prepare Your Code

1. **Initialize Git repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - WhatsApp Bot"
   ```

2. **Create GitHub repository**:
   - Go to https://github.com/new
   - Name: `whatsapp-limit-bot`
   - Make it private (recommended for production)
   - Don't initialize with README

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/whatsapp-limit-bot.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Create Render Account

1. Go to https://render.com
2. Sign up or log in using GitHub
3. Authorize Render to access your repositories

### Step 3: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `whatsapp-limit-bot`
3. Configure the service:

   **Basic Settings:**
   - **Name**: `whatsapp-bot` (or your preferred name)
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Runtime**: `Node`

   **Build & Deploy:**
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`

4. **Plan**: Select **"Free"**

### Step 4: Add Environment Variables

In Render dashboard, go to **Environment** section and add:

```plaintext
WHATSAPP_TOKEN=EAAxxxxxxxxxxxxxxxxx
PHONE_NUMBER_ID=123456789012345
WEBHOOK_VERIFY_TOKEN=verify123
MESSAGE_LIMIT=5
ADMIN_NUMBERS=15551234567,15557654321
PORT=3000
```

**Important:**
- Get `WHATSAPP_TOKEN` from Meta Developer Console
- Get `PHONE_NUMBER_ID` from WhatsApp API Setup
- Add all admin phone numbers with country code, no spaces

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (2-3 minutes)
3. Your bot will be live at: `https://your-app-name.onrender.com`

### Step 6: Test Deployment

1. Visit your app URL to check if it's running:
   ```
   https://your-app-name.onrender.com/
   ```
   You should see JSON response with status.

2. Check dashboard:
   ```
   https://your-app-name.onrender.com/dashboard
   ```

---

## 🚄 Railway Deployment

Railway offers simple deployment with automatic SSL and custom domains.

### Step 1: Install Railway CLI (Optional)

```bash
npm install -g @railway/cli
railway login
```

### Step 2: Deploy via Web Interface

1. Go to https://railway.app
2. Sign in with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your `whatsapp-limit-bot` repository
5. Railway will auto-detect Node.js

### Step 3: Add Environment Variables

In Railway project settings → Variables:

```plaintext
WHATSAPP_TOKEN=your_token_here
PHONE_NUMBER_ID=your_phone_id
WEBHOOK_VERIFY_TOKEN=verify123
MESSAGE_LIMIT=5
ADMIN_NUMBERS=admin_numbers
```

### Step 4: Deploy

Railway will automatically deploy on every push to main branch.

---

## 🖥️ VPS Deployment (DigitalOcean, AWS, etc.)

For more control, deploy on your own VPS.

### Prerequisites

- Ubuntu 20.04+ or similar Linux server
- Root or sudo access
- Domain name (optional but recommended)

### Step 1: Connect to Server

```bash
ssh root@your-server-ip
```

### Step 2: Install Node.js

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verify installation
node --version
npm --version
```

### Step 3: Install PM2 (Process Manager)

```bash
sudo npm install -g pm2
```

### Step 4: Clone Your Repository

```bash
cd /var/www
git clone https://github.com/YOUR_USERNAME/whatsapp-limit-bot.git
cd whatsapp-limit-bot
```

### Step 5: Install Dependencies

```bash
npm install --production
```

### Step 6: Create Environment File

```bash
nano .env
```

Add your variables:
```env
WHATSAPP_TOKEN=your_token
PHONE_NUMBER_ID=your_phone_id
WEBHOOK_VERIFY_TOKEN=verify123
MESSAGE_LIMIT=5
ADMIN_NUMBERS=numbers_here
PORT=3000
```

Save with `Ctrl+X`, `Y`, `Enter`

### Step 7: Start with PM2

```bash
pm2 start src/index.js --name whatsapp-bot
pm2 startup
pm2 save
```

### Step 8: Setup Nginx (Reverse Proxy)

```bash
sudo apt install nginx -y

# Create Nginx config
sudo nano /etc/nginx/sites-available/whatsapp-bot
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/whatsapp-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 9: Setup SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### Step 10: Firewall Setup

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

---

## 📱 WhatsApp Configuration

After deploying, configure WhatsApp webhook.

### Step 1: Get Your Webhook URL

- **Render**: `https://your-app.onrender.com/webhook`
- **Railway**: `https://your-app.railway.app/webhook`
- **VPS**: `https://your-domain.com/webhook`

### Step 2: Configure in Meta Developer Console

1. Go to https://developers.facebook.com/
2. Select your app
3. Go to **WhatsApp** → **Configuration**
4. Click **"Edit"** under Webhook

**Webhook Configuration:**
- **Callback URL**: Your webhook URL
- **Verify Token**: `verify123` (or your custom token)

5. Click **"Verify and Save"**

### Step 3: Subscribe to Webhooks

Subscribe to these webhook fields:
- ✅ `messages`

### Step 4: Test the Integration

1. Send a message to your WhatsApp Business number
2. Check server logs for incoming webhook
3. Verify bot responds correctly

---

## ✅ Post-Deployment Checklist

After deployment, verify everything works:

### Functional Tests

- [ ] Server is accessible at deployment URL
- [ ] Dashboard loads correctly
- [ ] Webhook verification succeeds
- [ ] Bot receives WhatsApp messages
- [ ] Message counting works
- [ ] Auto-removal works (test in test group)
- [ ] Admin commands work
- [ ] Daily reset works (wait for midnight or test manually)
- [ ] Dashboard shows real-time data

### Security Checks

- [ ] Environment variables are secure
- [ ] `.env` file is not committed to Git
- [ ] HTTPS is enabled
- [ ] Webhook uses verify token
- [ ] Admin numbers are correctly configured

### Monitoring

- [ ] Check logs regularly: `pm2 logs whatsapp-bot` (VPS)
- [ ] Monitor Render logs in dashboard
- [ ] Set up uptime monitoring (e.g., UptimeRobot)
- [ ] Monitor API usage in Meta Developer Console

---

## 🔧 Maintenance

### Updating the Bot

**Render/Railway (Auto-deploy):**
```bash
git add .
git commit -m "Update message"
git push
```

**VPS (Manual):**
```bash
cd /var/www/whatsapp-limit-bot
git pull
npm install
pm2 restart whatsapp-bot
```

### Viewing Logs

**Render**: Dashboard → Logs
**Railway**: Project → Deployments → Logs
**VPS**: `pm2 logs whatsapp-bot`

### Backup Data

If using file-based storage, regularly backup your data:
```bash
pm2 save  # Saves current state
```

---

## 🐛 Common Issues

### Issue: Webhook verification fails
**Solution**: 
- Check verify token matches
- Ensure server is publicly accessible
- Check server logs for errors

### Issue: Messages not received
**Solution**:
- Verify webhook subscription is active
- Check message webhook field is subscribed
- Test with webhook test tool in Meta Console

### Issue: Bot can't remove users
**Solution**:
- Ensure bot phone number is admin in group
- Check group ID is being received
- Verify API permissions

### Issue: Server sleeps on Render (Free plan)
**Solution**:
- Render free tier sleeps after 15 min inactivity
- Use uptime monitor to ping server every 10 minutes
- Or upgrade to paid plan for 24/7 uptime

---

## 📊 Monitoring & Analytics

### Uptime Monitoring

Use UptimeRobot or similar:
1. Create account at https://uptimerobot.com
2. Add monitor for your URL
3. Set check interval to 5-10 minutes
4. Add alert contacts

### Log Analysis

Monitor these in logs:
- Message receive rate
- Error frequency
- Admin command usage
- User removals

---

## 🎯 Production Best Practices

1. **Use Environment Variables**: Never hardcode credentials
2. **Enable HTTPS**: Always use SSL in production
3. **Monitor Logs**: Check regularly for errors
4. **Rate Limiting**: Consider adding rate limits
5. **Database**: Use persistent storage for production
6. **Backups**: Regular backups of user data
7. **Updates**: Keep dependencies updated
8. **Testing**: Test in staging before production

---

## 📞 Support Resources

- **WhatsApp API**: https://developers.facebook.com/docs/whatsapp
- **Render Support**: https://render.com/docs
- **Railway Support**: https://docs.railway.app
- **PM2 Documentation**: https://pm2.keymetrics.io/docs

---

**Deployment Complete!** 🎉

Your WhatsApp bot is now live and ready to manage your group messages!
