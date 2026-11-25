# -*- coding: utf-8 -*-
import sys
from pathlib import Path

with open('nunes_fleet_agent.ps1', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'Write-Host "   [OK] Fleet registration confirmed for $($Telemetry.Computer)!" -ForegroundColor Green'
replacement = target + '\n                $Script:CandidateUrls = @($baseUrl) + ($CandidateUrls | Where-Object { $_ -ne $baseUrl })'

if target in text and '$Script:CandidateUrls = @($baseUrl)' not in text:
    text = text.replace(target, replacement)
    with open('nunes_fleet_agent.ps1', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Added $Script:CandidateUrls to nunes_fleet_agent.ps1")
else:
    print("Target already updated or not found")

# Rebuild client zip
sys.path.insert(0, str(Path('.').resolve()))
import zip_builder
zip_builder.build_client_zip(verbose=True)
