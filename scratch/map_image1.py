from PIL import Image

im = Image.open(r"C:\Users\Nunes\.gemini\antigravity\brain\50d997d7-7a4d-4750-9c70-6aed19af6f2b\.user_uploaded\media_1794454272799_27ba2150.png")
print("im size:", im.size)

# Print 2D representation of pixels
for y in range(0, im.height, 2):
    row = ""
    for x in range(0, im.width, 1):
        r, g, b, *a = im.getpixel((x, y))
        # classify color
        if r > 250 and g > 250 and b > 250:
            row += "." # pure white (card)
        elif r > 230 and g > 240:
            row += " " # light blue (page bg)
        elif r < 180 and b > 200:
            row += "B" # blue
        elif r > 150 and b < 100:
            row += "O" # orange
        elif r < 150:
            row += "#"
        else:
            row += "-"
    print(f"{y:2d}: {row}")
