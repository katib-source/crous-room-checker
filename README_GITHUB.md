# 🏠 CROUS Room Availability Checker

A Python application that monitors CROUS (French student housing) accommodation availability in the Rennes area and sends instant Telegram notifications when rooms become available.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

## ✨ Features

- 🎯 **Geographic Filtering**: Monitors only Rennes area accommodations
- 📱 **Telegram Notifications**: Instant alerts when rooms become available
- ⏰ **Real-time Monitoring**: Configurable check intervals (default: 5 minutes)
- 🚫 **Duplicate Prevention**: Smart tracking to avoid repeated notifications
- 📝 **Comprehensive Logging**: Full activity logs for debugging
- 🛡️ **Error Handling**: Robust error recovery and network resilience
- ⚙️ **Easy Configuration**: Simple JSON configuration file

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Internet connection
- Telegram account

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/crous-room-checker.git
cd crous-room-checker
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or use the automated setup:

```bash
python setup.py
```

### 3. Set Up Telegram Bot

#### Create a Bot:
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the instructions
3. Save your bot token (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### Get Your Chat ID:
1. Search for `@userinfobot` on Telegram
2. Start a chat and send any message
3. Copy your Chat ID (format: `123456789`)

### 4. Configure the Application

```bash
cp config_sample.json config.json
```

Edit `config.json` with your credentials:

```json
{
    "telegram": {
        "bot_token": "YOUR_BOT_TOKEN_HERE",
        "chat_id": "YOUR_CHAT_ID_HERE"
    },
    "settings": {
        "check_interval_minutes": 5,
        "use_simulation": false,
        "log_level": "INFO"
    }
}
```

### 5. Test Your Setup

```bash
python test_setup.py
```

### 6. Run the Application

```bash
python crous-checker.py
```

## 📁 Project Structure

```
crous-room-checker/
├── crous-checker.py          # Main application
├── config_sample.json       # Configuration template
├── requirements.txt         # Python dependencies
├── setup.py                # Automated setup script
├── test_setup.py           # Setup validation
├── test_scraping.py        # Scraping functionality test
├── README.md               # This file
├── SETUP_GUIDE.md          # Detailed setup instructions
└── .gitignore              # Git ignore rules
```

## ⚙️ Configuration Options

- `check_interval_minutes`: How often to check for rooms (default: 5)
- `use_simulation`: Set to `true` for testing, `false` for real monitoring
- `log_level`: Logging detail level (DEBUG, INFO, WARNING, ERROR)

## 📱 Notification Format

When rooms are found, you'll receive notifications like:

```
🏠 CROUS Rennes Area - 3 Rooms Available!

Room 1:
📍 Campus de Beaulieu
🏡 Studio
💰 285€
🆔 CROUS_RENNES_1234

Room 2:
📍 Centre-ville
🏡 T1
💰 320€
🆔 CROUS_RENNES_5678

📊 Total: 3 rooms found
⏰ 14:30:25
🔗 View all on CROUS
```

## 🧪 Testing

Run the test suite to verify everything is working:

```bash
# Test complete setup
python test_setup.py

# Test web scraping functionality
python test_scraping.py

# Test Rennes-specific filtering
python test_rennes_url.py
```

## 🔧 Troubleshooting

### Common Issues:

1. **Bot token errors**: Verify your token with BotFather
2. **Chat ID issues**: Use `python get_chat_id.py` to get the correct ID
3. **No notifications**: Check `crous_checker.log` for detailed error information
4. **Network errors**: The script handles temporary connectivity issues automatically

### Debug Mode:

Set `"log_level": "DEBUG"` in config.json for detailed logging.

## 📝 Logs

The application creates detailed logs in `crous_checker.log` including:
- Check attempts and results
- Rooms found and notifications sent
- Error messages and recovery attempts
- Performance metrics

## 🛑 Stopping the Application

Press `Ctrl+C` to stop the monitoring. The application will send a shutdown notification.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚠️ Important Notes

- **Respect CROUS website**: Don't set check intervals below 2-3 minutes
- **Keep credentials secure**: Never commit your `config.json` file
- **Terms of service**: Ensure compliance with CROUS website terms
- **Educational purpose**: This tool is for educational and personal use

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- CROUS for providing student housing services
- Telegram Bot API for notifications
- BeautifulSoup for web scraping capabilities

## 📞 Support

If you encounter issues:

1. Check the [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions
2. Run `python test_setup.py` to diagnose problems
3. Check the log file for error details
4. Open an issue on GitHub

---

**Happy room hunting! 🏠✨**
