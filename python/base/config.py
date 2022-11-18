# 配置文件
from pathlib import Path
import os
import yaml

_YAML_FILE = os.path.join(Path(__file__).resolve().parent.parent, "config.yml")


def read_yml(file):
    """读取yml,传入文件路径file"""
    with open(file, 'r', encoding="utf-8") as f:  # 读取文件
        yml_config = yaml.load(f, Loader=yaml.FullLoader)  # Loader为了更加安全
    return yml_config


def updata_yaml(file, *args, **kwargs):
    """更新yml的数值"""
    old_data = read_yml(file)  # 读取文件数据
    for key in kwargs.keys():
        old_data[key] = kwargs[key]
    with open(file, "w", encoding="utf-8") as f:
        yaml.dump(old_data, f, encoding='utf-8', allow_unicode=True)


yaml_config = read_yml(_YAML_FILE)
# ----------base config--------------
_base = yaml_config["base"]
_face = yaml_config["face"]


class Settings:
    FastAPI_SETTINGS = dict(title=_base["title"],
                            description=_base["description"],  # 描述
                            version=_base["version"],  # 版本号
                            )

    DB_URL: str = _base["db_url"]
    CORS = dict(allow_origins=_base["allow_origins"],  # 设置允许的origins来源
                allow_credentials=True,
                allow_methods=_base["allow_methods"],  # 设置允许跨域的http方法，比如 get、post、put等。
                allow_headers=_base["allow_headers"])  # 允许跨域的headers，可以用来鉴别来源等作用.
    # 程序配置
    BASE_DIR = Path(__file__).resolve().parent.parent
    ROOT_DIR = BASE_DIR.parent

    LOG_LEVEL = "DEBUG" if _base["debug"] else "INFO"
    PORT = _base["port"]
    WORKERS = _base["workers"]

    REC_THRESHOLD = _face["rec_threshold"]
    IS_ANTI_SPOOF = _face["is_anti_spoof"]
    USE_GPU = _face["use_gpu"]
    GPU_ID = _face["gpu_id"]
    TRACKING_SIZE = _face["tracking_size"]
    FUNCTIONS = _face["functions"]
    ALLOW_IMAGES = _face["allow_images"]


settings = Settings()
