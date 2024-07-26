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
    text = """
    **Commands available in the bot:**
    
    **1.** __/generate\_card__ - Generate a new roleplay card. The bot will provide you with a new card with a unique situation to practice on
    **2.** __/play\_game__ - Start roleplay. You will receive a card and will be able to record voice messages while playing the role of a doctor
    """
    # **3.** __/info__ - Get materials for training. The bot will provide you with a list of available materials to prepare for the OET exam
    # Show last 5 cards. The bot will show you the last 5 cards you generated
    # Rate a card. You can rate the card from 1 to 5 points
    # Show top 5 cards. The bot will show you the top 5 highest rated cards
    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_on_help_kb(),
    )
