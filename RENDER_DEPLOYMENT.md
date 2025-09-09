# 🚀 Deploy CROUS Room Checker to Render

This guide will help you deploy your CROUS room checker to Render for 24/7 monitoring without keeping your computer running.

## 🌟 Why Render?

- ✅ **Free tier available** (500 hours/month)
- ✅ **Auto-deploys from GitHub**
- ✅ **Environment variables** for secure config
- ✅ **Always-on services**
- ✅ **Easy setup** with GitHub integration

## 📋 Prerequisites

1. **GitHub repository** with your project (✅ Done)
2. **Render account** (free at https://render.com)
3. **Telegram bot credentials** (✅ You have these)

## 🔧 Step-by-Step Deployment

### 1. Prepare Your Repository

First, let's update your repository with the cloud-ready files:

```powershell
# Switch to cloud version
copy crous-checker-cloud.py crous-checker.py

# Add new files to Git
git add .
git commit -m "Add Render deployment files and cloud-ready version"
git push origin main
```

### 2. Create Render Account

1. **Go to**: https://render.com
2. **Click "Get Started"**
3. **Sign up with GitHub** (recommended for easy integration)
4. **Authorize Render** to access your repositories

### 3. Create New Web Service

1. **Click "New +"** in Render dashboard
2. **Select "Web Service"**
3. **Connect your repository**: `crous-room-checker`
4. **Configure the service**:

#### Basic Settings:
- **Name**: `crous-room-checker`
- **Environment**: `Python 3`
- **Region**: `Frankfurt` (closest to France)
- **Branch**: `main`

#### Build Settings:
- **Root Directory**: Leave empty
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python crous-checker.py`

#### Advanced Settings:
- **Auto-Deploy**: `Yes` (deploys automatically on GitHub push)

### 4. Set Environment Variables

In Render dashboard, go to your service → **Environment** tab:

**Add these environment variables:**

| Key | Value |
|-----|-------|
| `TELEGRAM_BOT_TOKEN` | `8465766993:AAGpWR_LPuCFtEq3RdmvO733x3O7bOAwg2A` |
| `TELEGRAM_CHAT_ID` | `7391538221` |
| `CHECK_INTERVAL_MINUTES` | `5` |
| `PYTHON_VERSION` | `3.11.0` |

⚠️ **Important**: Use environment variables instead of config.json for security!

### 5. Deploy Your Service

1. **Click "Create Web Service"**
2. **Wait for deployment** (takes 2-5 minutes)
3. **Check logs** for any errors
4. **You should receive a startup notification** on Telegram

## 📊 Service Configuration

### Render Service Files Created:

```
├── runtime.txt              # Python version specification
├── Procfile                 # How to start the service
├── crous-checker-cloud.py   # Cloud-optimized version
└── requirements.txt         # Dependencies (existing)
```

### Environment Variables Explained:

- `TELEGRAM_BOT_TOKEN`: Your bot's API token
- `TELEGRAM_CHAT_ID`: Your Telegram user ID
- `CHECK_INTERVAL_MINUTES`: How often to check (5 minutes recommended)
- `PYTHON_VERSION`: Python runtime version

## 🔍 Monitoring Your Service

### 1. Render Dashboard
- **View logs**: See real-time application logs
- **Check metrics**: CPU, memory usage
- **Service status**: Running/stopped/error states

### 2. Telegram Notifications
- **Startup message**: Confirms service is running
- **Room alerts**: When accommodations are found
- **Error messages**: If something goes wrong

### 3. Log Messages to Watch For:
```
✅ "Bot initialized successfully!"
✅ "Checking CROUS room availability..."
✅ "Successfully found X rooms on CROUS website"
❌ "Error checking CROUS website"
```

## 💰 Render Free Tier Limits

- **500 hours/month** of service runtime
- **Service sleeps after 15 minutes** of inactivity
- **Automatic wake-up** when needed
- **750MB RAM** limit
- **No persistent disk** storage

## 🔧 Troubleshooting

### Common Issues:

#### 1. Service Won't Start
**Solution**: Check environment variables are set correctly

#### 2. No Telegram Notifications
**Solution**: Verify bot token and chat ID in environment variables

#### 3. Service Sleeps Too Often
**Solution**: Consider upgrading to paid plan for always-on service

#### 4. Python Version Error
**Solution**: Ensure `runtime.txt` specifies Python 3.11.0

### Debug Steps:

1. **Check Render logs** for error messages
2. **Verify environment variables** are set
3. **Test bot credentials** manually
4. **Check GitHub repository** is up to date

## ⚡ Advanced Features

### Auto-Wake Service
```python
# Add to your script to prevent sleeping
import os
import requests

def keep_alive():
    """Ping service to prevent sleeping"""
    service_url = os.getenv('RENDER_EXTERNAL_URL')
    if service_url:
        try:
            requests.get(f"{service_url}/health", timeout=5)
        except:
            pass

# Call every few minutes
```

### Custom Domain (Paid Plans)
- Add custom domain in Render dashboard
- Configure DNS records
- Automatic SSL certificates

## 🚀 Going Live

### Final Checklist:

- ✅ **Repository updated** with cloud files
- ✅ **Render service created** and configured
- ✅ **Environment variables set** correctly
- ✅ **Service deployed** successfully
- ✅ **Startup notification received** on Telegram
- ✅ **Logs show successful** CROUS checks

### Expected Behavior:

1. **Service starts** and sends Telegram notification
2. **Checks CROUS website** every 5 minutes
3. **Sends room alerts** when accommodations found
4. **Logs all activity** in Render dashboard
5. **Runs 24/7** within free tier limits

## 📱 Managing Your Service

### Update Configuration:
- **Change environment variables** in Render dashboard
- **Service restarts automatically** when changed

### Update Code:
- **Push to GitHub** → **Auto-deploys to Render**
- **Check logs** for successful deployment

### Stop Service:
- **Suspend in Render dashboard**
- **Receives shutdown notification** on Telegram

---

## 🎉 Congratulations!

Your CROUS room checker is now running 24/7 in the cloud! 

**Service URL**: `https://crous-room-checker-[random].onrender.com`

You'll receive notifications whenever rooms become available in Rennes, without keeping your computer running! 🏠✨
