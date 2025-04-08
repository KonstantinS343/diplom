import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logging(log_level=logging.INFO, log_file="app.log"):
    """
    Настраивает глобальное логирование для приложения.
    
    Args:
        log_level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Путь к файлу логов
    """
    # Создаем логгер
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Очищаем существующие обработчики, чтобы избежать дублирования
    if logger.hasHandlers():
        logger.handlers.clear()

    # Формат сообщений
    log_format = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # Обработчик для записи в файл с ротацией
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5           # Хранить до 5 файлов логов
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    # Устанавливаем уровень логирования для корневого логгера
    logging.getLogger().setLevel(log_level)