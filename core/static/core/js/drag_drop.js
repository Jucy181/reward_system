// drag_drop.js

let dropArea = document.getElementById("drop-area");

// Highlight drop area when file is over
dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.classList.add("highlight");
});

// Remove highlight when file leaves
dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("highlight");
});

// Handle file drop
dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove("highlight");

    const files = e.dataTransfer.files;
    handleFiles(files);
});

// Handle file selection
document.getElementById("fileElem").addEventListener("change", (e) => {
    handleFiles(e.target.files);
});

// Function to handle files
function handleFiles(files) {
    for (let i = 0; i < files.length; i++) {
        console.log("File dropped:", files[i].name);
         formData.append('screenshot', file);
        formData.append('app_name', 'Example App'); // Replace dynamically if needed

        fetch('/api/upload-screenshot/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // Important for CSRF
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => console.log('Upload success:', data))
        .catch(error => console.error('Upload error:', error));
    }
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
