import os
import platform
import requests
import shutil
import tarfile
import zipfile
from tqdm import tqdm

# URLs of the archives
windows_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2024-04-20-12-56/ffmpeg-N-114897-gbba996d6cd-win64-gpl-shared.zip"
mac_url = "https://evermeet.cx/ffmpeg/ffmpeg-114896-gf18de5bc4a.7z"
linux_url = "https://example.com/ffmpeg_linux.tar.xz"  # Provide the actual Linux archive URL


# Function to download a file
def download_file(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

# Function to extract a .tar.xz archive
def extract_tar_xz(archive_path, extract_dir):
    with tarfile.open(archive_path, 'r:xz') as tar:
        print(f"Extracting {archive_path}...")
        tar.extractall(extract_dir)
        print(f"Extraction of {archive_path} complete.")

# Function to extract a .7z archive
def extract_7z(archive_path, extract_dir):
    print(f"Extracting {archive_path}...")
    os.system(f'7z x "{archive_path}" -o"{extract_dir}"')
    print(f"Extraction of {archive_path} complete.")

# Function to remove a file
def remove_file(file_path):
    os.remove(file_path)

# Download and extract archives based on the system
if platform.system() == "Windows":
    # Download the Windows archive
    download_file(windows_url, "win_ffmpeg.zip")
    # Extract the Windows archive
    with zipfile.ZipFile("win_ffmpeg.zip", 'r') as zip_ref:
        zip_ref.extractall("win_ffmpeg")
    # Set FFmpeg path as environment variable
    os.environ["FFMPEG_PATH"] = os.path.join(os.getcwd(), "win_ffmpeg", "ffmpeg.exe")
    # Remove the compressed file
    remove_file("win_ffmpeg.zip")
elif platform.system() == "Darwin":  # macOS
    # Download the macOS archive
    download_file(mac_url, "ffmpeg_mac.7z")
    # Extract the macOS archive
    extract_7z("ffmpeg_mac.7z", "ffmpeg_mac")
    # Set FFmpeg path as environment variable
    os.environ["FFMPEG_PATH"] = os.path.join(os.getcwd(), "ffmpeg_mac", "ffmpeg")
    # Remove the compressed file
    remove_file("ffmpeg_mac.7z")
elif platform.system() == "Linux":
    # Download the Linux archive
    download_file(linux_url, "ffmpeg_linux.tar.xz")
    # Extract the Linux archive
    extract_tar_xz("ffmpeg_linux.tar.xz", "ffmpeg_linux")
    # Set FFmpeg path as environment variable
    os.environ["FFMPEG_PATH"] = os.path.join(os.getcwd(), "ffmpeg_linux", "ffmpeg")
    # Remove the compressed file
    remove_file("ffmpeg_linux.tar.xz")
else:
    print("Unsupported operating system")
