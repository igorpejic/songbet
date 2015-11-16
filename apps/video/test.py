import numpy as np
import sys
from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects

screensize = (1280,720)


cool = VideoFileClip("cool.mp4").subclip(1, 7)

image = (ImageClip("lower1.png").set_duration(4))

txt_title = (TextClip("15th century dancing\n(hypothetical)", fontsize=18,
                      font="Century-Schoolbook-Roman", color="white")
             .margin(top=15, opacity=0)
             .set_position(("left","bottom")))


final = CompositeVideoClip([cool, image], size=((1280, 720)))
#final.subclip(0,5).write_videofile('sub.mp4', fps=24, codec='libx264')
image2 = (ImageClip("lower2.png").set_duration(4))
final2 = CompositeVideoClip([cool, image2], size=((1280, 720)))

FINAL = concatenate_videoclips([final, final2])
FINAL.write_videofile("final.mp4", fps=24, codec='libx264')
