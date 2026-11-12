import pygame
from pathlib import Path


FONTS_DIR = Path(__file__).parent / "assets" / "fonts"


def load_font(filename, size):
    font_path = FONTS_DIR / filename

    if not font_path.exists():
        raise FileNotFoundError(
            f"Не найден файл шрифта: {font_path}"
        )

    return pygame.font.Font(str(font_path), size)