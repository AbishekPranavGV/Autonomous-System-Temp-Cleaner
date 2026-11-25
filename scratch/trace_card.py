from PIL import Image

im = Image.open(r"C:\Users\Nunes\.gemini\antigravity\brain\50d997d7-7a4d-4750-9c70-6aed19af6f2b\.user_uploaded\media_1794454272799_27ba2150.png")

for y in range(im.height):
    for x in range(im.width):
        r, g, b, *a = im.getpixel((x, y))
        # Find where white card meets light-blue background
        # card is white: r>240, g>240, b>240
        # background is: r~238, g~246, b~255
        pass

print("Bottom edge of card:")
# find bottom-most white pixel in each column
for x in range(0, im.width, 4):
    bottom_y = -1
    for y in range(im.height):
        r, g, b, *a = im.getpixel((x, y))
        if r > 248 and g > 248 and b > 248:
            bottom_y = y
    if bottom_y != -1:
        print(f"x={x}: bottom_y={bottom_y}")
