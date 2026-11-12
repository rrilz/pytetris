import pygame
from pathlib import Path


class AudioManager:
    # Все звуковые эффекты (короткие звуки)
    SOUND_FILES = {
        "button":    "button.ogg",
        "hard_drop": "hard_drop.ogg",
        "lock":      "lock.ogg",
        "clear":     "clear.ogg",
        "rotate":    "rotate.ogg",
    }

    # Все музыкальные треки
    MUSIC_FILES = {
        "menu":      "menu.mp3",
        "game":      "main.mp3",
        "game_over": "over.mp3",
    }

    def __init__(self, music_volume=0.5, sound_volume=0.7):
        self.music_volume = self._clamp(music_volume)
        self.sound_volume = self._clamp(sound_volume)
        self.sounds = {}

        self._assets_dir = Path(__file__).parent / "assets"
        self._load_all_sounds()

    @staticmethod
    def _clamp(value):
        return max(0.0, min(1.0, float(value)))

    def _load_all_sounds(self):
        """Пытается загрузить все стандартные sfx. Отсутствующие — молча пропускает."""
        sound_dir = self._assets_dir / "sounds"
        for name, filename in self.SOUND_FILES.items():
            path = sound_dir / filename
            if not path.is_file():
                # Не роняем игру — просто не будет этого эффекта
                continue
            sound = pygame.mixer.Sound(str(path))
            sound.set_volume(self.sound_volume)
            self.sounds[name] = sound

    def load_sound(self, name, filename):
        """Ручная загрузка звука. Относительный путь ищется в assets/sounds/."""
        path = Path(filename)
        if not path.is_absolute():
            path = self._assets_dir / "sounds" / filename

        if not path.is_file():
            raise FileNotFoundError(f"Не найден звуковой файл: {path}")

        sound = pygame.mixer.Sound(str(path))
        sound.set_volume(self.sound_volume)
        self.sounds[name] = sound
        return sound

    def play_sound(self, name):
        sound = self.sounds.get(name)
        if sound is not None:
            sound.set_volume(self.sound_volume)
            sound.play()

    # Алиас — game.py и main.py вызывают именно play_sfx
    def play_sfx(self, name):
        self.play_sound(name)

    def stop_sound(self, name):
        sound = self.sounds.get(name)
        if sound is not None:
            sound.stop()

    def set_sound_volume(self, value):
        self.sound_volume = self._clamp(value)
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)

    def play_music(self, track, loops=-1, restart=True):
        if track not in self.MUSIC_FILES:
            raise ValueError(f"Неизвестный музыкальный трек: {track}")

        path = self._assets_dir / "music" / self.MUSIC_FILES[track]
        if not path.is_file():
            raise FileNotFoundError(f"Не найден музыкальный файл: {path}")

        if not restart and pygame.mixer.music.get_busy():
            return

        pygame.mixer.music.load(str(path))
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(loops)

    def stop_music(self):
        pygame.mixer.music.stop()

    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
        pygame.mixer.music.unpause()

    def set_music_volume(self, value):
        self.music_volume = self._clamp(value)
        pygame.mixer.music.set_volume(self.music_volume)