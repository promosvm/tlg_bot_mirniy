import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from config_data.config import Config, load_config
from services.auto_delete import (AutoDeleteMiddleware,
                                  DeleteIncomingMiddleware,
                                  configure as configure_auto_delete)
from handlers import (main_handlers,
                      other_handlers,
                      get_weather,
                      interesting_places,
                      local_cuisene,
                      souvenirs,
                      transport,
                      hotel,
                      rest,
                      sport,
                      emergency,
                      analitic
                      )

# from keyboards.main_menu import set_main_menu

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()
    configure_auto_delete(config.auto_delete.after_seconds,
                          config.auto_delete.user_messages,
                          config.auto_delete.replace_messages)

    # Инициализируем бот и диспетчер
    session = AiohttpSession()
    session.middleware.register(AutoDeleteMiddleware())
    bot = Bot(token=config.tg_bot.token,
              session=session,
              default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    dp.message.middleware.register(DeleteIncomingMiddleware())
    dp.callback_query.middleware.register(DeleteIncomingMiddleware())

    # # Настраиваем главное меню бота
    # await set_main_menu(bot)

    # Регистриуем
    #  роутеры в диспетчере
    dp.include_router(analitic.router)
    dp.include_router(main_handlers.router)
    dp.include_router(transport.router)
    dp.include_router(interesting_places.router)
    dp.include_router(get_weather.router)
    dp.include_router(souvenirs.router)
    dp.include_router(hotel.router)
    dp.include_router(rest.router)
    dp.include_router(other_handlers.router)
    dp.include_router(sport.router)
    dp.include_router(local_cuisene.router)
    dp.include_router(emergency.router)


    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())
