# -*- coding: utf-8 -*-
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Look for chart initialization or datasets
chart_idx = text.find('trajectoryChart')
if chart_idx != -1:
    print("Found trajectoryChart at index", chart_idx)
    print(text[chart_idx:chart_idx+1500])
else:
    chart_idx2 = text.find('storageTrajectoryChart')
    if chart_idx2 != -1:
        print("Found storageTrajectoryChart at index", chart_idx2)
        print(text[chart_idx2:chart_idx2+1500])
