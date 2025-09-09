# CROUS Room Availability Checker

A Python script that monitors CROUS housing website for available rooms and sends Telegram notifications when rooms become available.

## Features

- 🏠 Monitors CROUS room availability
- 📱 Sends instant Telegram notifications
- ⏰ Configurable check intervals
- 🎮 Simulation mode for testing
- 📝 Comprehensive logging
- 🔄 Prevents duplicate notifications

## Quick Start

### 1. Set up Telegram Bot

#### Create a Bot with BotFather:

1. Open Telegram and search for `@BotFather`
2. Start a chat and send `/newbot`
3. Choose a name for your bot (e.g., "CROUS Room Checker")
4. Choose a username ending in "bot" (e.g., "crous_room_checker_bot")
5. Save the bot token provided (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### Get Your Chat ID:

1. Search for `@userinfobot` on Telegram
2. Start a chat and send any message
3. The bot will reply with your user information including your Chat ID
4. Save the Chat ID (format: `123456789`)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Script

1. Copy the sample configuration:

   ```bash
   copy config_sample.json config.json
   ```

2. Edit `config.json` with your credentials:
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

### 4. Run the Script

```bash
python crous-checker.py
```

## Configuration Options

- `check_interval_minutes`: How often to check for rooms (default: 5 minutes)
- `use_simulation`: Set to `true` for testing, `false` for real checking
- `log_level`: Logging verbosity (DEBUG, INFO, WARNING, ERROR)

## Real Website Integration

To integrate with the actual CROUS website:

1. Set `use_simulation` to `false` in config.json
2. Update the `crous_url` in the script to the actual CROUS housing URL
3. Modify the `check_availability_real()` function to parse the actual website structure
4. Install BeautifulSoup for web scraping:
   ```bash
   pip install beautifulsoup4
   ```

## Logs

The script creates a `crous_checker.log` file with detailed information about:

- Check attempts
- Rooms found
- Notifications sent
- Errors encountered

## Stopping the Script

Press `Ctrl+C` to stop the script gracefully. It will send a shutdown notification to Telegram.

## Troubleshooting

### Common Issues:

1. **"config.json not found"**

   - Copy `config_sample.json` to `config.json` and fill in your credentials

2. **"Failed to send Telegram message"**

   - Check your bot token and chat ID
   - Ensure you've started a conversation with your bot

3. **"Error checking CROUS website"**
   - Check your internet connection
   - The website might be temporarily unavailable

### Testing Your Setup:

1. Run the script with simulation mode enabled
2. Check that you receive the startup notification
3. Wait for a few check cycles to see room notifications

## License

This project is for educational purposes. Please respect the CROUS website's terms of service when using real web scraping.
