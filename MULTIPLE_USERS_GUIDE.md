# 👥 Adding Multiple Users to CROUS Room Checker

This guide shows you how to add friends, family, or roommates to receive CROUS room notifications.

## 🔧 **Method 1: Multiple Chat IDs (Recommended)**

### **For Local Development (config.json):**

Update your `config.json` to include multiple chat IDs:

```json
{
    "telegram": {
        "bot_token": "8465766993:AAGpWR_LPuCFtEq3RdmvO733x3O7bOAwg2A",
        "chat_ids": [
            "7391538221",           // Your chat ID
            "FRIEND_CHAT_ID_1",     // Friend 1's chat ID
            "FRIEND_CHAT_ID_2"      // Friend 2's chat ID
        ]
    },
    "settings": {
        "check_interval_minutes": 5,
        "use_simulation": false,
        "log_level": "INFO"
    }
}
```

### **For Render Deployment (Environment Variables):**

In your Render dashboard, update the environment variables:

**Option A: Use the new TELEGRAM_CHAT_IDS variable:**
- **Key**: `TELEGRAM_CHAT_IDS`
- **Value**: `7391538221,FRIEND_CHAT_ID_1,FRIEND_CHAT_ID_2`
  (comma-separated, no spaces)

**Option B: Keep backward compatibility:**
- Keep your existing `TELEGRAM_CHAT_ID` for yourself
- The bot will still work with single chat ID

## 🆔 **How to Get Someone's Chat ID**

### **Step 1: They Start Your Bot**
Each person needs to:
1. **Find your bot**: Search `@KatibCrousBot` on Telegram
2. **Start the bot**: Click "START" 
3. **Send a message**: Type "hello" or any message

### **Step 2: Get Their Chat ID**

Use the helper script to find their chat ID:

```powershell
python get_chat_id.py
```

Or use this manual method:

1. **Get bot updates**: Visit this URL in browser (replace with your bot token):
   ```
   https://api.telegram.org/bot8465766993:AAGpWR_LPuCFtEq3RdmvO733x3O7bOAwg2A/getUpdates
   ```

2. **Find their message**: Look for their message in the JSON response

3. **Extract chat ID**: Find `"chat":{"id":123456789}` - that's their chat ID

### **Step 3: Alternative - Use @userinfobot**
Each person can:
1. **Search**: `@userinfobot` on Telegram
2. **Send message**: Any message to the bot
3. **Get ID**: Bot replies with their user information including ID

## 👥 **Method 2: Telegram Group (Alternative)**

Create a Telegram group to notify everyone at once:

### **Steps:**
1. **Create group**: In Telegram, create a new group
2. **Add people**: Add friends who want notifications
3. **Add your bot**: Add `@KatibCrousBot` to the group
4. **Get group ID**: Use the same method as getting chat ID
5. **Update config**: Use the group ID instead of individual chat IDs

### **Pros:**
- ✅ Easy to manage
- ✅ People can join/leave themselves
- ✅ Group chat for coordination

### **Cons:**
- ❌ All notifications go to group chat
- ❌ Less privacy than direct messages

## 🤖 **Method 3: Self-Service Bot Commands (Advanced)**

For a more advanced setup, you can modify the bot to handle commands:

### **Features:**
- `/start` - Subscribe to notifications
- `/stop` - Unsubscribe from notifications  
- `/status` - Check subscription status
- `/help` - Show available commands

This requires more complex code modifications. Let me know if you want me to implement this!

## 🔄 **Updating Your Deployment**

### **For Local Testing:**
1. **Update `config.json`** with new chat IDs
2. **Test locally**: `python crous-checker.py`
3. **Verify**: All users should receive startup notification

### **For Render Deployment:**
1. **Update environment variables** in Render dashboard
2. **Service restarts automatically** when environment variables change
3. **Check logs** to confirm multiple recipients
4. **Verify**: All users should receive startup notification

## 📝 **Example Configurations**

### **For 3 Users (Local config.json):**
```json
{
    "telegram": {
        "bot_token": "8465766993:AAGpWR_LPuCFtEq3RdmvO733x3O7bOAwg2A",
        "chat_ids": [
            "7391538221",     // You
            "987654321",      // Friend 1  
            "123456789"       // Friend 2
        ]
    },
    "settings": {
        "check_interval_minutes": 5,
        "use_simulation": false,
        "log_level": "INFO"
    }
}
```

### **For 3 Users (Render Environment Variable):**
```
TELEGRAM_CHAT_IDS = 7391538221,987654321,123456789
```

## 🔍 **Testing Multiple Users**

### **Quick Test:**
1. **Update configuration** with multiple chat IDs
2. **Run**: `python test_setup.py` 
3. **Check**: All users should receive test message
4. **Verify logs**: Should show "Message sent to X/Y recipients"

### **Expected Log Output:**
```
INFO - Loading configuration from config.json
INFO - Bot initialized successfully!
INFO - Recipients: 3 user(s)
INFO - Telegram notification sent successfully to 7391538221
INFO - Telegram notification sent successfully to 987654321  
INFO - Telegram notification sent successfully to 123456789
INFO - Message sent to 3/3 recipients
```

## ⚠️ **Important Notes**

### **Privacy:**
- **Each person gets individual notifications** (not group messages)
- **People don't see each other's chat IDs**
- **Bot token is shared** but only you control the service

### **Bot Limitations:**
- **All users must start the bot first** by sending `/start`
- **Bot can only message users who initiated contact**
- **Users can block the bot** to stop receiving messages

### **Telegram Rate Limits:**
- **30 messages per second** to different users (more than enough)
- **No practical limit** for your use case

## 🎯 **Recommended Setup**

**For close friends/family (2-5 people):**
- ✅ Use **Method 1** (Multiple Chat IDs)
- ✅ Individual notifications
- ✅ Privacy maintained

**For larger groups (5+ people):**
- ✅ Use **Method 2** (Telegram Group)
- ✅ Easier management
- ✅ People can self-manage membership

**For public/open access:**
- ✅ Use **Method 3** (Bot Commands)
- ✅ Self-service subscription
- ✅ No manual chat ID management

---

## 🚀 **Quick Start for Friends**

Send this to friends who want notifications:

> **"Hey! I set up a bot that monitors CROUS room availability in Rennes. To get notifications:**
> 
> **1. Open Telegram and search: `@KatibCrousBot`**
> **2. Click START and send any message**  
> **3. Send me your Chat ID (I'll help you get it)**
> **4. I'll add you to the notification list!**
> 
> **You'll get instant alerts when rooms become available! 🏠"**

Your updated bot now supports multiple users! 👥✨
