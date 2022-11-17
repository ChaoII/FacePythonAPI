from base.config import settings
from tortoise import Tortoise, run_async


async def do_stuff():
    """关闭数据库"""
    await Tortoise.close_connections()


async def init():
    """创建数据库"""
    await Tortoise.init(
        config={
            'connections': {
                'default': settings.db_url
            },
            'apps': {
                'models': {
                    "models": ["models.models"],
                    'default_connection': 'default',
                }
            },
            "use_tz": False,
            "timezone": "Asia/Shanghai",
        }
    )
    await Tortoise.generate_schemas()


if __name__ == '__main__':
    run_async(init())  # 创建数据库
    run_async(do_stuff())  # 清理数据库连接
