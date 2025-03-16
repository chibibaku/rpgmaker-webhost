from flask import Flask, send_from_directory, request, jsonify, render_template
import os
import zipfile
import shutil
import json

app = Flask(__name__,
            template_folder="templates",
            static_folder="templates/static")

# Path to the game files
GAME_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'game')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure the game directory exists
os.makedirs(GAME_PATH, exist_ok=True)

@app.route('/')
def upload_form():
    """Serve the upload form"""
    return render_template("upload.html")

@app.route('/play')
def index():
    """Serve the index.html file"""
    if os.path.exists(os.path.join(GAME_PATH, 'index.html')):
        return send_from_directory(GAME_PATH, 'index.html')
    
    if os.path.exists(os.path.join(ROOT_DIR, 'index.html')):
        return send_from_directory(ROOT_DIR, 'index.html')
    
    return "Game not installed", 404

@app.route('/game-status')
def game_status():
    """Check if game is installed and get game title"""
    index_exists = os.path.exists(os.path.join(GAME_PATH, 'index.html'))
    
    game_title = "Unknown Game"
    package_json_path = os.path.join(GAME_PATH, 'package.json')
    
    if os.path.exists(package_json_path):
        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
                if package_data.get('window', {}).get('title'):
                    game_title = package_data['window']['title']
                elif package_data.get('name'):
                    game_title = package_data['name']
        except Exception as e:
            print(f"Error reading package.json: {e}")
    
    return jsonify({
        "installed": index_exists,
        "title": game_title
    })

@app.route('/upload', methods=['POST'])
def upload_game():
    """Handle game upload"""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if not file.filename.endswith('.zip'):
        return jsonify({"error": "Only ZIP files are allowed"}), 400
    
    # Save the uploaded zip temporarily
    temp_zip = os.path.join(ROOT_DIR, "temp.zip")
    file.save(temp_zip)
    
    try:
        # Clear the game directory
        if os.path.exists(GAME_PATH):
            shutil.rmtree(GAME_PATH)
        os.makedirs(GAME_PATH, exist_ok=True)
        
        # Extract the zip to the game directory
        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
            zip_ref.extractall(GAME_PATH)
            
        # Remove the temporary zip file
        os.remove(temp_zip)
        
        # Get game title from package.json if available
        game_title = "Unknown Game"
        package_json_path = os.path.join(GAME_PATH, 'package.json')
        if os.path.exists(package_json_path):
            try:
                with open(package_json_path, 'r', encoding='utf-8') as f:
                    package_data = json.load(f)
                    if package_data.get('window', {}).get('title'):
                        game_title = package_data['window']['title']
                    elif package_data.get('name'):
                        game_title = package_data['name']
            except Exception as e:
                print(f"Error reading package.json: {e}")
        
        return jsonify({
            "message": "Game uploaded and extracted successfully", 
            "title": game_title
        })
    except Exception as e:
        return jsonify({"error": f"Error extracting game: {str(e)}"}), 500

@app.route('/<path:path>')
def serve_file(path):
    """Serve any requested file from either root or game directory"""
    # Check if the requested file is in the root directory
    root_path = os.path.join(ROOT_DIR, path)
    if os.path.exists(root_path) and os.path.isfile(root_path):
        return send_from_directory(ROOT_DIR, path)
    
    # Otherwise check in the game directory
    game_path = os.path.join(GAME_PATH, path)
    if os.path.exists(game_path) and os.path.isfile(game_path):
        return send_from_directory(GAME_PATH, path)
    
    return "File not found", 404


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', debug=True)