
from flask import Flask, request, jsonify
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        df = pd.read_excel(BytesIO(file.read()))
        json_result = df.to_dict(orient='records')
        return jsonify(json_result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
