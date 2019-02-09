from flask import Flask, request, abort, make_response
from flask_cors import CORS
import json
from utils import get_malayalam_model, get_tamil_model


app = Flask(__name__)
cors = CORS(app)
ml_model = get_malayalam_model()
ta_model = get_tamil_model()



def get_similar(lang, word):
    if lang == 'ml':
        similar = ml_model.wv.most_similar(word, topn=10)
        not_similar = ml_model.wv.most_similar(negative=word, topn=10)[::-1]
        result = {
                    'similar': similar,
                    'not_similar': not_similar
                }
        return result
    elif lang == 'ta':
        result = ta_model[word]
        return result



@app.route("/")
def home():
    return "Hello, IndicNLP!"

@app.route("/similar/<lang>/", methods=['POST'])
def w2v(lang):
    data = request.json
    try:
        if data.get('word',None):
            try:
                
                result = get_similar(lang, data['word'].strip())
                # similar = model.wv.most_similar(data['word'], topn=10)
                # not_similar = model.wv.most_similar(negative=[data['word']], topn=10)[::-1]
                # result = {
                #     'similar': similar,
                #     'not_similar': not_similar
                # }
            except KeyError:
                return 'Not in vocab'
            return make_response(json.dumps(result))
        else:
            return abort(404)
    except AttributeError:
        return abort(500,{'reponse':'Incorrect application format'})
        
@app.route("/compare/", methods=['POST'])
def compare():
    data = request.json
    try:
        if data['positive'] and data['negative']:
            positive, negative = data['positive'], data['negative']
            if positive:
                try:
                    result = ml_model.wv.most_similar(positive=positive,negative=negative,topn=3)
                except KeyError:
                    return 'Not in vocab'
            return make_response(json.dumps(result))
        else:
            return abort(404)
    except AttributeError:
        return abort(500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8400, debug=True)
