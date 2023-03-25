while cap.isOpened():
    success, image = cap.read()
    if not success:
      sys.exit(
          'ERROR: Unable to read from webcam. Please verify your webcam settings.'
      )

    counter += 1
    image = cv2.flip(image, 1)

    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create a TensorImage object from the RGB image.
    input_tensor = vision.TensorImage.create_from_array(rgb_image)

    # Run object detection estimation using the model.

    """ Performs object detection on the provided TensorImage.  
    https://www.tensorflow.org/lite/api_docs/python/tflite_support/task/vision/ObjectDetector 
    
    Output is detection result, which appears to be a list of all "Detection" entities

    in utils/utils.py, can see that for each detection in detection_result.detections there are the following attributes: 
        --> bounding_box: detection.bounding_box  
            ----> bounding_box.origin_x, bounding_box.origin_y, bounding_box.width, bounding_box.height
        --> category: detection.categories[0]
            ----> category_name: category.category_name
            ----> confidence: category.score
    """
    detection_result = detector.detect(input_tensor) 

""" decide how to send this to UI -- lists? objects?"""
for detection in detection_result.detections:
    # Draw bounding_box
    bbox = detection.bounding_box
    start_point = bbox.origin_x, bbox.origin_y
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
    cv2.rectangle(image, start_point, end_point, _TEXT_COLOR, 3)

    # Draw label and score
    category = detection.categories[0]
    category_name = category.category_name
    probability = round(category.score, 2)
    result_text = category_name + ' (' + str(probability) + ')'
    text_location = (_MARGIN + bbox.origin_x,
                     _MARGIN + _ROW_SIZE + bbox.origin_y)
    cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                _FONT_SIZE, _TEXT_COLOR, _FONT_THICKNESS)

"""create a list to keep track of all ingredients that have been detected and also send to UI for adding the green boxes on the order list"""
