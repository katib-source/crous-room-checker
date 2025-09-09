# CROUS Room Checker - Complete Setup Guide

## 📋 Table of Contents

1. [Creating a Telegram Bot](#creating-telegram-bot)
2. [Getting Your Chat ID](#getting-chat-id)
3. [Installing and Running the Script](#installation)
4. [Configuration](#configuration)
5. [Testing Your Setup](#testing)
6. [Running the Checker](#running)
7. [Troubleshooting](#troubleshooting)

---

## 🤖 Creating a Telegram Bot {#creating-telegram-bot}

### Step 1: Open Telegram

- Download and install Telegram if you haven't already
- Open Telegram on your phone or computer

### Step 2: Find BotFather

- In the Telegram search bar, type: `@BotFather`
- Click on the official BotFather (it will have a blue checkmark)
- Click "START" to begin the conversation

### Step 3: Create Your Bot

1. Send the command: `/newbot`
2. BotFather will ask for a name for your bot
   - Enter something like: `CROUS Room Checker`
3. BotFather will ask for a username (must end with 'bot')
   - Enter something like: `crous_room_checker_bot`
   - If it's taken, try variations like: `my_crous_checker_bot`

### Step 4: Save Your Bot Token

- BotFather will send you a message with your bot token
- It looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
- **IMPORTANT**: Save this token securely - you'll need it later
- **NEVER** share this token publicly

### Step 5: Start Your Bot

- Click on the link provided by BotFather to open your bot
- Click "START" to activate it

---

## 🆔 Getting Your Chat ID {#getting-chat-id}

### Method 1: Using @userinfobot (Easiest)

1. In Telegram search bar, type: `@userinfobot`
2. Click on the bot and start a conversation
3. Send any message (like "hi")
4. The bot will reply with your user information
5. Copy the "Id" number (it looks like: `123456789`)

### Method 2: Using @RawDataBot

1. Search for `@RawDataBot` in Telegram
2. Start the bot and send any message
3. Look for `"id": 123456789` in the response
4. Copy that number

### Method 3: Manual Method

1. Send a message to your newly created bot
2. Open this URL in your browser (replace YOUR_BOT_TOKEN):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
3. Look for `"chat":{"id":123456789` in the response
4. Copy that number

---

## 💻 Installing and Running the Script {#installation}

### Prerequisites

- Python 3.7 or higher installed
- Internet connection

### Step 1: Download the Files

Make sure you have all these files in your project folder:

- `crous-checker.py` (main script)
- `requirements.txt` (dependencies)
- `config_sample.json` (configuration template)
- `setup.py` (setup script)
- `test_setup.py` (testing script)

### Step 2: Install Dependencies

Open PowerShell/Command Prompt in your project folder and run:

```powershell
python setup.py
```

Or manually:

```powershell
pip install -r requirements.txt
```

---

## ⚙️ Configuration {#configuration}

### Step 1: Create Configuration File

If not done automatically by setup script:

```powershell
copy config_sample.json config.json
```

### Step 2: Edit Configuration

Open `config.json` in a text editor and replace the placeholder values:

```json
{
  "telegram": {
    "bot_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
    "chat_id": "123456789"
  },
  "settings": {
    "check_interval_minutes": 5,
    "use_simulation": true,
    "log_level": "INFO"
  }
}
```

**Replace:**

- `123456789:ABCdefGHIjklMNOpqrsTUVwxyz` with your actual bot token
- `123456789` with your actual chat ID

### Configuration Options Explained:

- `check_interval_minutes`: How often to check (in minutes)
- `use_simulation`: `true` for testing, `false` for real checking
- `log_level`: Detail level of logs (DEBUG, INFO, WARNING, ERROR)

---

## 🧪 Testing Your Setup {#testing}

### Run the Test Script

```powershell
python test_setup.py
```

This will check:

- ✅ Required packages are installed
- ✅ Configuration file is valid
- ✅ Bot token works
- ✅ Chat ID is correct
- ✅ Test message can be sent

**Expected Output:**

```
🧪 CROUS Room Checker - Test Script
================================================

📦 Testing dependencies...
✅ requests is installed
✅ bs4 is installed
✅ lxml is installed
✅ All dependencies are installed

📋 Testing configuration...
✅ Configuration file is valid

🤖 Testing Telegram bot...
✅ Bot 'Your Bot Name' is accessible
✅ Test message sent successfully!
📱 Check your Telegram to confirm you received the test message.

================================================
🎉 All tests passed! Your setup is ready.
🚀 You can now run: python crous-checker.py
================================================
```

---

## 🚀 Running the Checker {#running}

### Start the Script

```powershell
python crous-checker.py
```

**Expected Output:**

```
🏠 CROUS Room Availability Checker Starting...
==================================================
✅ Bot initialized successfully!
⏰ Check interval: 5 minutes
🎮 Simulation mode: ON
==================================================
```

### What Happens:

1. **Startup Notification**: You'll receive a Telegram message confirming the bot started
2. **Regular Checks**: Every X minutes (as configured), the script checks for rooms
3. **Room Notifications**: When rooms are found, you'll get detailed Telegram messages
4. **Logging**: All activity is logged to `crous_checker.log`

### Stopping the Script:

Press `Ctrl+C` to stop. You'll receive a shutdown notification on Telegram.

---

## 🔧 Troubleshooting {#troubleshooting}

### Common Issues and Solutions:

#### ❌ "config.json not found"

**Solution**: Run the setup script or manually copy `config_sample.json` to `config.json`

#### ❌ "Invalid bot token"

**Solutions**:

- Check you copied the entire token from BotFather
- Ensure no extra spaces or characters
- Create a new bot if needed

#### ❌ "Failed to send message"

**Solutions**:

- Verify your chat ID is correct
- Make sure you've started your bot (sent /start)
- Check your internet connection

#### ❌ "Module not found" errors

**Solution**: Install dependencies:

```powershell
pip install requests beautifulsoup4 lxml
```

#### ❌ No test message received

**Solutions**:

- Check your chat ID is correct
- Ensure you started the bot conversation
- Try getting your chat ID again using different method

### Getting Help:

1. **Check the logs**: Look at `crous_checker.log` for detailed error information
2. **Run the test script**: `python test_setup.py` to diagnose issues
3. **Verify configuration**: Double-check your bot token and chat ID

---

## 📝 Advanced Usage

### Switching to Real Website Checking:

1. Set `"use_simulation": false` in `config.json`
2. Update the `crous_url` in the main script to the actual CROUS website
3. Modify the `check_availability_real()` function to parse the real website

### Customizing Check Frequency:

- Modify `"check_interval_minutes"` in `config.json`
- Minimum recommended: 2-3 minutes (to avoid overwhelming the website)

### Running as a Background Service:

On Windows, you can run the script in the background:

```powershell
pythonw crous-checker.py
```

---

## 🔒 Security Notes

- **Never share your bot token**
- **Don't commit config.json to version control**
- **Keep your script updated**
- **Respect website terms of service**

---

## 📞 Support

If you encounter issues:

1. Check this guide thoroughly
2. Run the test script to identify problems
3. Check the log file for error details
4. Ensure all requirements are met

Happy room hunting! 🏠✨
