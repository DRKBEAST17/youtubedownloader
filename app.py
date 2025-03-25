from flask import Flask, request, render_template_string, send_file
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

# Ensure the "downloads" folder exists
if not os.path.exists("downloads"):
    os.makedirs("downloads")

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Downloader</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Poppins', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }

        #bg-gif {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('https://i.pinimg.com/originals/5b/e7/14/5be714881bbe562fb5e51c24ae773159.gif') no-repeat center center;
            background-size: cover;
            z-index: -1;
        }

        .container {
            background: rgba(255, 255, 255, 0.9);
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            text-align: center;
            width: 90%;
            max-width: 500px;
        }

        h1 {
            font-size: 2rem;
            margin-bottom: 1rem;
            color: #333;
        }

        /* Button Styles from Uiverse.io */
        .youtube-button {
            position: relative;
            overflow: hidden;
            height: 3rem;
            padding: 0 2rem;
            border-radius: 1.5rem;
            background: #3d3a4e;
            background-size: 400%;
            color: #fff;
            border: none;
            cursor: pointer;
            font-size: 1rem;
            width: 100%;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }

        .youtube-button:hover::before {
            transform: scaleX(1);
        }

        .youtube-button::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            transform: scaleX(0);
            transform-origin: 0 50%;
            width: 100%;
            height: inherit;
            border-radius: inherit;
            background: linear-gradient(
                82.3deg,
                rgba(150, 93, 233, 1) 10.8%,
                rgba(99, 88, 238, 1) 94.3%
            );
            transition: all 0.475s;
        }

        input, select {
            width: 100%;
            padding: 0.75rem;
            margin-bottom: 1rem;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 1rem;
        }

        #progress-container {
            margin-top: 1rem;
            display: none;
        }

        #progress-bar {
            width: 100%;
            height: 10px;
            background: #ddd;
            border-radius: 5px;
            overflow: hidden;
        }

        #progress-bar div {
            height: 100%;
            width: 0;
            background: #ff4757;
            transition: width 0.3s ease;
        }

        #progress-text {
            display: block;
            margin-top: 0.5rem;
            font-size: 0.9rem;
        }

        .contact {
            margin-top: 1.5rem;
            font-size: 0.9rem;
        }

        .contact a {
            color: #ff4757;
            text-decoration: none;
        }

        .contact a:hover {
            text-decoration: underline;
        }

        /* Telegram Button Styles */
        .telegram {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: #0088cc;
            color: #fff;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            transition: background 0.3s ease;
        }

        .telegram:hover {
            background: #0077b5;
        }

        .telegram-svg {
            width: 20px;
            height: 20px;
            margin-right: 0.5rem;
        }

        @media (max-width: 600px) {
            h1 {
                font-size: 1.5rem;
            }

            input, select, .youtube-button {
                font-size: 0.9rem;
            }
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Background GIF -->
    <div id="bg-gif"></div>

    <!-- Main Content -->
    <div class="container">
        <!-- YouTube Button -->
        <button class="youtube-button">
            <span>YouTube</span>
        </button>

        <h1>YouTube Downloader</h1>
        <form id="download-form">
            <input type="text" id="url" name="url" placeholder="Enter YouTube URL" required>
            <select id="quality" name="quality">
                <option value="144p">144p</option>
                <option value="360p">360p</option>
                <option value="720p">720p</option>
                <option value="1080p">1080p</option>
                <option value="1440p">1440p (2K)</option>
                <option value="4K">4K</option>
            </select>
            <button type="submit" class="youtube-button">
                <span>Download</span>
            </button>
        </form>

        <!-- Progress Bar -->
        <div id="progress-container">
            <div id="progress-bar"><div></div></div>
            <span id="progress-text">0%</span>
        </div>

        <!-- Telegram Button -->
        <a href="https://t.me/GAMECHANGER17" target="_blank" rel="noopener noreferrer">
            <button class="telegram">
                <svg
                    style="fill:#FFFFFF;"
                    class="telegram-svg"
                    viewBox="0,0,256,256"
                    y="0px"
                    x="0px"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <g
                        style="mix-blend-mode: normal"
                        text-anchor="none"
                        font-size="none"
                        font-weight="none"
                        font-family="none"
                        stroke-dashoffset="0"
                        stroke-dasharray=""
                        stroke-miterlimit="10"
                        stroke-linejoin="miter"
                        stroke-linecap="butt"
                        stroke-width="1"
                        stroke="none"
                        fill-rule="nonzero"
                        fill="#ffffff"
                    >
                        <g transform="scale(5.12,5.12)">
                            <path
                                d="M46.137,6.552c-0.75,-0.636 -1.928,-0.727 -3.146,-0.238h-0.002c-1.281,0.514 -36.261,15.518 -37.685,16.131c-0.259,0.09 -2.521,0.934 -2.288,2.814c0.208,1.695 2.026,2.397 2.248,2.478l8.893,3.045c0.59,1.964 2.765,9.21 3.246,10.758c0.3,0.965 0.789,2.233 1.646,2.494c0.752,0.29 1.5,0.025 1.984,-0.355l5.437,-5.043l8.777,6.845l0.209,0.125c0.596,0.264 1.167,0.396 1.712,0.396c0.421,0 0.825,-0.079 1.211,-0.237c1.315,-0.54 1.841,-1.793 1.896,-1.935l6.556,-34.077c0.4,-1.82 -0.156,-2.746 -0.694,-3.201zM22,32l-3,8l-3,-10l23,-17z"
                            ></path>
                        </g>
                    </g>
                </svg>
                <span class="telegram-text">Telegram</span>
            </button>
        </a>
    </div>

    <script>
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
    </script>
</body>
</html>
    ''')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    quality = request.form['quality']

    # Map quality to yt-dlp format
    format_map = {
        '144p': 'worst',          # Lowest quality (144p)
        '360p': '18',             # 360p
        '720p': '22',             # 720p
        '1080p': '137+140',       # 1080p video + audio
        '1440p': '400+140',       # 1440p (2K) video + audio
        '4K': '313+140',          # 4K video + audio
    }
    ydl_opts = {
        'format': format_map.get(quality, 'best'),
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',  # Merge video and audio into mp4
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)