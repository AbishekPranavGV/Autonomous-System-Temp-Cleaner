from PIL import Image

for fn in ["media_1794392613776_3df7d435.png", "media_1794392713093_faddc7ec.jpg", "media_1794390319673_0c258eae.png"]:
    p = f"C:/Users/Nunes/.gemini/antigravity/brain/50d997d7-7a4d-4750-9c70-6aed19af6f2b/.user_uploaded/{fn}"
    im = Image.open(p)
    print(fn, "size:", im.size)
