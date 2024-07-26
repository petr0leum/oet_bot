# OET Role Play Bot

This is a Telegram bot designed to help users prepare for the Occupational English Test (OET) by generating role play scenarios. Users can generate cards, play a role play game, and evaluate their performance.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Generate OET role play scenarios.
- Save and fetch user-preferred cards.
- Play a role play game with voice interactions.
- Evaluate the dialogue based on predefined criteria.
- Manage game states using FSM (Finite State Machine).

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
Create a ```{code}.env``` file in the root directory of the project and add the following environment variables:
```bash
TELEGRAM_API_TOKEN=your-telegram-bot-api-token
OPENAI_API_TOKEN=your-openai-api-token
```

### Usage
#### Running the Bot
```bash
python main.py
```

### Available Commands
__/generate_card__ - Generate a new OET card.
__/play_game__ - Start a role play game.
__/cancel__ - Cancel the current operation.

### Interaction Flow
Generate a Card: Use the __/generate_card__ command to generate a new OET card.
Play a Game: After generating a card, or just use the __/play_game__ command to start the role play game.
Evaluate: Use /get_dialog_text to get the text of the current dialogue and /score to get an evaluation of the dialogue. 

## Project Structure

```plaintext
.
├── config.py                # Configuration settings
├── keyboards                # Keyboards for Telegram bot
│   ├── __init__.py
│   ├── common_keyboards.py  # Common keyboards for different states
│   └── game_keyboards.py    # Keyboards specific to the game
├── llms_content.py          # Prompts and content for the language model
├── main.py                  # Main entry point of the bot
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── routers                  # Handlers and commands
│   ├── __init__.py
│   ├── commands
│   │   ├── __init__.py
│   │   ├── generate_card.py # Command for generating cards
│   │   └── role_play_game.py# Command for role play game
│   └── handlers
│       ├── __init__.py
│       └── game_handlers.py # Handlers for the game interactions
├── utils                    # Utility functions
│   ├── __init__.py
│   ├── audio_utils.py       # Audio processing utilities
│   ├── format_utils.py      # Formatting utilities
│   └── openai_utils.py      # OpenAI API interaction utilities
└── data
    └── audio_storage        # Directory for storing audio files    
```