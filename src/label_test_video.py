import cv2
from os import path, mkdir, listdir
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import tflite_runtime.interpreter as tflite 
from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file


def label_video(input_path, 
                out_path, 
                model_path,
                frate=15,
                out_name='sample_video.mp4', 
                verbose=True):
    """Takes as input a sample video and a path to write 
    and outputs a video with boxes and labels"""
    if verbose:
        print(path.isfile(input_path))
    
    vidCap = cv2.VideoCapture(input_path) # Open input video
    width  = int(vidCap.get(cv2.CAP_PROP_FRAME_WIDTH))   # convert width to int
    height = int(vidCap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # fconvert height to int

    #Output video
    out = path.join(out_path, out_name)
    outVid = cv2.VideoWriter(out, cv2.VideoWriter_fourcc(*'mp4v'), frate, (width,height))
    # Start reading
    more_frames = 1 # Boolean to see if we've finished parsing the video
    # Load the TF Lite model
    labels = read_label_file(LABELS_FILENAME)
    interpreter = tflite.Interpreter(TFLITE_FILENAME)
    interpreter.allocate_tensors()
    while more_frames:
        more_frames, img = vidCap.read()
        

        try:
          # Resize the image for input
          #image = Image.open(INPUT_IMAGE)
          image = Image.fromarray(img)
          _, scale = common.set_resized_input(
              interpreter, image.size, lambda size: image.resize(size, Image.ANTIALIAS))

        # Run inference
          interpreter.invoke()
          objs = detect.get_objects(interpreter, score_threshold=0.2, image_scale=scale)

          # Resize again to a reasonable size for display
          display_width = 500
          scale_factor = display_width / image.width
          height_ratio = image.height / image.width
          image = image.resize((display_width, int(display_width * height_ratio)))
          draw_objects(ImageDraw.Draw(image), objs, scale_factor, labels)
          outVid.write(img)
        except:
          continue
    outVid.release()


if __name__ == '__main__':
    inPth = "C:/Users/jonathan.sy/Documents/Rest_Item_Identifier_Proj/training/video/pack_vid_3.mov"
    outPth = "C:/Users/jonathan.sy/Documents/Rest_Item_Identifier_Proj/training/video"
    model = None
    label_video(inPth, outPth, model)