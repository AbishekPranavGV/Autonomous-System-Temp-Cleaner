from PIL import Image

im = Image.open(r"C:\Users\Nunes\.gemini\antigravity\brain\50d997d7-7a4d-4750-9c70-6aed19af6f2b\.user_uploaded\media_1794454272799_27ba2150.png")
# Let's crop around the non-background pixels
pixels = []
for y in range(im.height):
    row = ""
    for x in range(im.width):
        r, g, b, *a = im.getpixel((x, y))
        # background is very light blue or white: r > 220, g > 230, b > 240
        if r < 200 or g < 200 or b < 200:
            row += "#"
        else:
            row += " "
    if "#" in row:
        print(f"{y:2d}: {row.rstrip()}")
