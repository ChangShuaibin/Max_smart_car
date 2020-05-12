#############################################
# Object detection - YOLO - OpenCV
# Author : Arun Ponnusamy   (July 16, 2018)
# Website : http://www.arunponnusamy.com
############################################


import cv2
import numpy as np


class Object_detect():
    def __init__(self):
        super().__init__()
        self.config_path='/Users/stephanchang/PycharmProjects/Object_detection1/yolov3.cfg'
        self.weights_path='/Users/stephanchang/PycharmProjects/Object_detection1/yolov3.weights'
        self.classes_path='/Users/stephanchang/PycharmProjects/Object_detection1/yolov3.txt'
        self.list_obj_x=[]
        self.list_obj_y=[]
        self.list_obj_name=[]
        self.classes = None
        self.image=None
        self.COLORS=None


    def get_output_layers(self, net):
        layer_names = net.getLayerNames()

        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        return output_layers


    def draw_prediction(self, img, class_id, confidence, x, y, x_plus_w, y_plus_h):
        label = str(self.classes[class_id])

        color = self.COLORS[class_id]

        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)

        cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def list_prediction(self, class_id, x, y, x_plus_w, y_plus_h):
        self.list_obj_name.append(self.classes[class_id])
        self.list_obj_x.append(x+x_plus_w/2)
        self.list_obj_y.append(y+y_plus_h/2)

    def obj_detect(self, image_path):
        self.image = cv2.imread(image_path)

        Width = self.image.shape[1]
        Height = self.image.shape[0]
        scale = 0.00392


        with open(self.classes_path, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

        self.COLORS = np.random.uniform(0, 255, size=(len(self.classes), 3))

        net = cv2.dnn.readNet(self.weights_path, self.config_path)

        blob = cv2.dnn.blobFromImage(self.image, scale, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)

        outs = net.forward(self.get_output_layers(net))

        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.5
        nms_threshold = 0.4

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            #self.draw_prediction(self.image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
            self.list_prediction(class_ids[i], round(x), round(y), round( w),
                                 round( h))
        for i in range(len(indices)):
            print(self.list_obj_name[i], self.list_obj_x[i], self.list_obj_y[i])
        #cv2.imshow("object detection", self.image)
        #cv2.waitKey()

        #cv2.imwrite("object-detection.jpg", self.image)
        #cv2.destroyAllWindows()


if __name__ == '__main__':
    window = Object_detect()
    window.obj_detect('/Users/stephanchang/PycharmProjects/Object_detection1/fruit.jpg')


