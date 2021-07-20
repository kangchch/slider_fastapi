import os
# import time
from loguru import logger

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# print(f"log basedir{basedir}")  # /xxx/python_code/FastAdmin/backend/app
# 定位到log日志文件
log_path = os.path.join(basedir, 'logs')

if not os.path.exists(log_path):
    os.mkdir(log_path)
if not os.path.exists(log_path):
    os.mkdir(log_path)

log_path_all = os.path.join(log_path, 'log.log')
log_path_error = os.path.join(log_path, 'error.log')

# 日志简单配置
# 具体其他配置 可自行参考 https://github.com/Delgan/loguru
logger.add(log_path_all, rotation="50 MB", retention="30 days",
           enqueue=True, level='INFO', compression='zip')
logger.add(log_path_error, rotation="50 MB", retention="30 days",
           enqueue=True, level='ERROR', compression='zip')  # 日志等级分割
# format 参数： {time} {level} {message}、  
# {time:YYYY-MM-DD at HH:mm:ss} | {level} | {message} 记录参数
# level 日志等级
# rotation 参数：1 week 一周、00:00每天固定时间、 500 MB 固定文件大小
# retention 参数： 10 days 日志最长保存时间
# compression 参数： zip 日志文件压缩格式
# enqueue 参数 True 日志文件异步写入
# serialize 参数： True 序列化json
# encoding 参数： utf-8 字符编码、部分情况会出现中文乱码问题
#  可通过等级不同对日志文件进行分割储存
