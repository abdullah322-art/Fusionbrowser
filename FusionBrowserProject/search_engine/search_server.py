# File: search_engine/search_server.py
from flask import Flask, render_template, request
from serpapi import GoogleSearch
import os

# لقد قمنا فقط بتنظيف الكود من أي مسافات خاطئة
SERPAPI_API_KEY = "12a39798f9404fd1828ec01bfe682428674f4dea"

app = Flask(__name__)

@app.route('/search')
def search():
    # الحصول على كلمة البحث من الرابط
    query = request.args.get('q', '')
    results_list = []

    # إذا كان هناك كلمة للبحث عنها
    if query:
        try:
            params = {
              "q": query,
              "api_key": SERPAPI_API_KEY,
              "engine": "google",
            }

            google_search = GoogleSearch(params)
            results = google_search.get_dict()
            
            # استخراج نتائج البحث العضوية
            if 'organic_results' in results:
                results_list = results['organic_results']

        except Exception as e:
            print(f"حدث خطأ: {e}")

    # عرض النتائج في صفحة HTML
    # (تأكد من أن لديك ملف HTML بهذا الاسم)
    return render_template('search_results.html', results=results_list)
