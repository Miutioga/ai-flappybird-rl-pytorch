# MIT License
#
# Copyright (c) 2020 Gabriel Nogueira (Talendar)
# Copyright (c) 2023 Martin Kubovcik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

""" Utility functions.

Some of the code in this module is an adaption of the code in the `FlapPyBird`
GitHub repository by `sourahbhv` (https://github.com/sourabhv/FlapPyBird),
released under the MIT license.
"""

import os
import sys
import random
import pygame
from pathlib import Path
from typing import Any, Dict, List, Optional

from pygame import Rect
from pygame import image as pyg_image
from pygame import mixer as pyg_mixer
from pygame.transform import flip as img_flip

_BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__))).parent

SPRITES_PATH = str(_BASE_DIR / "assets/sprites")
AUDIO_PATH = str(_BASE_DIR / "assets/audio")
MODEL_PATH = str(_BASE_DIR / "assets/model")


class GroundAnimals:
    def __init__(self, screen_width, ground_y):
        self.animals = []
        self.screen_width = screen_width
        self.ground_y = ground_y
        
        self.animal_images = {
            'fat': pyg_image.load(f"{SPRITES_PATH}/fat.png"),
            'normal': pyg_image.load(f"{SPRITES_PATH}/normal.png"),
            'tall': pyg_image.load(f"{SPRITES_PATH}/tall.png"),
        }

        # Khởi tạo các con vật với vị trí ngẫu nhiên
        self.spawn_animals(3)  # Số lượng con vật ban đầu
        
    def spawn_animals(self, num_animals):
        count = 0


        for _ in range(num_animals):
            lst = ['fat', 'normal', 'tall']
            i = lst[count]

            # Xác định tọa độ y tùy thuộc vào loại động vật
            if i == 'fat':
                y = self.ground_y - 20  # Đặt con vật thấp nhất
                speed = 0.5
            elif i == 'normal':
                y = self.ground_y - 15  # Đặt con vật ở giữa
                speed = 1
            else:  # 'tall'
                y = self.ground_y - 25  # Đặt con vật cao nhất
                speed = 2

            animal = {
                'x': random.randrange(0, self.screen_width),
                'y': y,
                'speed': speed,  # Tốc độ di chuyển ngẫu nhiên
                # 'direction': random.choice([-1, 1]),  # -1: trái, 1: phải
                'direction': 1,
                'type': i,  # Loại con vật
            }
            self.animals.append(animal)
            count += 1
            if count == 3:
                count = 0
    
    def update(self):
        for animal in self.animals:
            # Di chuyển con vật
            animal['x'] += animal['speed'] * animal['direction']
            
            # Nếu con vật đi ra khỏi màn hình, cho nó quay lại
            if animal['x'] < -20:
                animal['x'] = self.screen_width + 20
                animal['direction'] = -1
            elif animal['x'] > self.screen_width + 20:
                animal['x'] = -20
                animal['direction'] = 1
    
    def draw(self, surface):
        for animal in self.animals:
            # Lấy ảnh tương ứng cho loại con vật
            animal_image = self.animal_images[animal['type']]
            animal_image = pygame.transform.scale(animal_image, (animal_image.get_width()//5, animal_image.get_height()//5))
            
            # Điều chỉnh vị trí vẽ hình ảnh dựa trên kích thước con vật
            image_rect = animal_image.get_rect(center=(int(animal['x']), int(animal['y'])))
            
            # Vẽ ảnh con vật lên màn hình
            surface.blit(animal_image, image_rect)


class SnowfallEffect:
    def __init__(self, screen_width, screen_height, num_snowflakes=50):
        self.snow = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Khởi tạo các bông tuyết với vị trí ngẫu nhiên
        for _ in range(num_snowflakes):
            self.snow.append({
                'x': random.randrange(0, screen_width),
                'y': random.randrange(-50, screen_height),
                'speed': random.randrange(1, 4),  # Tốc độ rơi khác nhau
                'size': random.randrange(1, 3)    # Kích thước khác nhau
            })

    def update(self):
        # Cập nhật vị trí của các bông tuyết
        for snowflake in self.snow:
            # Di chuyển bông tuyết xuống dưới
            snowflake['y'] += snowflake['speed']
            
            # Thêm chút chuyển động sang ngang
            snowflake['x'] += random.randrange(-1, 2)
            
            # Nếu bông tuyết rơi ra khỏi màn hình, đặt lại vị trí từ trên cao
            if snowflake['y'] > self.screen_height:
                snowflake['y'] = random.randrange(-50, -10)
                snowflake['x'] = random.randrange(0, self.screen_width)
            
            # Giữ bông tuyết trong phạm vi màn hình theo chiều ngang
            if snowflake['x'] < 0:
                snowflake['x'] = self.screen_width
            elif snowflake['x'] > self.screen_width:
                snowflake['x'] = 0

    def draw(self, surface):
        # Vẽ các bông tuyết
        for snowflake in self.snow:
            pygame.draw.circle(
                surface, 
                'white', 
                (int(snowflake['x']), int(snowflake['y'])),
                snowflake['size']
            )


def pixel_collision(
    rect1: Rect, rect2: Rect, hitmask1: List[List[bool]], hitmask2: List[List[bool]]
) -> bool:
    """Checks if two objects collide and not just their rects."""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                return True
    return False


def get_hitmask(image) -> List[List[bool]]:
    """Returns a hitmask using an image's alpha."""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x, y))[3]))
    return mask


