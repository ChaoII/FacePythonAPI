# 配置文件
import os
import asyncio
from pathlib import Path


class Settings:
    FastAPI_SETTINGS = dict(title="人脸识别",
                            description="人脸识别服务，包含人脸库注册，删除人脸",  # 描述
                            version="1.0rc",  # 版本号
                            )
    sem = asyncio.Semaphore(30)  # 控制项目中 异步请求其他网址时的并发量
    retry = 30  # 网络访重试次数
    # 数据库 配置mysql
    # DB = {
    #     "host": "127.0.0.1",
    #     "port": 3306,
    #     "user": 'root',
    #     "password": '123456',
    #     "database": 'test',
    #     "charset": "utf8mb4"
    # }
    db_url: str = "sqlite://DB.sqlite"
    CORS = dict(allow_origins=['*'],  # 设置允许的origins来源
                allow_credentials=True,
                allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
                allow_headers=["*"])  # 允许跨域的headers，可以用来鉴别来源等作用.
    debug = False

    # 程序配置
    BASE_DIR = Path(__file__).resolve().parent.parent
    log_level = "DEBUG" if debug else "INFO"


settings = Settings()
