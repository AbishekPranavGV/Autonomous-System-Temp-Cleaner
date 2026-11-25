import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

tabs = re.findall(r'id=["\']tab_[^"\']+["\']', text)
print('Tabs found:', tabs)

sections = re.findall(r'id=["\']sec_[^"\']+["\']', text)
print('Sections found:', sections)

canvas_list = re.findall(r'<canvas[^>]+>', text)
print('Canvases found:', len(canvas_list))
for c in canvas_list:
    print('  ', c)

chart_refs = re.findall(r'new Chart\([^)]+\)', text)
print('Chart instances found:', len(chart_refs))
for cr in chart_refs:
    print('  ', cr)
