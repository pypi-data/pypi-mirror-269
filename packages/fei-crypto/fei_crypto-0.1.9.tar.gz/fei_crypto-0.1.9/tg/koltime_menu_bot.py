import base64
import io
import os
import dotenv
import redis
from tg import config
from tg.utils import clean_session_files, get_command_prefix
from tg.parse import proxy_parse_tuple
from telethon import TelegramClient, events, functions, types, Button
from telethon.tl.types import MessageMediaPhoto, Photo, DocumentAttributeFilename, DocumentAttributeImageSize

PINDAO_TEXT = '📚频道列表'
XUEXI_TEXT = '🍿学习视频'
SHIYONG_TEXT = '🐝试用频道'
VIP_TEXT = '💎购买会员'
FANYONG_TEXT = '🍕返佣链接'
QUN_TEXT = '🙌社群链接'
FAQ_TEXT = '🤔疑问解答'
ENV_PREFIX = 'TG_KOLTIME_MENU_BOT_'

score_dict: dict[float, str] = {
    1.0: '中文博主',
    2.0: '提阿非罗',
    3.0: '英文博主',
    4.0: 'koltime',
    5.0: '其他',
}

r: redis.client.Redis | None = None


def koltime_menu_bot(env_path: str = '.env') -> None:
    clean_session_files()
    dotenv.load_dotenv(env_path)
    global r
    if r is None:
        r = redis.Redis(
            host=os.getenv(f'{ENV_PREFIX}REDIS_HOST'),
            port=os.getenv(f'{ENV_PREFIX}REDIS_PORT'),
            password=os.getenv(f'{ENV_PREFIX}REDIS_PASSWORD'),
            db=0)

    proxy = os.getenv(f'{ENV_PREFIX}PROXY')
    token = os.getenv(f'{ENV_PREFIX}TOKEN')
    api_id = os.getenv(f'{ENV_PREFIX}API_ID')
    api_hash = os.getenv(f'{ENV_PREFIX}API_HASH')

    client = TelegramClient(
        "bot",
        int(api_id),
        api_hash,
        proxy=proxy_parse_tuple(proxy)
    )

    client.start(bot_token=token)

    with client:
        client.loop.run_until_complete(start(client))


async def start(client: TelegramClient) -> None:
    me = await client.get_me()
    print(f'🛩️usd_id:{me.id}')
    print(f'🛩️usename:{me.username}')
    config.is_bot = await client.is_bot()
    print(f'🛩️is_bot:{config.is_bot}')

    command_events = get_command_events()
    ALL_EVENTS.update(command_events)

    for key, val in ALL_EVENTS.items():
        client.add_event_handler(*val)

    await client(
        functions.bots.SetBotCommandsRequest(
            scope=types.BotCommandScopeDefault(),
            lang_code="en",
            commands=[
                types.BotCommand(command=key, description=value)
                for key, value in COMMANDS.items()
            ],
        )
    )

    await client.run_until_disconnected()


async def start_command_handler(event):
    keyboard = [
        [
            Button.text(PINDAO_TEXT),
            Button.text(XUEXI_TEXT),
        ],
        [
            Button.text(SHIYONG_TEXT),
            Button.text(VIP_TEXT),
        ],
        [
            Button.text(FANYONG_TEXT),
            Button.text(QUN_TEXT),
        ], [
            Button.text(FAQ_TEXT)
        ]
    ]

    description = r.hget('koltime_menu_bot', 'description')
    caption = 'welcome!'
    if isinstance(description, bytes):
        caption = description.decode()
    photo = r.hget('koltime_menu_bot', 'pic_base64')
    if isinstance(photo, bytes):
        # await event.client.send_file(
        #     event.chat_id,
        #     photo.decode(),
        #     attributes=(DocumentAttributeFilename("koltime.png"),),
        #     caption=caption,
        #     buttons=keyboard)
        file = io.BytesIO(base64.b64decode(photo.decode()))
        file.name = 'koltime.png'
        await event.respond(
            file=file,
            attributes=(DocumentAttributeFilename("koltime.png"),),
            message=caption,
            buttons=keyboard,
        )
    else:
        await event.respond(
            text=caption,
            buttons=keyboard,
        )


async def help_command_handler(event):
    await event.respond("help")


async def faq(event) -> None:
    await event.respond("🍄开发中...")


async def pindao(event) -> None:
    pindao_dict: dict[str, list[tuple[str]]] = {}
    channels = r.zrange("koltime_menu_bot_channels", 0, 1000, withscores=True)
    for item in channels:
        pindao_list = pindao_dict.setdefault(score_dict[item[1]], [])
        pindao_list.append(tuple(item[0].decode().split(',')))

    text = f"{PINDAO_TEXT}👇\n"
    for k, v in pindao_dict.items():
        text += f'【{k}】\n'
        for v_item in v:
            text += f'[{v_item[1]}]({v_item[2]})\n'

        text += '\n'

    # text = text.replace('-', '\\-')

    await event.respond(text, parse_mode='md')


async def xuexi(event) -> None:
    await event.respond("🍄开发中...")


async def shiyong(event) -> None:
    await event.respond("🍄开发中...")


async def vip(event) -> None:
    await event.respond("🍄开发中...")


async def fanyong(event) -> None:
    await event.respond("🍄开发中...")


async def qun(event) -> None:
    await event.respond("🍄开发中...")


ALL_EVENTS = {
    "faq": (faq, events.NewMessage(pattern=FAQ_TEXT)),
    "pindao": (pindao, events.NewMessage(pattern=PINDAO_TEXT)),
    "xuexi": (xuexi, events.NewMessage(pattern=XUEXI_TEXT)),
    "shiyong": (shiyong, events.NewMessage(pattern=SHIYONG_TEXT)),
    "vip": (vip, events.NewMessage(pattern=VIP_TEXT)),
    "fanyong": (fanyong, events.NewMessage(pattern=FANYONG_TEXT)),
    "qun": (qun, events.NewMessage(pattern=QUN_TEXT)),
}

COMMANDS = {
    "start": "启动菜单",
    "help": "帮助菜单",
}


def get_command_events():
    _ = get_command_prefix()

    command_events = {
        "start": (start_command_handler, events.NewMessage(pattern=f"{_}start")),
        "help": (help_command_handler, events.NewMessage(pattern=f"{_}help")),
    }

    return command_events


if __name__ == '__main__':
    koltime_menu_bot("d:/.env")
