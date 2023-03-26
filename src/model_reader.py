import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision


class ModelReader:
    def __init__(self, model, input_type, n_threads):
        """
        Takes the following inputs
        model: Path to a tf-lite model
        input_type:
        """
        self.model = model
        self.input_type = input_type
        # Visualization parameters
        row_size = 20  # pixels
        left_margin = 24  # pixels
        text_color = (0, 0, 255)  # red
        font_size = 1
        font_thickness = 1
        fps_avg_frame_count = 10


        base_options = core.BaseOptions(
          file_name=model,
          use_coral=enable_edgetpu,
          num_threads=n_threads)
        detection_options = processor.DetectionOptions(
          max_results= maxResults, 
          score_threshold=scoreThreshold)
        options = vision.ObjectDetectorOptions(
          base_options=base_options,
          detection_options=detection_options)

        detector = vision.ObjectDetector.create_from_options(options)

    def get_image_labels(self, input):
        if input_type == 'video':
            # Read frame
            frame = input.read()
        elif input_type == 'frame':
            frame = input

        # Apparently we need to flip the image?
        frame = cv2.flip(frame, 1)
        # Convert the image from BGR to RGB as required by the TFLite model.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        input_tensor = vision.TensorImage.create_from_array(rgb_image)
        # Get result
        detection_result = detector.detect(input_tensor)
