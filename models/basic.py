import cv2
import os
import pandas as pd
import numpy as np


def FrameExtract(path, reso):

    vidObj = cv2.VideoCapture(path)
    fps = vidObj.get(cv2.CAP_PROP_FPS)
    g_frame = []
    og_frame = []
    wi = reso
    hi = int(vidObj.get(cv2.CAP_PROP_FRAME_HEIGHT) /
             vidObj.get(cv2.CAP_PROP_FRAME_WIDTH)*reso)
    success = 1

    while success:

        success, image = vidObj.read()
        if (success == True):
            og_frame.append(image)
            gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_img = cv2.resize(gray_img, (wi, hi),
                                  interpolation=cv2.INTER_AREA)
            gray_img = cv2.GaussianBlur(gray_img, (21, 21), 0)
            image = np.array(gray_img)
            # Saves the frames with frame-count
            g_frame.append(image.flatten())

    return og_frame, g_frame, fps, hi, wi


def impPt(frame):
    frame_nos = []
    imp_frams = []
    for i in range(len(frame)-1):
        if(np.mean(cv2.subtract(frame[0], frame[i])) > 1.5):
            frame_nos.append(i)
            imp_frams.append(cv2.subtract(g_frames[0].reshape(
                (height, width)), g_frames[i].reshape((height, width))))
    return frame_nos, imp_frams


def genImpVid(video_name, images, height, width, color, fps):
    writer = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(
        *'MP4V'), fps, (width, height), color)
    for i in images:
        writer.write(i)


def main(vid_file):
    global og_frames, g_frames, fps, height, width, hist_arr, impFrams

    og_frames, g_frames, fps, height, width = FrameExtract(vid_file, 500)
    frame_nos, impFrams = impPt(g_frames)
    genImpVid("static/video/output/og.mp4",
              [og_frames[i] for i in frame_nos], 720, 1280, True, fps)
    os.system(
        "yes | ffmpeg -i static/video/output/og.mp4 -vcodec libx264 static/video/output/output.mp4")
    os.remove("static/video/output/og.mp4")


# main("video.mp4")
