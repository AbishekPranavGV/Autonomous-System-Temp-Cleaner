from PIL import Image

im = Image.open(r"C:\Users\Nunes\.gemini\antigravity\brain\50d997d7-7a4d-4750-9c70-6aed19af6f2b\.user_uploaded\media_1794372827860_36403fa4.png")
for y in range(0, im.height, 2):
    row = ""
    for x in range(0, im.width, 2):
        r, g, b, *a = im.getpixel((x, y))
        if r < 150 or b < 150:
            row += "#"
        else:
            row += " "
    print(f"{y:2d}: {row}")
