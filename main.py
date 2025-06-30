from flask import Flask, request, jsonify
from utils.kpi_analysis import generate_chatters_json

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse():
    inflow = request.files.get('inflow')
    creator = request.files.get('creator')
    if not inflow or not creator:
        return jsonify({'error': 'Missing inflow or creator export'}), 400
    result = generate_chatters_json(inflow, creator)
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
