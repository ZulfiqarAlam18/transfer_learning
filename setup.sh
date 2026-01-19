#!/bin/bash

# WhatsApp Bot Setup Script
# This script helps you set up your WhatsApp bot quickly

echo "=========================================="
echo "  WhatsApp Limit Bot - Setup Script"
echo "=========================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed!"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version is too old (found v$NODE_VERSION)"
    echo "Please upgrade to Node.js 18+ from https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js $(node -v) detected"
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists!"
    read -p "Do you want to overwrite it? (y/N): " OVERWRITE
    if [ "$OVERWRITE" != "y" ] && [ "$OVERWRITE" != "Y" ]; then
        echo "Skipping .env creation..."
    else
        cp .env.example .env
        echo "✅ Created new .env file from template"
    fi
else
    cp .env.example .env
    echo "✅ Created .env file from template"
fi

echo ""
echo "=========================================="
echo "  Configuration Required"
echo "=========================================="
echo ""
echo "You need to configure your .env file with:"
echo ""
echo "1. WHATSAPP_TOKEN - Get from Meta Developer Console"
echo "   https://developers.facebook.com/"
echo ""
echo "2. PHONE_NUMBER_ID - Your WhatsApp Business phone number ID"
echo ""
echo "3. ADMIN_NUMBERS - Phone numbers of admins (with country code)"
echo "   Example: 15551234567,15557654321"
echo ""

read -p "Do you want to edit .env now? (Y/n): " EDIT_ENV
if [ "$EDIT_ENV" != "n" ] && [ "$EDIT_ENV" != "N" ]; then
    # Try different editors
    if command -v nano &> /dev/null; then
        nano .env
    elif command -v vim &> /dev/null; then
        vim .env
    elif command -v vi &> /dev/null; then
        vi .env
    else
        echo "⚠️  No text editor found. Please edit .env manually."
    fi
fi

echo ""
echo "=========================================="
echo "  Installing Dependencies"
echo "=========================================="
echo ""

npm install

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Dependencies installed successfully!"
else
    echo ""
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "🎉 Your WhatsApp bot is ready to run!"
echo ""
echo "Next steps:"
echo ""
echo "1. Make sure .env is configured with your credentials"
echo "2. Start the bot: npm start"
echo "3. Open dashboard: http://localhost:3000/dashboard"
echo "4. Configure webhook in Meta Developer Console"
echo ""
echo "📚 Read QUICKSTART.md for detailed instructions"
echo "🚀 Read DEPLOYMENT.md to deploy to production"
echo ""
echo "=========================================="
