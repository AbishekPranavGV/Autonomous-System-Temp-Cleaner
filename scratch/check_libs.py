import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("chart.js present:", "chart.js" in text.lower())
print("tailwind present:", "tailwind" in text.lower())
