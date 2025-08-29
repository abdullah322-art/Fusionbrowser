    # File: search_engine/search_server.py
    from flask import Flask, render_template, request
    from serpapi import GoogleSearch
    import os
    # --- مفتاحك السري مدمج هنا وجاهز للعمل ---
    SERPAPI_API_KEY = "12a39798f9404fd1828ec01bfe682428674f4dea"
    # --------------------------------------------------------

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
                    "google_domain": "google.com",
                    "gl": "sa",
                    "hl": "ar"
                }
                
                search_results = GoogleSearch(params).get_dict()
                
                if "organic_results" in search_results:
                    for result in search_results["organic_results"]:
                        results_list.append({
                            'title': result.get('title', ''),
                            'url': result.get('link', ''),
                            'text': result.get('snippet', 'No snippet available.')
                        })
                            
            except Exception as e:
                print(f"An error occurred while calling SerpApi: {e}")

        return render_template('results.html', query=query, results=results_list)

    @app.route('/')
    def home():
        return render_template('results.html', query='', results=[])

    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)

