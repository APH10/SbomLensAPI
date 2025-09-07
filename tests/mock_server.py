from flask import Flask, request, jsonify
app = Flask(__name__)
VALID_API_KEY='TESTKEY'; VALID_USER='user'; VALID_PASS='pass'; VALID_TOKEN='dummytoken'

@app.before_request
def require_key():
    key = request.headers.get('X-API-Key') or request.headers.get('x-api-key')
    if key != VALID_API_KEY:
        return jsonify({'error':'Invalid API key'}), 401

@app.route('/api/status')
def status(): return jsonify({'status':'OK'})

@app.route('/api/auth', methods=['POST'])
def auth():
    data = request.get_json(silent=True) or {}
    if data.get('username')==VALID_USER and data.get('password')==VALID_PASS:
        return jsonify({'token': VALID_TOKEN})
    return jsonify({'error':'Invalid credentials'}), 401

@app.route('/api/end1')
def end1():
    if request.headers.get('Authorization') != f'Bearer {VALID_TOKEN}': return jsonify({'error':'Unauthorized'}), 403
    return jsonify({'data':'hello'})

@app.route('/api/load', methods=['POST'])
def load():
    if request.headers.get('Authorization') != f'Bearer {VALID_TOKEN}': return jsonify({'error':'Unauthorized'}), 403
    project = request.form.get('project'); release = request.form.get('release'); f = request.files.get('file')
    if not f: return jsonify({'error':'File missing'}), 400
    return jsonify({'project':project,'release':release,'filename': f.filename})

if __name__=='__main__': app.run(host='127.0.0.1', port=5000)
