import logging
import logging.handlers
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)


def setup_logger(
    name: str = __name__,
    log_file: str = "arcana_os.log",
    error_file: str = "arcana_os_errors.log",
    level: int = logging.INFO,
) -> logging.Logger:
    """Настроить логгер с выводом в консоль и файлы .log в logs/.

    Args:
        name: Имя логгера.
        log_file: Имя основного лог-файла (относительно logs/).
        error_file: Имя файла для ошибок (относительно logs/).
        level: Минимальный уровень логирования.

    Returns:
        Настроенный logging.Logger.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # уже настроен

    logger.setLevel(level)

    _format = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(_format)
    logger.addHandler(console_handler)

    # Основной файл
    log_path = LOGS_DIR / log_file
    file_handler = logging.handlers.RotatingFileHandler(
        log_path,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(_format)
    logger.addHandler(file_handler)

    # Файл ошибок
    error_path = LOGS_DIR / error_file
    error_handler = logging.handlers.RotatingFileHandler(
        error_path,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(_format)
    logger.addHandler(error_handler)

    return logger
