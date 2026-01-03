# 🎬 LAN Video Player

A lightweight, self-hosted video streaming application for your local network. Stream movies with subtitles from any device on your LAN without relying on external services.

## ✨ Features

- **LAN Streaming**: Stream videos to any device on your local network
- **Multiple Format Support**: Plays MP4, MKV, AVI, MOV, and WebM videos
- **Subtitle Support**: Automatically detects and displays SRT and VTT subtitles
- **Range Request Support**: Efficient streaming with HTTP range request support for seeking
- **Responsive UI**: Beautiful, mobile-friendly web interface
- **Playback Controls**: 
  - Play/Pause toggle
  - Rewind/Forward 5-second buttons
  - Keyboard shortcuts (Space, Arrow keys)
- **Automatic Movie Discovery**: Scans your Movies folder for video files and subtitles

## 🚀 Getting Started

### Requirements

- Python 3.13 or higher
- Flask
- Any modern web browser

### Installation

1. **Clone or download** this project to your desired location:
   ```bash
   cd Local-Movie-Server
   ```

2. **Install dependencies**:
   ```bash
   pip install flask
   ```

3. **Add your movies**:
   Create a `Movies` folder in the project root and organize your videos:
   ```
   Local-Movie-Server/
   ├── Movies/
   │   ├── Movie Name 1/
   │   │   ├── video.mp4
   │   │   └── subtitles.srt
   │   └── Movie Name 2/
   │       ├── video.mkv
   │       └── subtitles.vtt
   ```

4. **Start the server**:
   ```bash
   python app.py
   ```

5. **Access the player**:
   - On the same machine: Open `http://localhost:5000` in your browser
   - On another device: Use `http://<your-machine-ip>:5000`
   - To find your machine IP: Run `ipconfig` (Windows) or `ifconfig` (Linux/Mac)

## 📁 File Structure

```
Local-Movie-Server/
├── app.py                 # Flask server and routing
├── templates/
│   └── index.html         # Web UI and player
├── Movies/                # Your video files (auto-created)
└── README.md             # This file
```

## 🎮 Keyboard Shortcuts

When a video is playing:

| Key | Action |
|-----|--------|
| **Space** | Play/Pause |
| **← Arrow** | Rewind 5 seconds |
| **→ Arrow** | Forward 5 seconds |

## 🎯 Usage Tips

### Organizing Movies

- Each movie should be in its own folder within the `Movies` directory
- Folder names are used as movie titles (underscores converted to spaces)
- Each folder should contain exactly one video file
- Subtitles are optional but automatically detected if present

### Supported Formats

**Video**: `.mp4`, `.mkv`, `.avi`, `.mov`, `.webm`  
**Subtitles**: `.srt`, `.vtt`

### SRT to WebVTT Conversion

SRT subtitles are automatically converted to WebVTT format on-the-fly. The player will display them correctly without any manual conversion needed.

## 🌐 Network Access

The server listens on all interfaces by default (`0.0.0.0:5000`), making it accessible from any device on your local network.

**Example Network Setup**:
```
PC (Server): 192.168.1.100
├── Phone: 192.168.1.50  → http://192.168.1.100:5000
├── Tablet: 192.168.1.75 → http://192.168.1.100:5000
└── Laptop: 192.168.1.120 → http://192.168.1.100:5000
```

## 🔧 Configuration

Edit `app.py` to customize:

```python
MOVIES_FOLDER = 'Movies'          # Where to look for videos
VIDEO_EXTENSIONS = {'.mp4', ...}  # Supported video formats
SUBTITLE_EXTENSIONS = {'.srt', ...} # Supported subtitle formats
```

To change the port, modify:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

## 📋 API Endpoints

- `GET /` - Serves the main web interface
- `GET /api/movies` - Returns JSON list of available movies
- `GET /video/<folder>/<filename>` - Streams video with range request support
- `GET /subtitle/<folder>/<filename>` - Serves subtitle file (auto-converts SRT to WebVTT)

## 🐛 Troubleshooting

### Movies not showing up
- Ensure videos are in `Movies/<FolderName>/video.ext` structure
- Check that video files have supported extensions (`.mp4`, `.mkv`, etc.)
- Verify the `Movies` folder exists and has proper permissions

### Subtitles not displaying
- Ensure subtitle file is in the same folder as the video
- Subtitle name can be anything with `.srt` or `.vtt` extension
- Check browser console (F12) for CORS or loading errors
- Try clearing browser cache and reloading

### Can't access from other devices
- Verify both devices are on the same network (WiFi/LAN)
- Check your machine's firewall settings
- Find your machine IP: Run `ipconfig` and use the IPv4 address
- Test: `ping <your-machine-ip>` from another device

### Server won't start
- Ensure Python 3.13+ is installed: `python --version`
- Check that Flask is installed: `pip install flask`
- Verify port 5000 is not already in use
- Try a different port by editing `app.run()` in `app.py`

## 📝 License

This project is provided as-is for personal use.

## 💡 Tips & Tricks

- **Naming**: Use descriptive folder names—they become the movie titles
- **Subtitles**: Any SRT or VTT file works; automatic naming not required
- **Multiple formats**: Mix video and subtitle formats (MP4 with SRT, MKV with VTT, etc.)
- **Seeking**: Use range requests for smooth seeking in large files
- **Browser support**: Works best in Chrome, Firefox, Safari, and Edge

---

Enjoy your personal LAN video streaming! 🎥
