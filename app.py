import os
import psycopg2
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Database connection details from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'password')

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

HTML_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <title>HR Portal - internal</title>
    <style>
        body { font-family: 'Courier New', monospace; background: #0d1117; color: #58a6ff; padding: 40px; }
        .box { border: 1px solid #30363d; padding: 20px; margin-bottom: 20px; border-radius: 5px; }
        input { background: #0d1117; color: #c9d1d9; border: 1px solid #30363d; padding: 8px; }
        button { background: #238636; color: white; border: none; padding: 8px 15px; cursor: pointer; border-radius: 5px; }
        .danger { border-color: #f85149; }
        pre { background: #161b22; padding: 10px; color: #f0f6fc; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>HR Management System (v2.1.0-beta)</h1>
    
    <div class="box">
        <h3>Staff Search</h3>
        <form method="POST" action="/search">
            <input type="text" name="username" placeholder="Enter username...">
            <button type="submit">Search</button>
        </form>
    </div>

    <div class="box danger">
        <h3>Network Health Check</h3>
        <p><small>Warning: Internal use only. Pings the DB gateway.</small></p>
        <form method="POST" action="/ping">
            <input type="text" name="ip" value="127.0.0.1">
            <button type="submit">Run Diagnostics</button>
        </form>
    </div>

    {% if output %}
    <div class="box">
        <h3>System Output:</h3>
        <pre>{{ output }}</pre>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_LAYOUT)

@app.route('/search', methods=['POST'])
def search():
    username = request.form.get('username')
    # VULNERABILITY: String formatting for SQL queries (Classic SQLi)
    query = f"SELECT username, role FROM users WHERE username = '{username}';"
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return render_template_string(HTML_LAYOUT, output=str(results))
    except Exception as e:
        return render_template_string(HTML_LAYOUT, output=str(e))

@app.route('/ping', methods=['POST'])
def ping():
    ip = request.form.get('ip')
    # VULNERABILITY: Command Injection (RCE)
    command = f"ping -c 2 {ip}"
    output = os.popen(command).read()
    return render_template_string(HTML_LAYOUT, output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)