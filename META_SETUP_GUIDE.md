# 🎯 Complete Meta Developer Setup Guide

## 📋 Table of Contents
1. [Pricing Information](#pricing-information)
2. [Getting WhatsApp Credentials](#getting-whatsapp-credentials)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [Understanding Your Credentials](#understanding-your-credentials)
5. [Testing for Free](#testing-for-free)

---

## 💰 Pricing Information

### Meta WhatsApp Cloud API Pricing

#### ✅ **FREE TIER (Perfect for Testing!)**

Meta provides **1,000 FREE conversations per month** - Great for testing and small projects!

**What's included for FREE:**
- ✅ 1,000 conversations per month (resets monthly)
- ✅ Full API access
- ✅ Test phone number included
- ✅ All features available
- ✅ No credit card required initially
- ✅ Perfect for development and testing

**What is a "conversation"?**
- A conversation = 24-hour window with a user
- Multiple messages within 24 hours = 1 conversation
- Example: User sends 50 messages in one day = 1 conversation

**Free Tier Calculation:**
```
1,000 free conversations/month = ~33 users per day
Or: 1,000 users if each sends messages once a month

For a group of 50 people:
- If each person messages every day: 50 conversations/day × 30 days = 1,500/month
- Cost: 1,000 free + 500 paid = ~$2.50/month
```

#### 💵 **PAID PRICING (After Free Tier)**

**Conversation-based pricing (after 1,000 free):**

| Conversation Type | Price (per conversation) |
|-------------------|-------------------------|
| **User-initiated** | $0.005 - $0.009 USD |
| **Business-initiated** | $0.016 - $0.045 USD |

**Varies by country:**
- India: ~$0.0042 per conversation
- USA: ~$0.0088 per conversation
- UK: ~$0.0104 per conversation

**Example costs:**
- 2,000 conversations/month: ~$5-10/month
- 5,000 conversations/month: ~$20-40/month
- 10,000 conversations/month: ~$40-80/month

#### 💡 **For Your Testing:**

**Absolutely FREE for testing!** Here's why:
- ✅ First 1,000 conversations are free
- ✅ No credit card required to start
- ✅ Test phone number provided
- ✅ Can test with 10-20 users extensively
- ✅ Perfect for development

**When you'll need to pay:**
- After 1,000 conversations per month
- When you add a payment method (optional)
- For production with many users

---

## 🚀 Getting WhatsApp Credentials

You need these 3 things:

1. **WHATSAPP_TOKEN** - API Access Token
2. **PHONE_NUMBER_ID** - Your WhatsApp Business Phone ID
3. **ADMIN_NUMBERS** - Your personal phone numbers

Let's get them step by step!

---

## 📝 Step-by-Step Setup

### STEP 1: Create Meta Developer Account

1. **Go to Meta for Developers**
   - Visit: https://developers.facebook.com/
   - Click **"Get Started"** or **"My Apps"**

2. **Sign Up / Log In**
   - Use your Facebook/Instagram account
   - Or create a new account
   - **No credit card required!**

3. **Complete Your Profile**
   - Fill in basic information
   - Verify your email if prompted

**Time needed:** 2-3 minutes

---

### STEP 2: Create a New App

1. **Click "Create App"**
   - On your dashboard, click **"Create App"** button
   - Or go to: https://developers.facebook.com/apps/create/

2. **Select App Type**
   - Choose: **"Business"** (recommended)
   - Click **"Next"**

3. **Fill App Details**
   ```
   App Name: WhatsApp Message Bot (or any name)
   App Contact Email: your_email@example.com
   Business Account: Create new or select existing
   ```

4. **Create App**
   - Click **"Create App"**
   - Complete security check if prompted
   - Wait 3-5 seconds

✅ **Your app is created!**

**Time needed:** 2-3 minutes

---

### STEP 3: Add WhatsApp Product

1. **Find WhatsApp in Products**
   - You'll see a dashboard with available products
   - Scroll down to find **"WhatsApp"**
   - Click **"Set Up"** button

2. **WhatsApp Setup Wizard**
   - You'll be taken to WhatsApp setup page
   - You'll see "API Setup" section

✅ **WhatsApp is now added to your app!**

**Time needed:** 1 minute

---

### STEP 4: Get Your Credentials (IMPORTANT!)

#### 4.1 Get WHATSAPP_TOKEN

1. **Go to API Setup**
   - In your app, click: **WhatsApp** → **"Getting Started"** or **"API Setup"**

2. **Find "Temporary Access Token"**
   - Look for a section called **"Temporary access token"**
   - You'll see a long token starting with `EAA...`
   - Click **"Copy"** button

3. **Save it somewhere safe!**
   ```
   WHATSAPP_TOKEN=EAAGZBl0Vyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

   ⚠️ **IMPORTANT:**
   - This token expires in **24 hours** (for testing)
   - For production, we'll create a permanent token later
   - Keep it secret - don't share publicly!

#### 4.2 Get PHONE_NUMBER_ID

1. **Same "API Setup" Page**
   - Look for **"Phone Number ID"** section
   - You'll see a test phone number provided by Meta
   - Format: `123456789012345` (15 digits)

2. **Copy Phone Number ID**
   ```
   PHONE_NUMBER_ID=123456789012345
   ```

3. **Copy the Test Number (for receiving messages)**
   - You'll also see: **"Phone number"** like `+1 555-025-6789`
   - This is the number users will message
   - Save it to test your bot

   ```
   Test WhatsApp Number: +1 555-025-6789
   ```

#### 4.3 Get ADMIN_NUMBERS (Your Phone)

This is **your personal WhatsApp phone number** that will control the bot.

1. **Format Your Phone Number**
   - Remove all spaces, dashes, and the + sign
   - Include country code
   
   **Examples:**
   ```
   USA: +1-555-123-4567 → 15551234567
   UK: +44 20 1234 5678 → 442012345678
   India: +91 98765 43210 → 919876543210
   Pakistan: +92 300 1234567 → 923001234567
   ```

2. **Your Admin Number:**
   ```
   ADMIN_NUMBERS=your_country_code_and_number
   ```

   For multiple admins (comma-separated):
   ```
   ADMIN_NUMBERS=15551234567,919876543210
   ```

---

### STEP 5: Configure Your Bot

1. **Open your `.env` file**
   ```bash
   cd /home/zulfi/Desktop/boot
   nano .env
   ```

2. **Add your credentials:**
   ```env
   # WhatsApp Cloud API Configuration
   WHATSAPP_TOKEN=EAAGZBl0Vyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   PHONE_NUMBER_ID=123456789012345
   
   # Webhook Configuration
   WEBHOOK_VERIFY_TOKEN=verify123
   
   # Server Configuration
   PORT=3000
   
   # Bot Configuration
   MESSAGE_LIMIT=5
   
   # Admin Phone Numbers (your personal WhatsApp number)
   ADMIN_NUMBERS=15551234567
   ```

3. **Save and close:**
   - Press `Ctrl + X`
   - Press `Y`
   - Press `Enter`

✅ **Configuration complete!**

---

### STEP 6: Start Your Bot

1. **Install dependencies** (if not done):
   ```bash
   npm install
   ```

2. **Start the server:**
   ```bash
   npm start
   ```

3. **You should see:**
   ```
   🚀 WhatsApp Limit Bot Server Started
   📡 Server running on port 3000
   🌐 Dashboard: http://localhost:3000/dashboard
   📊 Message Limit: 5 messages/day
   👥 Admins configured: 1
   ```

✅ **Bot is running!**

---

### STEP 7: Expose Your Local Server (For Testing)

To receive WhatsApp messages, you need a public URL.

#### Option A: Using ngrok (Recommended)

1. **Download ngrok:**
   - Visit: https://ngrok.com/download
   - Or install via snap:
   ```bash
   sudo snap install ngrok
   ```

2. **Sign up (free):**
   - Create account at https://dashboard.ngrok.com/signup
   - Copy your auth token

3. **Configure ngrok:**
   ```bash
   ngrok config add-authtoken YOUR_AUTH_TOKEN
   ```

4. **Expose your server:**
   ```bash
   ngrok http 3000
   ```

5. **Copy the HTTPS URL:**
   ```
   Forwarding  https://abc123.ngrok-free.app → http://localhost:3000
   ```
   
   Your webhook URL: `https://abc123.ngrok-free.app/webhook`

#### Option B: Using localtunnel (No signup needed)

1. **Install:**
   ```bash
   npm install -g localtunnel
   ```

2. **Expose server:**
   ```bash
   lt --port 3000
   ```

3. **Copy the URL:**
   ```
   your url is: https://funny-cat-12.loca.lt
   ```
   
   Your webhook URL: `https://funny-cat-12.loca.lt/webhook`

---

### STEP 8: Configure WhatsApp Webhook

1. **Go to Meta Developer Console**
   - Visit: https://developers.facebook.com/apps
   - Select your app

2. **Navigate to WhatsApp Configuration**
   - Click: **WhatsApp** → **Configuration**
   - Find the **"Webhook"** section

3. **Click "Edit"**
   
4. **Enter Webhook Details:**
   ```
   Callback URL: https://your-ngrok-url.ngrok-free.app/webhook
   Verify Token: verify123
   ```

5. **Click "Verify and Save"**
   - Meta will test your webhook
   - You should see ✅ Success!

6. **Subscribe to Webhook Fields**
   - Find **"Webhook fields"**
   - Check ✅ **"messages"**
   - Click **"Subscribe"**

✅ **Webhook configured!**

---

### STEP 9: Test Your Bot

#### 9.1 Add Test Number to WhatsApp

1. **Get the test number from Meta Console**
   - Example: `+1 555-025-6789`

2. **Add to WhatsApp:**
   - Open WhatsApp on your phone
   - Add this number as a contact: "WhatsApp Test Bot"
   - Start a conversation

#### 9.2 Send Test Messages

1. **From your phone, send:**
   ```
   Hello bot!
   ```

2. **Check your terminal:**
   ```
   Received message from 15551234567: Hello bot!
   User 15551234567 sent message number 1/5
   ```

3. **Check dashboard:**
   - Visit: http://localhost:3000/dashboard
   - You should see your message count!

#### 9.3 Test Admin Commands

1. **Send from your admin phone:**
   ```
   /help
   ```

2. **You should receive:**
   ```
   📋 Admin Commands

   /limit <number> - Change daily message limit
   /reset - Reset all message counts
   /stats - Show message statistics
   /ban <number> - Ban a user
   /unban <number> - Unban a user
   /help - Show this help message

   Current limit: 5 messages/day
   ```

3. **Try other commands:**
   ```
   /stats
   /limit 10
   /reset
   ```

✅ **Everything is working!**

---

## 🔐 Understanding Your Credentials

### WHATSAPP_TOKEN

**What it is:** Access token to authenticate API requests

**Format:** `EAAGZBl0Vy...` (long string)

**Types:**
- **Temporary (24 hours)** - For testing
- **Permanent (never expires)** - For production

**How to create permanent token:**

1. Go to: **Business Settings** → **System Users**
2. Click **"Add"** → Create system user
3. Click on the system user
4. Click **"Generate New Token"**
5. Select your app
6. Select permissions: `whatsapp_business_messaging`
7. Copy the permanent token
8. Update your `.env` file

### PHONE_NUMBER_ID

**What it is:** Unique identifier for your WhatsApp Business number

**Format:** `123456789012345` (15 digits)

**Where to find:**
- WhatsApp → API Setup
- Or: WhatsApp → Phone Numbers

**Test vs Production:**
- **Test number:** Provided by Meta (free, limited)
- **Production number:** Your own business number

### ADMIN_NUMBERS

**What it is:** Phone numbers that can control the bot

**Format:** Country code + number (no spaces, no +)

**Examples:**
```
USA: 15551234567
UK: 442012345678
India: 919876543210
Multiple: 15551234567,919876543210,442012345678
```

**Where to get:** Your own WhatsApp phone number!

---

## 🆓 Testing for Free - Complete Workflow

### Free Testing Checklist

✅ **What you can do for FREE:**
- Test with up to 1,000 conversations/month
- Use Meta's test phone number
- Full API access
- Test all bot features
- Test with real users
- Use ngrok/localtunnel for local testing
- No credit card required

✅ **Perfect for:**
- Development and testing
- Learning WhatsApp API
- Small projects (<1,000 conversations/month)
- Proof of concept
- Personal projects

⚠️ **Limitations of test number:**
- Can't customize the phone number
- Limited to specific test numbers
- Need to add users manually to test list
- 1,000 conversations/month limit

### Moving to Production (When Ready)

**When you need a production number:**
1. Your own business phone number
2. More than 1,000 conversations/month
3. Professional appearance
4. Custom number

**How to add your own number:**
1. Have a phone number (not currently on WhatsApp)
2. Go to: WhatsApp → Phone Numbers → Add Phone Number
3. Verify with SMS/Call
4. Update PHONE_NUMBER_ID in `.env`

**Cost:** Still FREE for first 1,000 conversations, then ~$0.005-0.009 per conversation

---

## 📊 Quick Reference Card

```
╔═══════════════════════════════════════════════════════════════╗
║                    YOUR CREDENTIALS                           ║
╚═══════════════════════════════════════════════════════════════╝

1. WHATSAPP_TOKEN
   Where: WhatsApp → API Setup → Temporary Access Token
   Format: EAAGZBl0Vy... (long string)
   Expires: 24 hours (temporary) or never (permanent)

2. PHONE_NUMBER_ID  
   Where: WhatsApp → API Setup → Phone Number ID
   Format: 123456789012345 (15 digits)

3. Test WhatsApp Number
   Where: WhatsApp → API Setup → Phone number
   Format: +1 555-025-6789
   Use: Add this to your WhatsApp to test

4. ADMIN_NUMBERS
   Where: Your personal phone number
   Format: 15551234567 (country code + number, no +)

5. WEBHOOK_VERIFY_TOKEN
   Format: verify123 (or any custom string)
   Use: To verify webhook in Meta Console

6. Webhook URL
   Local (ngrok): https://abc123.ngrok-free.app/webhook
   Production: https://your-domain.com/webhook

╔═══════════════════════════════════════════════════════════════╗
║                         COSTS                                 ║
╚═══════════════════════════════════════════════════════════════╝

FREE: 1,000 conversations/month
After: $0.005 - $0.009 per conversation
Perfect for testing: 100% FREE
```

---

## 🐛 Common Issues & Solutions

### Issue 1: Can't find Temporary Access Token

**Solution:**
- Make sure you're in: **WhatsApp** → **Getting Started** or **API Setup**
- Look for "Temporary access token" section
- If not visible, try refreshing the page
- Make sure WhatsApp product is added to your app

### Issue 2: Webhook verification fails

**Solution:**
- Check your bot is running: `npm start`
- Check ngrok is running: `ngrok http 3000`
- Use HTTPS URL (not HTTP)
- Verify token matches in `.env` and Meta Console
- Check URL format: `https://abc123.ngrok.io/webhook`

### Issue 3: Messages not received

**Solution:**
- Verify webhook is configured
- Check "messages" field is subscribed
- Check bot logs for errors
- Make sure you're messaging the test number
- Add your phone to test users list (if required)

### Issue 4: Token expired

**Solution:**
- Temporary token expires in 24 hours
- Create a permanent token (see above)
- Or generate a new temporary token daily

### Issue 5: Can't send messages

**Solution:**
- Check WHATSAPP_TOKEN is correct
- Check PHONE_NUMBER_ID is correct
- Verify token hasn't expired
- Check API permissions

---

## ✅ Final Setup Summary

### You Need (5 minutes total):

1. ✅ Meta Developer Account (Free)
2. ✅ Create App (2 min)
3. ✅ Add WhatsApp Product (1 min)
4. ✅ Copy 2 credentials: Token + Phone ID (30 sec)
5. ✅ Format your phone number (30 sec)
6. ✅ Configure .env file (1 min)
7. ✅ Start bot + ngrok (1 min)
8. ✅ Configure webhook (2 min)
9. ✅ Test! (30 sec)

**Total time:** ~10 minutes
**Total cost:** $0 (FREE!)

---

## 🎉 You're Ready!

Follow the steps above and you'll have everything configured in ~10 minutes!

**Next:** After getting your credentials, update `.env` and run `npm start`

**Questions?** Check troubleshooting section above.

---

**Last updated:** January 17, 2026
