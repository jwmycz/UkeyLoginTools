import logging
import sys
import datetime
import os
import traceback
from logging import Formatter, StreamHandler

# 自定义日志级别：SUCCESS（介于 INFO 和 WARNING 之间）
SUCCESS_LEVEL_NUM = 25
logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")

def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kwargs)

logging.Logger.success = success  # 为 logging.Logger 添加 success 方法

# 定义全局日志文件路径（外部必须设定）
logfile = None

# 彩色日志格式化器
class ColorFormatter(Formatter):
    COLORS = {
        'DEBUG': '\033[36m',      # 青色
        'INFO': '\033[32m',       # 绿色
        'SUCCESS': '\033[35m',    # 紫色
        'WARNING': '\033[33m',    # 黄色
        'ERROR': '\033[31m',      # 红色
        'CRITICAL': '\033[1;31m'  # 粗体红色
    }
    RESET = '\033[0m'

    def format(self, record):
        color = self.COLORS.get(record.levelname, '')
        message = super().format(record)
        return f"{color}{message}{self.RESET}" if color else message

# 级别过滤器：只输出指定级别日志
class LevelFilter(logging.Filter):
    def __init__(self, allowed_levels):
        super().__init__()
        self.allowed_levels = allowed_levels

    def filter(self, record):
        return record.levelname in self.allowed_levels

def mkdir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path, 0o777, True)

def get_logger(console_output=False, file_color=False, allowed_levels=None):
    """
    获取配置好的日志记录器

    Args:
        console_output (bool): 是否输出到控制台
        file_color (bool): 日志文件是否包含颜色代码
        allowed_levels (list): 允许输出的日志级别，例如 ['DEBUG', 'INFO', 'SUCCESS', 'ERROR']

    Returns:
        logging.Logger: 配置好的日志记录器
    """
    global logfile
    if not logfile:
        raise ValueError("Log file path not set")

    mkdir_if_not_exists(logfile)
    logger = logging.getLogger('color_file_logger')
    logger.setLevel(logging.DEBUG)

    base_format = '%(asctime)s -- %(filename)s -- %(funcName)s -- %(levelname)s -- %(message)s'
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    log_filename = os.path.join(logfile, f'{now}.log')

    # 默认允许所有级别
    if allowed_levels is None:
        allowed_levels = ['DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL']
    level_filter = LevelFilter(allowed_levels)

    # 检查是否已有 file handler
    file_handler_exists = False
    for h in logger.handlers:
        if isinstance(h, logging.FileHandler) and h.baseFilename == os.path.abspath(log_filename):
            file_handler_exists = True
            file_handler = h
            break

    if not file_handler_exists:
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        formatter = ColorFormatter(base_format) if file_color else Formatter(base_format)
        file_handler.setFormatter(formatter)
        file_handler.addFilter(level_filter)
        logger.addHandler(file_handler)
    else:
        current_color = isinstance(file_handler.formatter, ColorFormatter)
        if current_color != file_color:
            formatter = ColorFormatter(base_format) if file_color else Formatter(base_format)
            file_handler.setFormatter(formatter)
        file_handler.filters.clear()
        file_handler.addFilter(level_filter)

    # 控制台输出
    console_handlers = [h for h in logger.handlers if isinstance(h, StreamHandler) and getattr(h, 'name', None) == 'console']
    if console_output:
        if not console_handlers:
            console = StreamHandler()
            console.name = 'console'
            console.setLevel(logging.DEBUG)
            console.setFormatter(ColorFormatter(base_format))
            console.addFilter(level_filter)
            logger.addHandler(console)
        else:
            for h in console_handlers:
                h.filters.clear()
                h.addFilter(level_filter)
    else:
        for handler in console_handlers:
            logger.removeHandler(handler)

    # 设置全局异常处理
    sys.excepthook = create_exception_handler()

    return logger

def create_exception_handler():
    def handle_exception(exc_type, exc_value, exc_traceback):
        logger = get_logger()
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.error("未捕获的异常", exc_info=(exc_type, exc_value, exc_traceback))
    return handle_exception

# 异常装饰器
def exception(msg="未指定异常信息"):
    def decorator(f):
        def wrap(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                logger = get_logger()
                logger.error(msg)
                logger.error(str(e))
                logger.error("\n" + traceback.format_exc())
        return wrap
    return decorator

def setlog():
    global logfile
    logfile = './logs'
    logger = get_logger(console_output=True, file_color=True,
                                      allowed_levels=['ERROR', 'SUCCESS','DEBUG','INFO','WARNING'])
    return logger
if __name__ == '__main__':
    logfile = './logs'
    logger = get_logger(console_output=True, file_color=True, allowed_levels=['ERROR', 'SUCCESS'])

    logger.debug("这是调试信息")       # 不显示
    logger.info("这是信息")           # 不显示
    logger.success("操作成功")         # ✅ 显示
    logger.warning("警告")             # 不显示
    logger.error("错误发生")           # ✅ 显示
