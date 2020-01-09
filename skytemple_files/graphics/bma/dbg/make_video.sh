#!/bin/sh
ffmpeg -stream_loop 20 -r 10 -i $1.%d.png -c:v libx264 -vf fps=60 $1.mp4
