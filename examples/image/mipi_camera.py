import os

os.system('gst-launch-1.0 -v v4l2src device=/dev/video0 num-buffers=1 ! "video/x-bayer, format=bggr, width=1920, height=1080, bpp=8, framerate=30/1" ! multifilesink location=test0.bayer')
os.system('./bayer2rgb --input=test0.bayer --output=data.tiff --width=640 --height=480 --bpp=8 --first=BGGR \ --method=BILINEAR --tiff')
os.system('convert data.tiff data.png')