def _load_sprite(filename, convert, alpha=True):
    img = pyg_image.load(f"{SPRITES_PATH}/{filename}")
    return (
        img.convert_alpha() if convert and alpha else img.convert() if convert else img
    )


def load_images(
    convert: bool = True,
    bg_type: Optional[str] = "day",
    bird_color: str = "yellow",
    pipe_color: str = "green",
) -> Dict[str, Any]:
    """Loads and returns the image assets of the game."""
    images = {}

    try:
        # Sprites with the number for the score display:
        images["numbers"] = tuple(
            [_load_sprite(f"{n}.png", convert=convert, alpha=True) for n in range(10)]
        )

        # Game over sprite:
        images["gameover"] = _load_sprite("gameover.png", convert=convert, alpha=True)

        # Welcome screen message sprite:
        images["message"] = _load_sprite("message.png", convert=convert, alpha=True)

        # Sprite for the base (ground):
        images["base"] = _load_sprite("base.png", convert=convert, alpha=True)

        # Background sprite:
        if bg_type is None:
            images["background"] = None
        else:
            images["background"] = _load_sprite(
                f"background-{bg_type}.png", convert=convert, alpha=False
            )

        # Bird sprites:
        images["player"] = (
            _load_sprite(f"{bird_color}bird-upflap.png", convert=convert, alpha=True),
            _load_sprite(f"{bird_color}bird-midflap.png", convert=convert, alpha=True),
            _load_sprite(f"{bird_color}bird-downflap.png", convert=convert, alpha=True),
        )

        # Pipe sprites:
        pipe_sprite = _load_sprite(
            f"pipe-{pipe_color}.png", convert=convert, alpha=True
        )
        images["pipe"] = (img_flip(pipe_sprite, False, True), pipe_sprite)
    except FileNotFoundError as ex:
        raise FileNotFoundError(
            "Can't find the sprites folder! No such file or"
            f" directory: {SPRITES_PATH}"
        ) from ex

    return images


def load_sounds() -> Dict[str, pyg_mixer.Sound]:
    """Loads and returns the audio assets of the game."""
    pyg_mixer.init()
    sounds = {}

    if "win" in sys.platform:
        soundExt = ".wav"
    else:
        soundExt = ".ogg"

    try:
        sounds["die"] = pyg_mixer.Sound(AUDIO_PATH + "/die" + soundExt)
        sounds["hit"] = pyg_mixer.Sound(AUDIO_PATH + "/hit" + soundExt)
        sounds["point"] = pyg_mixer.Sound(AUDIO_PATH + "/point" + soundExt)
        sounds["swoosh"] = pyg_mixer.Sound(AUDIO_PATH + "/swoosh" + soundExt)
        sounds["wing"] = pyg_mixer.Sound(AUDIO_PATH + "/wing" + soundExt)
    except FileNotFoundError as ex:
        raise FileNotFoundError(
            "Can't find the audio folder! No such file or " f"directory: {AUDIO_PATH}"
        ) from ex

    return sounds
