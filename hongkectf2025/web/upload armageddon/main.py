from flask import Flask, request, render_template
import os

app = Flask(__name__)
SANDBOX_PATH = "/var/sandbox/"
ALLOWED_EXT = {'upload'}
BLACKLIST = ['php', 'sh', 'py']

def check_file(filename):
    ext = filename.rsplit('.', 1)[-1]
    if any(b in filename.lower() for b in BLACKLIST):
        return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if not file:
        return "No file uploaded", 400
    if file.filename == '':
        return '文件名为空', 400
    if not check_file(file.filename):
        return "Invalid file type", 403
    save_path = os.path.join(SANDBOX_PATH, file.filename.split('\x00')[0])
    file.save(save_path)
    return f"File saved at {save_path} , flag in export~~~", 200       

@app.route('/execute')
def execute():
    path = request.args.get('file', '')
    safe_path = os.path.join(SANDBOX_PATH, path)

    if not os.path.exists(safe_path):
        return "File not found", 404

    os.system(f"timeout 3 python3 {safe_path}")
    return "Execution completed", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
