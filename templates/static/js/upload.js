// Check if game is already uploaded
async function checkGameStatus() {
    try {
        const response = await fetch('/game-status');
        
        if (!response.ok) {
            throw new Error('Failed to get game status');
        }
        
        const data = await response.json();
        const gameStatus = document.getElementById('game-status');
        
        if (data.installed) {
            let title = data.title || "Unknown Game";
            gameStatus.innerHTML = `
                <div class="game-title">${title}</div>
                <strong>Status:</strong> Game is currently installed and available at 
                <a href="/play" target="_blank">/play</a>. 
                <br>Uploading a new game will replace the existing one.
            `;
            gameStatus.className = 'game-status game-installed';
        } else {
            gameStatus.innerHTML = `
                <strong>Game Status:</strong> No game is currently installed. 
                Please upload a game ZIP file.
            `;
            gameStatus.className = 'game-status game-not-installed';
        }
    } catch (error) {
        console.error("Error checking game status:", error);
        document.getElementById('game-status').innerHTML = `
            <strong>Game Status:</strong> Could not determine if a game is installed.
        `;
        document.getElementById('game-status').className = 'game-status info';
    }
}

// Function to display messages
function showMessage(text, type) {
    const messageBox = document.getElementById('message-box');
    messageBox.innerHTML = text;
    messageBox.style.display = 'block';
    
    messageBox.className = 'message';
    if (type) {
        messageBox.classList.add(type);
    }
    
    // Scroll to message
    messageBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Initialize event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check for game on page load
    checkGameStatus();

    // Handle file selection
    document.getElementById('game-zip').addEventListener('change', function() {
        const uploadButton = document.getElementById('upload-button');
        const fileNameDisplay = document.getElementById('file-name');
        
        if (this.files[0]) {
            const fileName = this.files[0].name;
            fileNameDisplay.textContent = fileName;
            fileNameDisplay.style.fontWeight = 'bold';
            
            // Only enable upload if it's a zip file
            if (fileName.toLowerCase().endsWith('.zip')) {
                uploadButton.disabled = false;
            } else {
                uploadButton.disabled = true;
                showMessage('Please select a ZIP file.', 'error');
            }
        } else {
            fileNameDisplay.textContent = 'No file selected';
            fileNameDisplay.style.fontWeight = 'normal';
            uploadButton.disabled = true;
        }
    });

    // Handle form submission
    document.getElementById('upload-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const fileInput = document.getElementById('game-zip');
        if (!fileInput.files[0]) {
            showMessage('Please select a ZIP file first.', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            const uploadButton = document.getElementById('upload-button');
            uploadButton.disabled = true;
            uploadButton.textContent = 'Uploading...';
            
            showMessage('Uploading and extracting game files... This may take a moment.', 'info');
            
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            uploadButton.textContent = 'Upload Game';
            
            if (!response.ok) {
                uploadButton.disabled = false;
                throw new Error(result.detail || 'Upload failed');
            }
            
            let gameTitle = result.title || "Game";
            showMessage(`"${gameTitle}" uploaded successfully! You can now access it at <a href="/play" target="_blank">/play</a>`, 'success');
            
            // Update game status after successful upload
            checkGameStatus();
            
            // Reset the form
            document.getElementById('file-name').textContent = 'No file selected';
            document.getElementById('upload-button').disabled = true;
            fileInput.value = '';
        } catch (error) {
            showMessage(`Error: ${error.message}`, 'error');
        }
    });
});