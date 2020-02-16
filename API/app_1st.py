from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

#print(__name__)

stores = [
    {
'name': 'My Store 1',
'items': [{
    'name': 'item1',
    'price': 16.00
        }
    ]
    },
    {
'name': 'My Store 2',
'items': [{
    'name': 'item2A',
    'price': 17.00
        },
    {
    'name': 'item2B',
    'price': 18.00
        }
    ]
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    #print(request_data)
    new_store = {
    'name': request_data['name'],
    'items': []
    }
    stores.append(new_store)
    return jsonify({"message": "Successfully added new store"})

@app.route('/store/<string:name>/items', methods=['POST'])
def add_items(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)

    return jsonify({"message": "Store not found. Add store first"})


@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})  #list converted to dict passed as json

@app.route('/store/<string:name>')
def list_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)    #dict passed as json

@app.route('/store/<string:name>/items')
def get_items(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})

    return jsonify({"message": "Store not found"})
