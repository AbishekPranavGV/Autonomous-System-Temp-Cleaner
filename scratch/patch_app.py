import re

with open('dashboard/app.py', 'r', encoding='utf-8') as f:
    app_text = f.read()

# 1. Update version to 10.0.0
app_text = re.sub(r'LATEST_FLEET_VERSION = "[^"]+"', 'LATEST_FLEET_VERSION = "10.0.0"', app_text)

# 2. Update retention text
app_text = app_text.replace("35-day", "30-day").replace("35-Day", "30-Day").replace("35 days", "30 days")

# 3. Add DEPARTMENTS mapping if not present
if "FLEET_DEPARTMENTS = {" not in app_text:
    dept_code = """
FLEET_DEPARTMENTS = {
    'DESKTOP-M378M07': 'Engineering & Lab',
    'DESKTOP-EV2F0TV': 'Accounts & Finance',
    'DESKTOP-I2MHDIB': 'Production & Quality',
    'DESKTOP-F8G3T2C': 'Front Office & Sales'
}
"""
    app_text = app_text.replace('LATEST_FLEET_VERSION = "10.0.0"', 'LATEST_FLEET_VERSION = "10.0.0"\n' + dept_code)

# 4. Check fleet item creation to include department
if "'department':" not in app_text:
    app_text = app_text.replace("'computer': pc,", "'computer': pc,\n            'department': FLEET_DEPARTMENTS.get(pc, 'Office Workstation'),")

# 5. Add /api/diagnostics endpoint if not present
if "@app.route('/api/diagnostics')" not in app_text:
    diag_code = """
@app.route('/api/diagnostics')
def api_diagnostics():
    try:
        hw = fleet_ai_agent.get_hardware_telemetry() if fleet_ai_agent else {}
        fleet = get_fleet_data().get('fleet', [])
        return jsonify({
            'success': True,
            'version': LATEST_FLEET_VERSION,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'telemetry': hw,
            'fleet_health': {
                'total_nodes': len(fleet),
                'red_zone_count': len([p for p in fleet if p.get('disk_percent_used', 0) >= 90 or p.get('disk_free_gb', 100) < 15]),
                'low_space_alert': hw.get('c_free_gb', 100) < 15,
                'memory_pressure_alert': hw.get('ram_load_percent', 0) > 80,
                'disk_latency_alert': hw.get('disk_latency_ms', 0) > 25.0
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
"""
    # Insert right before @app.route('/api/ai/chat'
    app_text = app_text.replace("@app.route('/api/ai/chat'", diag_code + "\n@app.route('/api/ai/chat'")

# 6. Update api_ai_chat to support lang
app_text = app_text.replace(
    "current_node = payload.get('node') or payload.get('computer')",
    "current_node = payload.get('node') or payload.get('computer')\n        lang = payload.get('lang', 'en')"
)
app_text = app_text.replace(
    "result = fleet_ai_agent.process_message(message, current_node=current_node, fleet_data=fleet_data)",
    "result = fleet_ai_agent.process_message(message, current_node=current_node, fleet_data=fleet_data, lang=lang)"
)

with open('dashboard/app.py', 'w', encoding='utf-8') as f:
    f.write(app_text)

print("Updated dashboard/app.py successfully!")
