import cv2 as cv
from ultralytics import YOLO
import keras
from PIL import Image
import numpy as np

class InspectVideo:
    def __init__(self,objectDetectorPath :str = "models/fastModel.pt" ):
        self.ODmodel = YOLO(objectDetectorPath)

    def predictImage(self,img, model_dir):
        model = keras.models.load_model(model_dir)
        image = Image.fromarray(img, "RGB")
        image = np.array(image.resize((224, 224))) / 255.0
        input_img = np.expand_dims(image, axis=0)
        return np.argmax(model.predict(input_img))


    def inspectVideo(self,videoPath,filename,model):
        cap = cv.VideoCapture(videoPath+filename)

        my_model = f"models/{model}_model.h5"

        # Get the width and height of the original video frame
        original_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

        # Skip every n frames for processing
        frame_skip = 5

        bounded_boxes = {}
        X1, Y1, X2, Y2 = original_width * 0.4, 0, original_width * 0.6, original_height
        size = (original_width,original_height)

        fourcc = cv.VideoWriter_fourcc(*'MP42')  # You can choose other codecs too
        output_video = cv.VideoWriter(f'web/static/output/'+filename, fourcc, 5, size)

        while cap.isOpened():
            for _ in range(frame_skip):
                cap.grab()  # Skip frames

            ret, frame = cap.read()
            if not ret:
                break

            results = self.ODmodel(frame)


            # Draw bounding boxes on the original frame
            bounded_boxes = {}
            detected_boxes = {}

            annoted = results[0]
            count = 0

            for box in annoted.boxes.xyxy:
                x1, y1, x2, y2 = box[:4].tolist()
                bounded_boxes[count] = [x1, y1, x2, y2]
                detected_boxes[count] = 0

                x1, y1, x2, y2 = bounded_boxes[count]
                item = frame[int(y1) : int(y2) + 1, int(x1) : int(x2) + 1]

                box_center_x = (x2 + x1) / 2
                box_center_y = (y2 + y1) / 2

                # check if the box center lies in the X1,Y1,X2,Y2
                if X1 < box_center_x < X2 and Y1 < box_center_y < Y2:
                    prediction = self.predictImage(item, my_model)
                    if prediction == 1:
                        detected_boxes[count] = 1
                count += 1



            for key, value in bounded_boxes.items():
                x1, y1, x2, y2 = value
                box_center_x = (x2 + x1) / 2
                box_center_y = (y2 + y1) / 2

                # check if the box center lies in the X1,Y1,X2,Y2
                if X1 < box_center_x < X2 and Y1 < box_center_y < Y2:
                    if detected_boxes.get(key) == 1:
                        cv.rectangle(
                            frame,
                            pt1=(int(x1), int(y1)),
                            pt2=(int(x2), int(y2)),
                            color=(0, 0, 255),
                            thickness=3,
                        )
                    else:
                        cv.rectangle(
                            frame,
                            pt1=(int(x1), int(y1)),
                            pt2=(int(x2), int(y2)),
                            color=(0, 255, 0),
                            thickness=1,
                        )
            
            output_video.write(frame)


                # response = original_frame
            # Exit if 'q' is pressed
            if cv.waitKey(1) & 0xFF == ord("d"):
                break
            # Stop if 's' is pressed
            if cv.waitKey(1) & 0xFF == ord("s"):
                cv.waitKey(-1)

        # Release video capture and writer objects
        cap.release()
        output_video.release()
        cv.destroyAllWindows()
        return {"output_video_url": "/static/output/" + filename}
    

    def checklabel(self,videoPath,filename,label):

        cap = cv.VideoCapture(videoPath+filename)
        # Skip every n frames for processing
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = self.ODmodel(frame)

            names = results[0].names
            labelNo = 0
            for i, name in names.items():
                if (name =='fryams' and label=='fryums') or name==label:
                    labelNo = i

                
            #check if results[0].boxes['cls'] tensor contains the labelNo
            predLabel = results[0].boxes.cls.tolist()
                    
            if len(predLabel) == 0:
                continue

            if float(labelNo) in predLabel:
                cap.release()
                cv.destroyAllWindows()
                return True
            else:
                cap.release()
                cv.destroyAllWindows()
                return False

        cap.release()
        cv.destroyAllWindows()     
        return False