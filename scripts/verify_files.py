import os
import shutil
import subprocess

# Paths
DOWNLOAD_DIR = "/mnt/d/linux/media/downloads"
TV_DIR = "/mnt/d/linux/media/tv"
MOVIES_DIR = "/mnt/d/linux/media/movies"
MUSIC_DIR = "/mnt/d/linux/media/music"
QUARANTINE_DIR = "/mnt/d/linux/media/quarantine"
FAILED_DIR = "/mnt/d/linux/media/did_not_pass"

def scan_file(path):
    """Run ClamAV scan and return True if clean, False if infected"""
    result = subprocess.run(["clamscan", path], capture_output=True, text=True)
    if "Infected files: 0" in result.stdout:
        return True
    return False

def move_file(path, destination_dir):
    os.makedirs(destination_dir, exist_ok=True)
    shutil.move(path, os.path.join(destination_dir, os.path.basename(path)))

def classify_and_move(path):
    name = os.path.basename(path).lower()
    if any(ext in name for ext in [".mp4", ".mkv", ".avi"]):
        move_file(path, TV_DIR if "s" in name else MOVIES_DIR)
    elif any(ext in name for ext in [".mp3", ".flac", ".wav"]):
        move_file(path, MUSIC_DIR)
    else:
        move_file(path, FAILED_DIR)

def main():
    for root, _, files in os.walk(DOWNLOAD_DIR):
        for file in files:
            filepath = os.path.join(root, file)
            print(f"Scanning {filepath}...")
            if scan_file(filepath):
                classify_and_move(filepath)
            else:
                print(f"Infected! Moving {filepath} to quarantine.")
                move_file(filepath, QUARANTINE_DIR)

if __name__ == "__main__":
    main()