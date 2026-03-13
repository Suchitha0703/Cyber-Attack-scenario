import requests
import time
import random
from flask import Flask, render_template, jsonify, request

app = Flask(__name__, template_folder='templets')

# Track simulation statistics
stats = {
    'bruteforce': 0,
    'xss': 0,
    'phishing': 0,
    'dos': 0,
    'malware': 0,
    'ransomware': 0,
    'mitm': 0,
    'indirect': 0,
    'wifi': 0
}

@app.route('/')
def index():
    return render_template('index.html', title="Overview")

@app.route('/xss')
def xss():
    return render_template('xss.html', title="XSS Sandbox")

@app.route('/ransomware')
def ransomware():
    return render_template('ran.html', title="Ransomware Lab")

@app.route('/phishing')
def phishing():
    return render_template('phishing.html', title="Phishing Simulation")

@app.route('/mitm')
def mitm():
    return render_template('mitm.html', title="MITM Lab")

@app.route('/dos')
def dos():
    return render_template('dos.html', title="DoS Lab")

@app.route('/bruteforce')
def bruteforce():
    return render_template('bruteforce.html', title="Brute Force Lab")

@app.route('/malware')
def malware():
    return render_template('malware.html', title="Malware Lab")

@app.route('/wifi_sim')
def wifi_sim():
    return render_template('wifi_sim.html', title="WiFi Simulation")

@app.route('/indirect')
def indirect():
    return render_template('indirect.html', title="Indirect Injection")

@app.route('/hub')
def hub():
    return render_template('hub.html', title="Hub")

# API Endpoints for Interactive Features
@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Return simulation statistics"""
    total = sum(stats.values())
    return jsonify({'total': total, 'stats': stats})

@app.route('/api/bruteforce', methods=['POST'])
def api_bruteforce():
    """Run brute force simulation"""
    data = request.json or {}
    dictionary = data.get('dictionary', ["123456", "password", "admin123", "qwerty", "secret"])
    
    # Simulate attack
    target_password = random.choice(dictionary)
    attempts = []
    
    for i, pwd in enumerate(dictionary, 1):
        attempts.append({
            'attempt': i,
            'password': pwd,
            'success': pwd == target_password,
            'time': i * 500
        })
        if pwd == target_password:
            break
    
    stats['bruteforce'] += 1
    return jsonify({
        'success': True,
        'password_found': target_password,
        'attempts': attempts,
        'total_attempts': len(attempts)
    })

@app.route('/api/xss', methods=['POST'])
def api_xss():
    """Test XSS vulnerability"""
    data = request.json or {}
    payload = data.get('payload', '')
    
    dangerous = ['<script>', 'onclick=', 'onerror=', 'alert(', 'eval(']
    is_vulnerable = any(x in payload.lower() for x in dangerous)
    
    stats['xss'] += 1
    return jsonify({
        'payload': payload,
        'vulnerable': is_vulnerable,
        'severity': 'CRITICAL' if is_vulnerable else 'SAFE'
    })

@app.route('/api/dos', methods=['POST'])
def api_dos():
    """Simulate DoS attack"""
    data = request.json or {}
    duration = min(data.get('duration', 5), 10)
    
    attack_data = [{'second': i, 'requests': random.randint(100, 800)} for i in range(1, duration+1)]
    stats['dos'] += 1
    
    return jsonify({
        'duration': duration,
        'total_requests': sum(d['requests'] for d in attack_data),
        'data': attack_data
    })

@app.route('/api/phishing', methods=['POST'])
def api_phishing():
    """Simulate phishing attack"""
    stats['phishing'] += 1
    return jsonify({
        'success': random.random() > 0.3,
        'credentials_captured': random.random() > 0.4
    })

@app.route('/api/malware', methods=['POST'])
def api_malware():
    """Scan for malware"""
    data = request.json or {}
    file_hash = data.get('file_hash', '')
    
    suspicious_hashes = ['malware001', 'virus123', 'trojan456']
    detected = any(h in file_hash.lower() for h in suspicious_hashes)
    
    stats['malware'] += 1
    return jsonify({
        'detected': detected,
        'threat': 'CRITICAL' if detected else 'CLEAN'
    })

@app.route('/api/ransomware', methods=['POST'])
def api_ransomware():
    """Simulate ransomware"""
    data = request.json or {}
    num_files = data.get('num_files', 5)
    
    files = [f'document{i}.txt' for i in range(num_files)]
    stats['ransomware'] += 1
    
    return jsonify({
        'files_encrypted': num_files,
        'ransom_amount': random.randint(500, 5000),
        'encrypted_files': files
    })


# additional simple endpoints for tracking other scenarios
@app.route('/api/mitm', methods=['POST'])
def api_mitm():
    stats['mitm'] += 1
    return jsonify({'success': True})

@app.route('/api/indirect', methods=['POST'])
def api_indirect():
    stats['indirect'] += 1
    return jsonify({'success': True})

@app.route('/api/wifi', methods=['POST'])
def api_wifi():
    stats['wifi'] += 1
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)