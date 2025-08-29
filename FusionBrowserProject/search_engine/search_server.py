from flask import Flask, render_template, request
from pymongo import MongoClient
import os

# --- Your Connection String is embedded here ---
# تأكد أن هذا الرابط صحيح ويحتوي على اسم المستخدم وكلمة المرور الخاصة بك
CONNECTION_STRING = "mongodb+srv://abdullahmuhammadfawzy244_db_user:d5F7VzJz8OpK53hz@cluster0.iurjyo7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# --------------------------------------------------------

app = Flask(__name__)

# Setting up the database connection
try:
    client = MongoClient(CONNECTION_STRING)
    db = client['fusion_search_db']
    collection = db['articles']
    # Check if the connection is successful
    client.admin.command('ping')
    print("Success: You are now connected to MongoDB Atlas!")
except Exception as e:
    print(f"Error: Could not connect to MongoDB Atlas. Check your CONNECTION_STRING. Error details: {e}")
    client = None


@app.route('/search')
def search():
    query = request.args.get('q', '')
    results_list = []

    if client and query:
        try:
            search_stage = {
                '$search': {
                    'index': 'default',
                    'text': {
                        'query': query,
                        'path': {'wildcard': '*'},
                        'fuzzy': {'maxEdits': 1}
                    }
                }
            }
            limit_stage = {'$limit': 20}
            results = collection.aggregate([search_stage, limit_stage])
            results_list = list(results)
        except Exception as e:
            print(f"An error occurred during search: {e}")

    return render_template('results.html', query=query, results=results_list)


@app.route('/')
def home():
    return render_template('results.html', query='', results=[])


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    # This part of the code is not used by Render.
    # It is a good practice to use gunicorn on production.
    # The start command on Render should be: gunicorn search_engine.search_server:app
    print("Application is running...")


