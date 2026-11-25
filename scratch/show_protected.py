with open('cleaner.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('PROTECTED_PREFIXES')
print(text[idx:idx+500])
