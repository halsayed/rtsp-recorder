ffmpeg -i rtsp://nutanix:test1234@192.168.100.21:8554/Streaming/Channels/101 -c copy -f segment -segment_time 10 -strftime 1 "capture-%Y-%m-%d_%H-%M-%S.mp4"