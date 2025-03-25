document.getElementById('download-form').addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent the default form submission

    // Get form data
    const url = document.getElementById('url').value;
    const quality = document.getElementById('quality').value;

    // Show progress bar
    const progressContainer = document.getElementById('progress-container');
    const progressBar = document.getElementById('progress-bar').querySelector('div');
    const progressText = document.getElementById('progress-text');
    progressContainer.style.display = 'block';

    try {
        // Send a POST request to the backend
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `url=${encodeURIComponent(url)}&quality=${encodeURIComponent(quality)}`,
        });

        if (response.ok) {
            // Convert the response to a Blob (binary data)
            const blob = await response.blob();

            // Create a download link
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = 'video.mp4'; // Default filename
            document.body.appendChild(a);
            a.click(); // Trigger the download
            a.remove(); // Clean up

            // Reset progress bar
            progressBar.style.width = '0';
            progressText.textContent = '0%';
        } else {
            alert('Failed to download video. Please check the URL and try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    } finally {
        // Hide progress bar
        progressContainer.style.display = 'none';
    }
});

// Function to update the progress bar (optional, for real-time progress)
function updateProgressBar(progress) {
    const progressBar = document.getElementById('progress-bar').querySelector('div');
    const progressText = document.getElementById('progress-text');
    progressBar.style.width = `${progress}%`;
    progressText.textContent = `${progress}%`;
}