from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

# MongoDB connection
client = MongoClient('mongodb+srv://MuhammadRizkySamuel:123@cluster0.yxozh.mongodb.net/')
db = client.dbsparta

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# POST request to create a new bucket list item
@app.route("/bucket", methods=["POST"])
def bucket_post():
    sample_receive = request.form['sample_give']
    print(sample_receive)  # Debugging

    # Inserting the new item into the MongoDB
    doc = {
        'item': sample_receive,  # The bucket list item
        'done': False  # Default value for 'done' status
    }
    db.bucketlist.insert_one(doc)

    return jsonify({'msg': 'Item saved successfully!'})

# POST request to mark an item as done
@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    sample_receive = request.form['sample_give']
    print(sample_receive)  # Debugging

    # Update the item in the MongoDB database to mark it as done
    db.bucketlist.update_one({'item': sample_receive}, {'$set': {'done': True}})
    return jsonify({'msg': 'Item marked as done!'})

# POST request to delete a bucket list item
@app.route("/bucket/delete", methods=["POST"])
def bucket_delete():
    item_receive = request.form['item_give']
    print(item_receive)  # Debugging

    # Delete the item from the MongoDB database
    db.bucketlist.delete_one({'item': item_receive})

    return jsonify({'msg': 'Item deleted successfully!'})

# GET request to retrieve all bucket list items
@app.route("/bucket", methods=["GET"])
def bucket_get():
    # Retrieve all items from the MongoDB collection
    bucketlist_items = list(db.bucketlist.find({}, {'_id': False}))  # Excluding the _id field
    return jsonify({'items': bucketlist_items})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
