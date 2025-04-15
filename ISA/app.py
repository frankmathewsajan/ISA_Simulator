from flask import Flask, request, jsonify
from flask_cors import CORS  # New import
from asm_compiler import COMPILE_ASM
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/', methods=['POST'])
def handle_request():
    try:
        # Parse the incoming JSON data
        data = request.get_json()

        # Extract the code from the request
        code = data.get('code', '')
        compiled_code = COMPILE_ASM(code)
        # Return a JSON response with the output field
        return jsonify({
            'output': f'{compiled_code}'
        })
    except Exception as e:
        return jsonify({
            'output': f'Error processing request: {str(e)}'
        }), 400


if __name__ == '__main__':
    app.run(debug=True)
