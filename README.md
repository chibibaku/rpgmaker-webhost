# RPG Maker Web Host

日本語版は[こちら](README.ja.md)

A simple web server for hosting RPG Maker MV/MZ games online. This project allows you to easily upload and deploy your RPG Maker games to the web through a user-friendly interface.

## Features

- Simple web interface for uploading RPG Maker games
- Automatic game extraction from ZIP files
- Game title detection from package.json
- Immediate game availability after upload
- Support for RPG Maker MV/MZ game formats

## Main Files

- **server.py**  
  Flask server implementation handling uploads and serving game files.
- **upload.html / upload.js**  
  Frontend interface for uploading game ZIP files.
- **requirements.txt**  
  Dependencies list, installable via `pip install -r requirements.txt`.

## Getting Started

### Prerequisites

- Python 3.6+
- pip (Python package manager)

### Installation

1. Clone this repository or download the source code
2. Install the required dependencies:
  ```bash
  pip install -r requirements.txt
  ```
1. Start local server:
  ```bash
  python server.py
  ```

The server will be available at `http://localhost:5000`.

## Usage

1. Navigate to the root URL in your web browser
2. Package your RPG Maker MV/MZ game as a ZIP file
3. Click "Select ZIP File" to choose your game package
4. Upload your game using the provided interface
5. Once uploaded, access your game at `/play`

## Deploying to Render

This application is designed to be deployed to [Render](https://render.com). To deploy:

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `gunicorn server:app`
5. Deploy the service

## Future Enhancements

- User authentication for managing multiple games
- Individual save data handling per user
- Performance optimizations for large game files
- API for programmatic game deployment

## Technical Details

- Built with Flask (Python web framework)
- Uses a simple file-based storage system
- Handles ZIP extraction of game packages
- Serves static game files with proper content types

## License

- Undecided

## Acknowledgments

- RPG Maker MV/MZ developers
- Flask community