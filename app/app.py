import requests
from flask import Flask
import os

app = Flask(__name__)


def dec_to_bin(value):
    return bin(int(value))[2:]


def dec_to_hex(value):
    return hex(int(value))[2:]


def bin_to_dec(value):
    return str(int(value, 2))


def bin_to_hex(value):
    return hex(int(value, 2))[2:]


def hex_to_dec(value):
    return str(int(value, 16))


def hex_to_bin(value):
    return bin(int(value, 16))[2:]


conversion_functions = {
    ('dec', 'bin'): dec_to_bin,
    ('dec', 'hex'): dec_to_hex,
    ('bin', 'dec'): bin_to_dec,
    ('bin', 'hex'): bin_to_hex,
    ('hex', 'dec'): hex_to_dec,
    ('hex', 'bin'): hex_to_bin
}

usage_guide = (
    "Usage: /convert/&lt;value&gt;/&lt;input-format&gt;/&lt;output-format&gt;"
    "Possible values for &lt;input-format&gt; and &lt;output-format&gt: dec, hex, bin"
)


@app.route('/convert/<value>/<input_format>/<output_format>', methods=['GET'])
def convert(value, input_format, output_format):
    if input_format == output_format:
        return "The input and output should be different"

    try:
        conversion_function = conversion_functions.get(
            (input_format, output_format))
        if conversion_function:
            converted_value = conversion_function(value)
            return converted_value
        else:
            return usage_guide
    except ValueError:
        return "Invalid input value"


@app.errorhandler(404)
def page_not_found(e):
    return usage_guide, 404


@app.route('/health', methods=['GET'])
def health_check():
    try:
        base_url = "http://localhost:" + str(os.environ.get("FLASK_SERVER_PORT")) + "/convert"
        test_cases = [
            ("10", "dec", "bin", "1010"),
            ("10", "dec", "hex", "a"),
            ("1010", "bin", "dec", "10"),
            ("1010", "bin", "hex", "a"),
            ("a", "hex", "dec", "10"),
            ("a", "hex", "bin", "1010")
        ]
        
        for value, input_format, output_format, expected in test_cases:
            response = requests.get(f"{base_url}/{value}/{input_format}/{output_format}")
            if response.text != expected:
                return "Health check failed", 500
        
        return "OK"
    except Exception as e:
        return f"Health check failed: {str(e)}", 500

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", 
          port=os.environ.get("FLASK_SERVER_PORT"))