from flask import Flask, request, jsonify
from flask_cors import CORS
from read_file import readFile
from vector_store import add_text_to_collection, get_chroma, get_answer, delete_collection

app = Flask(__name__)
CORS(app=app)


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    f.save(f.filename)
    # readFile(f.filename)
    add_text_to_collection(f.filename)
    return jsonify("success")


@app.route('/getChroma', methods=['GET'])
def getChroma():
    return jsonify(get_chroma())


@app.route('/query',methods=['POST'])
def query():
    response = get_answer(request.json['query'])
    return jsonify(response)

@app.route('/delete', methods=['GET'])
def delete():
    delete_collection()
    return jsonify("success")

if __name__=="__main__":
    app.run(debug=True)
