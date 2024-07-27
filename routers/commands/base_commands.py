from aiogram import F, Router, types
from aiogram.utils import markdown
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command

from keyboards import (
    ButtonText,
    get_on_start_kb,
    get_on_help_kb
)

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        text=markdown.text(
            markdown.text(
                markdown.markdown_decoration.quote("👋 Hi, "),
                markdown.bold(message.from_user.full_name),
                markdown.markdown_decoration.quote("!")
            ),
            markdown.text("Use the buttons below ⬇️"),
            sep="\n"
        ),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=get_on_start_kb(),
    )


@router.message(F.text == ButtonText.HELP)
@router.message(Command("help", prefix="!/"))
async def handle_help(message: types.Message):
    text = markdown.text(
        markdown.markdown_decoration.quote("Hello! 👋 I'm here to help you prepare for the OET exam."),
        markdown.markdown_decoration.quote("Here's what I can do for you:"),
        '',
        markdown.bold("📝 Generate Card"),
        markdown.markdown_decoration.quote("Use /generate_card to create new OET scenario cards."),
        markdown.text(
            markdown.markdown_decoration.quote("You can"),
            markdown.bold("like"), 
            "or",
            markdown.bold("dislike"),
            markdown.markdown_decoration.quote("the generated cards, and the bot will learn your preferences over time."),
            sep=" "
        ),
        '',
        markdown.bold("🎭 Play Game"),
        markdown.markdown_decoration.quote("Use /play_game to start a role-playing game where the AI Bot acts as your interlocutor."),
        markdown.text(
            markdown.markdown_decoration.quote("You'll communicate through"), 
            markdown.bold("voice messages"), 
            markdown.markdown_decoration.quote(", simulating the OET Speaking exam."),
            sep=" "
        ),
        '',
        markdown.bold("💾 Show Liked Cards"),
        markdown.markdown_decoration.quote("Use /show_liked_cards to quickly view your recently liked cards."),
        '', 
        markdown.bold(
            markdown.markdown_decoration.quote("🗙 Cancel the current operation?")
        ),
        markdown.markdown_decoration.quote("Use /cancel command."),
        '',
        markdown.markdown_decoration.quote("Happy studying and good luck on your exam! 🍀"),
        sep='\n'
    )

    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=get_on_help_kb(),
    )
