// drag_drop.js

let dropArea = document.getElementById("drop-area");
let gallery = document.getElementById("gallery");

// Prevent default browser behavior for drag/drop on dropArea AND document
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Highlight drop area when file is over
dropArea.addEventListener("dragover", () => {
    dropArea.classList.add("highlight");
});

// Remove highlight when file leaves
dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("highlight");
});

// Handle file drop
dropArea.addEventListener("drop", (e) => {
    dropArea.classList.remove("highlight");
    let files = e.dataTransfer.files;
    handleFiles(files);
});

// Handle file selection via button
document.getElementById("fileElem").addEventListener("change", (e) => {
    handleFiles(e.target.files);
});

// Handle files: show preview and upload
function handleFiles(files) {
    for (let i = 0; i < files.length; i++) {
        let file = files[i];

        // Show preview
        previewFile(file);

        // Upload to Django
        uploadFile(file);
    }
}

// Function to show image preview
function previewFile(file) {
    let reader = new FileReader();
    reader.readAsDataURL(file);

    reader.onloadend = function() {
        let img = document.createElement('img');
        img.src = reader.result;
        gallery.appendChild(img);
    }
}

// Function to upload file to Django
function uploadFile(file) {
    let formData = new FormData();
    formData.append('screenshot', file);
    formData.append('app_name', 'Example App'); // replace dynamically if needed

    fetch('/api/upload-screenshot/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken') // CSRF for Django
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => console.log('Upload success:', data))
    .catch(error => console.error('Upload error:', error));
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
