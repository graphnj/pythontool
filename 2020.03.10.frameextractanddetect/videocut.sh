#!/bin/bash
#zhu.jinhua 2020.3.5

VIDEO_PATH=0308
FFMPEG_EXECPATH=/opt/ffmpeg/ffmpeg
FRAMES_PERSECOND=10
IMAGES_OUTPATH=0308images
mkdir $IMAGES_OUTPATH

for file in $VIDEO_PATH/*
do
    
    $FFMPEG_EXECPATH -i $file -f image2 -vf fps=fps=$FRAMES_PERSECOND/1 -qscale:v 2 $IMAGES_OUTPATH/${file#*/}-%06d.jpg
    echo "finished $file"
done    
