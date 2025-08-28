# File: search_engine/search_server.py

from flask import Flask, render_template, request
import requests  # سنستخدم مكتبة requests مباشرة
import os

# --- مفتاحك السري مدمج هنا وجاهز للعمل ---
SERPAPI_API_KEY = "12a39798f9404fd1828ec01bfe682428674f4dea"
SERPAPI_ENDPOINT = "https://serpapi.com/search.json"  # الرابط المباشر للخدمة
# --------------------------------------------------------

app = Flask(__name__)


@app.route('/search')
def search():
    query = request.args.get('q', '')
    results_list = []

    if query:
        # إعداد البارامترات للطلب
        params = {
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "engine": "google",
            "google_domain": "google.com",
            "gl": "sa",
            "hl": "ar"
        }

        try:
            # إرسال الطلب باستخدام مكتبة requests
            response = requests.get(SERPAPI_ENDPOINT, params=params, timeout=10)  # أضفنا مهلة 10 ثوانٍ
            response.raise_for_status()  # التأكد من نجاح الطلب

            search_results = response.json()

            # استخلاص النتائج
            if "organic_results" in search_results:
                for result in search_results["organic_results"]:
                    results_list.append({
                        'title': result.get('title', ''),
                        'url': result.get('link', ''),
                        'text': result.get('snippet', 'No snippet available.')
                    })

        except requests.exceptions.RequestException as e:
            # طباعة خطأ أكثر تفصيلاً إذا فشل الاتصال
            print(f"Error connecting to SerpApi: {e}")
        except Exception as e:
            print(f"An error occurred while processing results: {e}")

    return render_template('results.html', query=query, results=results_list)


@app.route('/')
def home():
    return render_template('results.html', query='', results=[])


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)