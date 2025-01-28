// Function to handle file upload
function handleFile(file) {
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const uploadedImg = document.getElementById('uploaded-img');
            uploadedImg.src = e.target.result;
            document.getElementById('image-container').style.display = 'flex'; // Show the image container
            document.getElementById('predict-btn').style.display = 'block'; // Show the predict button
        };
        reader.readAsDataURL(file);
    }
}

// Function to handle dragover event
document.getElementById('upload-box').addEventListener('dragover', function(e) {
    e.preventDefault();
    document.getElementById('drop-text').textContent = "Drop the file";
});

// Function to handle dragleave event
document.getElementById('upload-box').addEventListener('dragleave', function(e) {
    e.preventDefault();
    document.getElementById('drop-text').textContent = "or drop a file here";
});

// Function to handle drop event
document.getElementById('upload-box').addEventListener('drop', function(e) {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    handleFile(file);
});

// Function to handle paste event
// Function to handle paste event
document.addEventListener('paste', function(e) {
    const items = e.clipboardData.items;
    for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf("image") !== -1) {
            const blob = items[i].getAsFile();
            const reader = new FileReader();
            reader.onload = function(event) {
                const pastedImageDataUrl = event.target.result;
                const pastedImageFile = dataURLtoFile(pastedImageDataUrl, "pasted_image.png");
                handleFile(pastedImageFile);
            };
            reader.readAsDataURL(blob);
            break;
        }
    }
});

// Function to convert data URL to File object
function dataURLtoFile(dataUrl, filename) {
    const arr = dataUrl.split(',');
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, { type: mime });
}



// Function to handle file input change
document.getElementById('file-input').addEventListener('change', function(e) {
    const file = e.target.files[0];
    handleFile(file);
});

// Function to handle predict button click
document.getElementById('predict-btn').addEventListener('click', function() {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        // Show the result container
        const resultContainer = document.getElementById('result-container');
        resultContainer.style.display = 'block';

        // Update result container with loading message
        resultContainer.innerText = 'Predicting...';

        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.result) {
                // Update result container with the predicted disease
                resultContainer.innerText = `Predicted Result: ${data.result}`;
            } else {
                resultContainer.innerText = 'No result available.';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultContainer.innerText = 'An error occurred. Please try again.';
        });
    } else {
        console.error('No file selected.');
        document.getElementById('result-container').innerText = 'Please upload a file first.';
    }
});

