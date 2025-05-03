#Saarthak Mudigere Girsh
#saarthakmudigere@gmail.com
#6823923698

from flask import Flask, request, jsonify
from executor import run_script
import re

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json() #request data
    #error if 'script' field doesnt exist
    if not isinstance(data, dict) or 'script' not in data:
        return jsonify({"error": "Missing 'script' field"}), 400

    scr = data['script'] #request value

    #error if 'main()' function doesnt exist
    if not re.search(r"def\s+main\s*\(", scr):
        return jsonify({"error": "Missing 'main()' function"}), 400

    result, stdout, error = run_script(scr) #output

    #error if python script throws an error
    if error:
        return jsonify({"error": error}), 400

    return jsonify({"result": result, "stdout": stdout})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)