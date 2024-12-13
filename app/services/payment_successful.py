from app.bot.utils import TelegramError
from app.services.db import DataBase, DatabaseError
from aiogram import Bot

async def payment_success(bot: Bot, database: DataBase, update_type: str, invoice_id: int) -> None:
    if update_type == "invoice_paid":
        try:
            result = await database.get_orderdata(invoice_id)
            if result[1] == 'chatgpt':
                await database.update_chatgpt(result[0], invoice_id)
                await bot.send_message(result[0], "✅You have received 100000 ChatGPT tokens!")
            elif result[1] == 'dall_e':
                await database.update_dalle(result[0], invoice_id)
                await bot.send_message(result[0], "✅You have received 50 DALL·E image generations!")
            elif result[1] == 'stable':
                await database.update_stable(result[0], invoice_id)
                await bot.send_message(result[0], "✅You have received 50 Stable Diffusion image generations!")
        except DatabaseError:
            raise DatabaseError
        except Exception as e:
            err = TelegramError(str(e))
            err.output()
            raise err