import pymongo

# ==============================================================================
# تم وضع رابط الاتصال الخاص بك هنا مع تحديد اسم قاعدة البيانات
# ==============================================================================
CONNECTION_STRING = "mongodb+srv://abdullahmuhammadfawzy244_db_user:d5F7VzJz8OpK53hz@cluster0.iurjyo7.mongodb.net/fusion_search_db?retryWrites=true&w=majority&appName=Cluster0"
# ==============================================================================


# هذه هي البيانات التي سنضيفها (مثال)
# يمكنك إضافة المزيد من المواقع هنا
websites_data = [
    {
        "title": "Snapchat - The fastest way to share a moment!",
        "link": "https://www.snapchat.com/",
        "description": "Snapchat lets you easily talk with friends, view Live Stories from around the world, and explore news in Discover."
    },
    {
        "title": "Google Search",
        "link": "https://www.google.com/",
        "description": "The most popular search engine in the world."
    },
    {
        "title": "Python Programming Language - Official Website",
        "link": "https://www.python.org/",
        "description": "The official website for Python, a versatile and popular programming language."
    }
]

# الكود الخاص بالاتصال وإضافة البيانات
client = None  # نهيئ المتغير خارج الـ try
try:
    # 1. الاتصال بقاعدة البيانات
    client = pymongo.MongoClient(CONNECTION_STRING)

    # 2. تحديد قاعدة البيانات والمجموعة (Collection)
    # ملاحظة: تأكد من أن تطبيق الويب الخاص بك يبحث في نفس قاعدة البيانات والمجموعة
    db = client['fusion_search_db']  # اسم قاعدة البيانات
    collection = db['websites']  # اسم المجموعة التي ستخزن فيها المواقع

    # 3. حذف البيانات القديمة (اختياري، لتجنب التكرار عند التشغيل مرة أخرى)
    collection.delete_many({})
    print("Old data deleted successfully.")

    # 4. إضافة البيانات الجديدة
    collection.insert_many(websites_data)

    print(f"Success! {len(websites_data)} websites have been added to the database.")
    print("Database 'fusion_search_db' and collection 'websites' are now ready.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # 5. إغلاق الاتصال دائمًا
    if client:
        client.close()
        print("Connection to MongoDB closed.")
