import os
import subprocess
import json

def get_ffprobe_data(file_path):
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        file_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error running ffprobe: {e}")
        return None

def analyze_video(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        return

    data = get_ffprobe_data(file_path)
    if not data:
        print("Could not retrieve video data.")
        return

    format_info = data.get('format', {})
    streams = data.get('streams', [])

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    file_size_mb = file_size / (1024 * 1024)
    container = format_info.get('format_long_name', format_info.get('format_name', 'Unknown'))
    duration = float(format_info.get('duration', 0))

    video_stream = next((s for s in streams if s.get('codec_type') == 'video'), {})
    audio_stream = next((s for s in streams if s.get('codec_type') == 'audio'), {})

    print("================================")
    print("VIDEO METADATA REPORT")
    print("================================")
    print(f"File Name       : {file_name}")
    print(f"File Size       : {file_size_mb:.2f} MB")
    print(f"Container       : {container}")
    print(f"Duration        : {duration:.2f} seconds")

    if video_stream:
        width = video_stream.get('width', 'Unknown')
        height = video_stream.get('height', 'Unknown')
        frame_rate = video_stream.get('r_frame_rate', 'Unknown')
        bit_rate = video_stream.get('bit_rate', 'Unknown')
        if bit_rate != 'Unknown':
            bit_rate = f"{int(bit_rate) // 1000} kbps"
        codec = video_stream.get('codec_name', 'Unknown')

        print("\nVIDEO")
        print("--------------------------------")
        print(f"Resolution      : {width}x{height}")
        print(f"Frame Rate      : {frame_rate}")
        print(f"Bit Rate        : {bit_rate}")
        print(f"Codec           : {codec}")

    if audio_stream:
        a_codec = audio_stream.get('codec_name', 'Unknown')
        channels = audio_stream.get('channels', 'Unknown')
        sample_rate = audio_stream.get('sample_rate', 'Unknown')
        a_bit_rate = audio_stream.get('bit_rate', 'Unknown')
        if a_bit_rate != 'Unknown':
            a_bit_rate = f"{int(a_bit_rate) // 1000} kbps"

        print("\nAUDIO")
        print("--------------------------------")
        print(f"Codec           : {a_codec}")
        print(f"Channels        : {channels}")
        print(f"Sampling Rate   : {sample_rate} Hz")
        print(f"Bit Rate        : {a_bit_rate}")

    tags = format_info.get('tags', {})
    if tags:
        print("\nMETADATA")
        print("--------------------------------")
        for key, value in tags.items():
            print(f"{key:15} : {value}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        analyze_video(sys.argv[1])
    else:
        print("Usage: python video_analyzer.py <path_to_video>")
