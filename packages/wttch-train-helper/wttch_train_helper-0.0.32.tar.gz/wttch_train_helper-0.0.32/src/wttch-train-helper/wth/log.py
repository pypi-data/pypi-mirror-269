import logging
import os
import time

log_format_str = '%(asctime)s.%(msecs)03d %(levelname)s  [%(threadName)s] %(name)s - %(message)s'
colored_log_formatter = None
try:
    # 尝试使用 colorlog
    import colorlog

    colored_log_formatter = colorlog.ColoredFormatter(
        f'%(log_color)s{log_format_str}',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red'
        },
        reset=True,
        style='%'
    )
except ImportError:
    print("⚠️:如果想要带颜色的日志，请安装 colorlog 库")


def get_logger(name: str = "") -> logging.Logger:
    """
    根据指定的名称生成一个 logger, 并尝试使用 colorlog.
    Args:
        name: 日记名称

    Returns:
        logging.Logger: 生成的日志
    """
    timestamp = int(time.time())

    timestamp_str = time.strftime("%Y%m%d-%H%M%S", time.localtime(timestamp))

    if not os.path.exists('logs'):
        os.makedirs('logs')

    log_formatter = logging.Formatter(log_format_str)

    custom_logger = logging.getLogger(name)
    custom_logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(f'logs/{timestamp_str}.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(log_formatter if colored_log_formatter is None else colored_log_formatter)

    custom_logger.addHandler(file_handler)
    custom_logger.addHandler(console_handler)

    return custom_logger
