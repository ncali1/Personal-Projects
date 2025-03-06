from flask import Flask, request, redirect, url_for, render_template, jsonify

app = Flask(__name__)

# Dummy user data for authentication
users = {
    "user1": "PGurSUm",
    "user2": "password2"
}

@app.route('/')
def index():
    return render_template('landingpage.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username] == password:
        return redirect(url_for('chat'))
    else:
        return render_template('landingpage.html', error="Invalid credentials, please try again.")

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat_message():
    user_message = request.json.get('message')
    # Here you would integrate with your AI model to generate a response
    # For demonstration, we'll just echo the message back
    bot_response = f"Echo: {user_message}"
    return jsonify(response=bot_response)

if __name__ == "__main__":
    app.run(debug=True)