from PIL import Image

im = Image.open(r"C:\Users\Nunes\.gemini\antigravity\brain\50d997d7-7a4d-4750-9c70-6aed19af6f2b\.user_uploaded\media_1794454272799_27ba2150.png")
for y in range(33, 39):
    for x in range(10, 25):
        r, g, b, *a = im.getpixel((x, y))
        if r < 200 or g < 200 or b < 200:
            print(f"({x},{y}): R={r}, G={g}, B={b}")
