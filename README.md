# dracuzz : AI TOXICITY DETECTION DISCORD BOT

![License](https://img.shields.io/badge/license-MIT-blue.svg)

Toxicity Scanner Discord Bot is a Python-based bot that uses Google's Perspective API to scan messages in a Discord server for toxic content. The bot can take various actions such as deleting toxic messages, warning users, or even banning them based on the level of toxicity detected.

## Features

- **Real-time Toxicity Detection**: Scans messages in real-time for toxic content using Google's Perspective API.
- **Configurable Actions**: Take actions such as deleting messages, warning users, muting users, or banning users based on the detected toxicity level.
- **Customizable Settings**: Adjust toxicity thresholds and configure which actions to take for different levels of toxicity.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Aviralansh/dracuzz.git
    cd dracuzz
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables:
    - Create a `.env` file in the project root directory and add your Discord bot token and Perspective API key:
    ```plaintext
    DISCORD_TOKEN=your_discord_token_here
    PERSPECTIVE_API_KEY=your_perspective_api_key_here
    ```

## Usage

1. Run the bot:
    ```bash
    python bot.py
    ```

2. Invite the bot to your Discord server using the OAuth2 URL generated for your bot.


## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Discord.py](https://github.com/Rapptz/discord.py) - Python library for interacting with the Discord API.
- [Perspective API](https://www.perspectiveapi.com) - API for detecting toxic content.
