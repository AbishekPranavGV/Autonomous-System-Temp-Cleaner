import subprocess

res = subprocess.run(['git', 'show', '--stat', '72c0342'], capture_output=True, text=True)
print(res.stdout)
