from flask import Flask, render_template, request
from pymongo import MongoClient
import os

# --- رابط الاتصال الخاص بك مدمج هنا ---
CONNECTION_STRING = "mongodb+srv://abdullahmuhammadfawzy244_db_user:d5F7VzJz8OpK53hz@cluster0.iurjyo7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# --------------------------------------------------------

app = Flask(__name__)

# إعداد الاتصال بقاعدة البيانات
try:
    client = MongoClient(CONNECTION_STRING)
    db = client['fusion_search_db']
    collection = db['articles']
    # التحقق من نجاح الاتصال
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

    # للتأكد من أن الخادم يعمل على Render
    # قم بتشغيل الخادم باستخدام gunicorn وليس app.run()
    # تأكد أن أمر التشغيل في Render هو: gunicorn search_engine.search_server:app
    print("Application is running...")



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port)
