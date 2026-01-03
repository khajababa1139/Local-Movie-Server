from flask import Flask, render_template, send_file, jsonify, Response
from flask import request
import os
import re
from pathlib import Path

app = Flask(__name__)

# Configuration
MOVIES_FOLDER = 'Movies'
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.webm'}
SUBTITLE_EXTENSIONS = {'.srt', '.vtt'}

def get_movies():
    """Scan Movies folder and return list of movies with their files"""
    movies = []
    movies_path = Path(MOVIES_FOLDER)
    
    if not movies_path.exists():
        return movies
    
    for item in movies_path.iterdir():
        if item.is_dir():
            # Existing logic: look for videos in subdirectories
            video_file = None
            subtitle_file = None
            
            for file in item.iterdir():
                if file.suffix.lower() in VIDEO_EXTENSIONS:
                    video_file = file.name
                elif file.suffix.lower() in SUBTITLE_EXTENSIONS:
                    subtitle_file = file.name
            
            if video_file:
                movies.append({
                    'folder': item.name,
                    'title': item.name.replace('_', ' '),
                    'video': video_file,
                    'subtitle': subtitle_file
                })
        elif item.is_file() and item.suffix.lower() in VIDEO_EXTENSIONS:
            # New logic: look for bare video files in Movies folder
            video_file = item.name
            subtitle_file = None
            
            # Look for matching subtitle file in Movies folder
            for subtitle_ext in SUBTITLE_EXTENSIONS:
                subtitle_candidate = item.parent / (item.stem + subtitle_ext)
                if subtitle_candidate.exists():
                    subtitle_file = subtitle_candidate.name
                    break
            
            movies.append({
                'folder': '__bare__',
                'title': item.stem.replace('_', ' '),
                'video': video_file,
                'subtitle': subtitle_file
            })
    
    return sorted(movies, key=lambda x: x['title'])

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/movies')
def api_movies():
    """API endpoint to get list of movies"""
    return jsonify(get_movies())

@app.route('/video/<folder>/<filename>')
def video(folder, filename):
    """Stream video file with range request support"""
    # Handle both folder-based and bare video files
    if folder == '__bare__':
        video_path = Path(MOVIES_FOLDER) / filename
    else:
        video_path = Path(MOVIES_FOLDER) / folder / filename
    
    if not video_path.exists():
        return "Video not found", 404
    
    # Get file size
    file_size = video_path.stat().st_size
    
    # Parse range header
    range_header = request.headers.get('Range', None)
    
    if range_header:
        byte_start, byte_end = 0, file_size - 1
        match = re.search(r'bytes=(\d+)-(\d*)', range_header)
        
        if match:
            groups = match.groups()
            byte_start = int(groups[0])
            if groups[1]:
                byte_end = int(groups[1])
        
        length = byte_end - byte_start + 1
        
        def generate():
            with open(video_path, 'rb') as f:
                f.seek(byte_start)
                remaining = length
                while remaining:
                    chunk_size = min(8192, remaining)
                    data = f.read(chunk_size)
                    if not data:
                        break
                    remaining -= len(data)
                    yield data
        
        resp = Response(generate(), 206, mimetype='video/mp4',
                       direct_passthrough=True)
        resp.headers.add('Content-Range', f'bytes {byte_start}-{byte_end}/{file_size}')
        resp.headers.add('Accept-Ranges', 'bytes')
        resp.headers.add('Content-Length', str(length))
        return resp
    
    return send_file(video_path)

@app.route('/subtitle/<folder>/<filename>')
def subtitle(folder, filename):
    """Serve subtitle file"""
    # Handle both folder-based and bare video files
    if folder == '__bare__':
        subtitle_path = Path(MOVIES_FOLDER) / filename
    else:
        subtitle_path = Path(MOVIES_FOLDER) / folder / filename
    
    if not subtitle_path.exists():
        return "Subtitle not found", 404
    # If the file is already a WebVTT file, serve it directly
    if subtitle_path.suffix.lower() == '.vtt':
        return send_file(subtitle_path, mimetype='text/vtt')

    # If it's an SRT file, convert to WebVTT on-the-fly
    if subtitle_path.suffix.lower() == '.srt':
        try:
            with open(subtitle_path, 'r', encoding='utf-8', errors='replace') as f:
                srt_text = f.read()
        except Exception:
            return "Could not read subtitle", 500

        # Remove any BOM
        if srt_text.startswith('\ufeff'):
            srt_text = srt_text.lstrip('\ufeff')

        # Remove cue numbers (lines that only contain digits)
        srt_no_nums = re.sub(r'(?m)^\s*\d+\s*$', '', srt_text)

        # Convert timecodes from 00:00:00,000 to 00:00:00.000
        vtt_body = re.sub(r"(\d{2}:\d{2}:\d{2}),(\d{3})", r"\1.\2", srt_no_nums)

        # Prepend WebVTT header
        vtt = 'WEBVTT\n\n' + vtt_body.strip() + '\n'

        resp = Response(vtt, mimetype='text/vtt')
        # Suggest a filename for downloads and allow caching in the browser
        resp.headers['Content-Disposition'] = f'inline; filename="{subtitle_path.stem}.vtt"'
        resp.headers['Cache-Control'] = 'public, max-age=3600'
        return resp

    # Fallback: serve as plain text
    return send_file(subtitle_path, mimetype='text/plain')

if __name__ == '__main__':
    # Check and create Movies folder if it doesn't exist
    movies_path = Path(MOVIES_FOLDER)
    
    if movies_path.exists():
        print(f"✓ Movies folder found at: {movies_path.absolute()}")
    else:
        try:
            movies_path.mkdir(exist_ok=True, parents=True)
            print(f"✓ Movies folder created at: {movies_path.absolute()}")
        except PermissionError:
            print(f"✗ Error: Permission denied creating Movies folder at {movies_path.absolute()}")
            print("✗ Please check directory permissions and try again.")
        except Exception as e:
            print(f"✗ Error creating Movies folder: {e}")
            print("✗ Please check your filesystem and try again.")
    
    # Run on all interfaces so it's accessible on LAN
    print("\nStarting Local Movie Server...")
    print("Server running at: http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)