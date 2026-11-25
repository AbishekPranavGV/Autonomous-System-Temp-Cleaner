from PIL import Image
import os

target = Image.open(r"C:\Users\Nunes\.gemini\antigravity\brain\50d997d7-7a4d-4750-9c70-6aed19af6f2b\.user_uploaded\media_1794454272799_27ba2150.png")

up_dir = r"C:\Users\Nunes\.gemini\antigravity\brain\50d997d7-7a4d-4750-9c70-6aed19af6f2b\.user_uploaded"
for fn in os.listdir(up_dir):
    if fn == "media_1794454272799_27ba2150.png": continue
    p = os.path.join(up_dir, fn)
    try:
        im = Image.open(p)
        # Search if target crop or similar pixels appear in im
        tw, th = target.size
        w, h = im.size
        if w >= tw and h >= th:
            # check center pixel of target
            found = False
            for y in range(0, h - th, 5):
                for x in range(0, w - tw, 5):
                    # compare a few key pixels
                    match = True
                    for cy, cx in [(34, 12), (34, 16), (34, 20), (10, 20), (0, 0)]:
                        tp = target.getpixel((cx, cy))[:3]
                        ip = im.getpixel((x + cx, y + cy))[:3]
                        if abs(tp[0]-ip[0]) > 30 or abs(tp[1]-ip[1]) > 30 or abs(tp[2]-ip[2]) > 30:
                            match = False
                            break
                    if match:
                        print(f"Match found in {fn} at ({x}, {y})!")
                        found = True
                        break
                if found: break
    except Exception as e:
        pass
