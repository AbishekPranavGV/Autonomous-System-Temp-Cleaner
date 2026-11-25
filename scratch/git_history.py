import subprocess

res = subprocess.run(['git', 'log', '--oneline', '-n', '25'], capture_output=True, text=True)
print(res.stdout)
