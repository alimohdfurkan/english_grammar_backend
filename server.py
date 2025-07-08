from flask import Flask, request, jsonify
import language_tool_python
from gramformer import Gramformer

app = Flask(__name__)

tool = language_tool_python.LanguageTool('en-US')
gf = Gramformer(models=1)  # Grammar correction

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    text = data.get("text", "")
    matches = tool.check(text)
    suggestions = [{
        "message": m.message,
        "replacements": m.replacements,
        "offset": m.offset,
        "length": m.errorLength
    } for m in matches]

    corrected = list(gf.correct(text))
    return jsonify({
        "original": text,
        "corrected": corrected[0] if corrected else text,
        "suggestions": suggestions
    })

@app.route('/')
def home():
    return "Grammar API Running"

if __name__ == '__main__':
    app.run()
