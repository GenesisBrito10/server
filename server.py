from flask import Flask, request
from pymongo import MongoClient
import requests

app = Flask(__name__)


client = MongoClient('mongodb+srv://invictvs:oytmvb9m1zysmc44@cluster0.o10z4.mongodb.net/')
db = client['primepag']
collection = db['pagamentos']



@app.route('/pagamentos', methods=['POST'])
def pagamentos():
    
    id_pix = request.json['message']['reference_code']
    
    dados = collection.find_one_and_update({'gateway_id': id_pix}, {'$set': {'status': 'paid'}})
    if dados:
        dados['_id'] = str(dados['_id'])
        
        requests.post(dados['url'], json=dados)
        return 'ok',200
    
    return 'not found', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=27002)