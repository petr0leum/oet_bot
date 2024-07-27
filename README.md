# OET Preparation Bot

This is a Telegram bot designed to help users prepare for the Occupational English Test (OET) by generating new scenario cards (**MEDICINE**) and providing practice through role-playing games with an AI interlocutor. Additionally, it offers approximate evaluations of your dialogue with the bot.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Generate Card: Use the /generate_card command to create new OET scenario cards. You can provide feedback on the generated cards, and the bot will learn from your preferences. (Only **MEDICINE**)\\
- Play Game: Use the /play_game command to start a role-playing game where the AI Bot acts as your interlocutor. The conversation happens entirely through voice messages, simulating the OET Speaking exam. At the end of the game, you can evaluate the dialogue.\\
- Show Liked Cards: Use the /show_liked_cards command to quickly view a few of your recently liked cards.\\
- Evaluate the dialogue based on predefined criteria.\\

### Available Commands
* __/start__: Start the bot and receive a welcome message.
* __/help__: Get a list of available commands and their descriptions.
* __/generate_card__ - Generate new OET scenario cards. (Only **MEDICINE**)
* __/play_game__ - Start a role-playing game to practice OET Speaking.
* __/show_liked_cards__: View your recently liked OET scenario cards.
* __/cancel__ - Cancel the current operation.

Happy studying and good luck on your exam! 🍀

## Installation

### Prerequisites

- Python 3.10.11
- Telegram Bot API token
- OpenAI API token
- Whisper for speech recognition

### Clone the Repository

```bash
git clone https://github.com/petr0leum/oet_helper
cd oet_role_play_bot
```

### Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configuration
Create a ```.env``` file in the root directory of the project and add the following environment variables:
```bash
TELEGRAM_API_TOKEN=your-telegram-bot-api-token
OPENAI_API_TOKEN=your-openai-api-token
```

### Usage
#### Running the Bot
```bash
python main.py
```

## Project Structure

```plaintext
.
├── config.py                 # Configuration settings
├── database.py               # SQLite database interactions
├── llms_content.py           # Prompts and content for the language model
├── main.py                   # Main entry point of the bot
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── keyboards                 # Keyboards for Telegram bot
│   ├── __init__.py
│   ├── common_keyboards.py   # Common keyboards for different states
│   ├── card_keyboards.py     # Keyboards specific to card generation
│   └── game_keyboards.py     # Keyboards specific to the game
├── routers                   # Handlers and commands
│   ├── __init__.py
│   ├── callback_handlers
│   │   ├── __init__.py
│   │   ├── cards_view_cbh.py # Handler for viewing and managing liked cards
│   ├── commands
│   │   ├── __init__.py
│   │   ├── base_commands.py  # Standart commands
│   │   ├── generate_card.py  # Command for generating cards
│   │   └── role_play_game.py # Command for role play game
│   └── handlers
│       ├── __init__.py
│       ├── card_handlers.py  # Handlers for the card generation interactions
│       └── game_handlers.py  # Handlers for the game interactions
├── utils                     # Utility functions
│   ├── __init__.py
│   ├── audio_utils.py        # Audio processing utilities
│   ├── format_utils.py       # Formatting utilities
│   └── openai_utils.py       # OpenAI API interaction utilities
└── data
    └── audio_storage         # Directory for storing audio files    
```

### Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request. We welcome all improvements and suggestions.

### License
This project is licensed under the MIT License. See the LICENSE file for more information.
```
Feel free to modify these texts according to your specific requirements and preferences.
```