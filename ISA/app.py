from flask import Flask, request, jsonify
from flask_cors import CORS
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
        if not code:
            return jsonify({
                'error': 'No code provided',
                'cpu_state': None,
                'memory': None
            }), 400

        # Compile and execute the assembly code
        result = COMPILE_ASM(code)

        # Check if there was an error during execution
        if 'error' in result:
            return jsonify({
                'error': result['error'],
                'cpu_state': result['cpu_state'],
                'memory': result['memory']
            }), 400

        # Return successful execution results
        return jsonify({
            'error': None,
            'cpu_state': result['cpu_state'],
            'memory': result['memory']
        })

    except Exception as e:
        return jsonify({
            'error': f'Error processing request: {str(e)}',
            'cpu_state': None,
            'memory': None
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
