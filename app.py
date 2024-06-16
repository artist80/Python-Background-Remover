from flask import Flask, render_template, request, send_file
import requests
import os

app = Flask(__name__)

# Replace 'YOUR_API_KEY' with your remove.bg API key
API_KEY = 'Enter-Your-API-Key-From-Remove-BG-Website'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file.save(file.filename)
        remove_bg(file.filename)
        return render_template('index.html', success=True, filename=file.filename)

def remove_bg(filename):
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(filename, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': API_KEY},
    )
    if response.status_code == requests.codes.ok:
        with open('static/no_bg_' + filename, 'wb') as out:
            out.write(response.content)

@app.route('/download')
def download():
    filename = 'no_bg_' + request.args.get('filename')
    return send_file('static/' + filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
