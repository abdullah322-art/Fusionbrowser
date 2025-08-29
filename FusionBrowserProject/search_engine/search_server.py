# File: search_engine/search_server.py
import os
from flask import Flask, render_template, request
from serpapi import GoogleSearch

# --- التحسين: قراءة المفتاح السري من متغيرات البيئة بدلاً من كتابته مباشرة ---
# هذه الطريقة أكثر أمانًا، خاصة عند رفع الكود على منصات مثل GitHub.
SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY")

# التأكد من أن المفتاح موجود
if not SERPAPI_API_KEY:
    raise ValueError("لم يتم العثور على SERPAPI_API_KEY. يرجى تعيينه كمتغير بيئة.")

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    results_list = []

    if query:
        try:
            params = {
              "q": query,
              "api_key": SERPAPI_API_KEY,
              "engine": "google",
              # يمكنك إضافة المزيد من الإعدادات هنا حسب الحاجة
              # "location": "Riyadh, Saudi Arabia",
              # "hl": "ar",
              # "gl": "sa"
            }

            search = GoogleSearch(params)
            results = search.get_dict()
            
            # (هذا الجزء قد تحتاج لتعديله حسب شكل النتائج التي تريد عرضها)
            if 'organic_results' in results:
                results_list = results['organic_results']

        except Exception as e:
            print(f"An error occurred: {e}")
            # يمكنك التعامل مع الخطأ هنا، مثلاً عرض رسالة للمستخدم
            pass

    # يفترض أن لديك ملف HTML اسمه 'search_results.html' لعرض النتائج
    return render_template('search_results.html', query=query, results=results_list)

# هذا الجزء ضروري إذا كنت تريد تشغيل التطبيق محليًا للاختبار
if __name__ == '__main__':
    # سيتم تشغيل الخادم على المنفذ 5000 افتراضيًا
    app.run(debug=True)
