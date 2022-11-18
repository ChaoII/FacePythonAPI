import os
import sys
from loguru import logger
from base.config import settings

log_path = os.path.join(settings.BASE_DIR, 'logs')  # 下载文件位置
if not os.path.exists(log_path):
    os.makedirs(log_path)
log_file = os.path.join(log_path, f'BaseApi.log')
logger.remove()
logger.add(sys.stderr, level=settings.LOG_LEVEL)
logger.add(log_file, level=settings.LOG_LEVEL)
