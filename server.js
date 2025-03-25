const express = require('express');
const ytdl = require('ytdl-core');
const cors = require('cors');
const app = express();
const port = 5000;

// Enable CORS
app.use(cors());

// Download endpoint
app.get('/download', async (req, res) => {
  const videoURL = req.query.url;
  const quality = req.query.quality || 'highest';

  try {
    // Validate YouTube URL
    if (!ytdl.validateURL(videoURL)) {
      return res.status(400).send('Invalid YouTube URL');
    }

    // Get video info
    const info = await ytdl.getInfo(videoURL);
    const title = info.videoDetails.title.replace(/[^a-zA-Z0-9]/g, '_'); // Sanitize title

    // Set headers for download
    res.header('Content-Disposition', `attachment; filename="${title}.mp4"`);

    // Stream video to client
    ytdl(videoURL, { quality: quality })
      .pipe(res)
      .on('error', (err) => {
        console.error(err);
        res.status(500).send('Error downloading video');
      });
  } catch (err) {
    console.error(err);
    res.status(500).send('Error processing request');
  }
});

// Start server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});