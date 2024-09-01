from PIL import Image, ImageDraw, ImageFont
import os
import math

class SkinGenerator:
    RARITY_PRIORITY = {
        "mythic": 1,
        "legendary": 2,
        "epic": 13,
        "rare": 14,
        "uncommon": 15,
        "common": 16,
        "icon_series": 11,
        "dark": 3,
        "starwars": 5,
        "marvel": 6,
        "dc": 12,
        "gaminglegends": 9,
        "shadow": 10,
        "slurp": 4,
        "lava": 7,
        "frozen": 8
    }

    def __init__(self, font_path="Burbank-Big-Condensed-Black.ttf", img_folder="imgs"):
        self.font_path = font_path
        self.img_folder = img_folder

    def skin_size(self, count):
        if count > 200:
            return 64
        elif count > 100:
            return 80
        elif count > 50:
            return 100
        elif count > 25:
            return 120
        else:
            return 150

    def find_img(self, name):
        for f in os.listdir(self.img_folder):
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                skin_name, _, rarity = f.rpartition('$')
                skin_name = skin_name.replace('_', ' ')
                if skin_name.strip().lower() == name.strip().lower():
                    return os.path.join(self.img_folder, f), rarity.split('.')[0].lower()
        return None, None

    def load_imgs(self, names, size):
        imgs = []
        for name in names:
            path, rarity = self.find_img(name)
            if path and rarity:
                try:
                    img = Image.open(path).convert("RGBA")
                    img = img.resize((size, size), Image.LANCZOS)
                    imgs.append((img, rarity))
                except Exception as e:
                    print(f"Error: '{name}' - {e}")
            else:
                print(f"Not found: '{name}'")
        return imgs

    def sort_imgs(self, imgs):
        return sorted(imgs, key=lambda x: self.RARITY_PRIORITY.get(x[1].lower(), 99))

    def add_border(self, img, rarity, thickness=4):
        colors = {
            "mythic": (255, 223, 0),
            "legendary": (255, 69, 0),
            "epic": (138, 43, 226),
            "rare": (0, 0, 255),
            "uncommon": (0, 255, 0),
            "common": (169, 169, 169),
            "icon_series": (64, 224, 208),
            "dark": (128, 0, 128),
            "starwars": (0, 0, 139),
            "marvel": (255, 0, 0),
            "dc": (0, 0, 139),
            "gaminglegends": (0, 191, 255),
            "shadow": (105, 105, 105),
            "slurp": (64, 224, 208),
            "lava": (255, 140, 0),
            "frozen": (173, 216, 230)
        }
        color = colors.get(rarity.lower(), (255, 255, 255))
        bordered = Image.new("RGBA", (img.width + 2 * thickness, img.height + 2 * thickness), color)
        bordered.paste(img, (thickness, thickness), img)
        return bordered

    def generate(self, names, out_path):
        count = len(names)
        if count == 0:
            print("No skins")
            return

        min_count = max(count, 25)
        size = self.skin_size(min_count)

        imgs = self.sort_imgs(self.load_imgs(names, size))

        per_row = int(math.ceil(math.sqrt(min_count)))
        rows = (min_count + per_row - 1) // per_row

        pad = 5
        border = 4
        width = (size + 2 * border + pad) * per_row + pad
        height = (size + 2 * border + pad) * rows + 180

        bg_color = (20, 20, 20)
        text_color = (255, 255, 255)

        img = Image.new('RGBA', (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype(self.font_path, 50)
        footer_font = ImageFont.truetype(self.font_path, 40)
        title = "BoltFN - Fortnite Xbox Checker"
        title_width = draw.textbbox((0, 0), title, font=font)[2]
        draw.text(((width - title_width) / 2, pad), title, font=font, fill=text_color)

        for i, (skin_img, rarity) in enumerate(imgs):
            bordered = self.add_border(skin_img, rarity, border)
            x = pad + (i % per_row) * (size + 2 * border + pad)
            y = pad * 2 + 60 + (i // per_row) * (size + 2 * border + pad)
            img.paste(bordered, (x, y), bordered)

        footer = "https://github.com/dvmestos/BoltFN_Linux"
        footer_width = draw.textbbox((0, 0), footer, font=footer_font)[2]
        footer_y_position = height - pad - 60

        draw.text(((width - footer_width) / 2, footer_y_position), footer, font=footer_font, fill=text_color)

        img.save(out_path)
        print(f"Saved to {out_path}")
