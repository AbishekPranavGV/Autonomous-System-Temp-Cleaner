import os

up_dir = r"C:\Users\Nunes\.gemini\antigravity\brain\50d997d7-7a4d-4750-9c70-6aed19af6f2b\.user_uploaded"
files = os.listdir(up_dir)
for f in sorted(files):
    p = os.path.join(up_dir, f)
    sz = os.path.getsize(p)
    print(f"{f}: {sz} bytes")
