# Lab 3: Video Analyzer

This script reads a video file and generates a metadata report using `ffprobe` (part of the FFmpeg suite). It extracts details about the container, the video stream (resolution, frame rate, codec), and the audio stream (channels, sample rate, codec).

## Usage
```bash
python video_analyzer.py <path_to_video>
```

## Requirements
- Python 3
- FFmpeg/ffprobe installed on the system and available in the system path.

## System Workflow / Use Case
```mermaid
flowchart LR
    User([User])
    subgraph Video Analyzer
        UC1([Invoke FFprobe])
        UC2([Parse Container Info])
        UC3([Parse Video Stream])
        UC4([Parse Audio Stream])
        UC5([Generate Output Report])
    end
    
    User -->|Provides Video| UC1
    UC1 --> UC2
    UC1 --> UC3
    UC1 --> UC4
    UC2 --> UC5
    UC3 --> UC5
    UC4 --> UC5
    UC5 -->|View Metadata| User
```
