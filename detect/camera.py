import cv2, urllib.request
import numpy as np
import easyocr
import string
from home.models import VehicleDetails

net = cv2.dnn.readNet('./model/18_03_new_weights/yolov3_training_last.weights', './model/18_03_new_weights/yolov3_testing.cfg')

classes = []
with open("./model/18_03_new_weights/classes.txt", "r") as f:
    classes = f.read().splitlines()

# cap = cv2.VideoCapture('./model/Resources/video7.mp4')
font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(100, 3))
state = ('AP','AR','AS','BR','CG','GA','GJ','HR','HP','JK','JH','KA','KL','MP','MH','MN','ML','MZ','NL','OR','PB','RJ','SK','TN','TR','UK','UP','WB','TN','TR','AN','CH','DH','DD','DL','LD','PY')

MainText = []
DeletedText = []
FinalText = []
# idv = [133]

# mydb = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='',
#     database='vrd'
# )
# cur = mydb.cursor()
# s="INSERT INTO home_cameradetails (cameranum, location, status) VALUES (%s, %s, %s)"
# b1 = (117, 'Ved Road', True)
# cur.execute(s, b1)
# mydb.commit()
# print("Inserted")

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture('./model/Resources/v19_7.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):

        success, img = self.video.read()
        # img = cv2.resize(img, (1080, 720))
        height, width, _ = img.shape

        blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
        net.setInput(blob)
        output_layers_names = net.getUnconnectedOutLayersNames()
        layerOutputs = net.forward(output_layers_names)

        boxes = []
        confidences = []
        class_ids = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.2:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append((float(confidence)))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)
        countHP = 0
        probableText = []
        if len(indexes) > 0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = str(round(confidences[i], 2))
                color = colors[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

                imgRoi = img[y:y + h, x:x + w]

                countHP += 1
                print("*****************", countHP, " ", confidence, "********************")

                gray = cv2.cvtColor(imgRoi, cv2.COLOR_BGR2GRAY)

                print("EasyOCR Results :")
                read = easyocr.Reader(['en'], gpu=False)
                ALLOWED_LIST = string.ascii_uppercase + string.digits
                result = read.readtext(gray, detail=0, allowlist=ALLOWED_LIST)
                print(result)
                TempText = ""
                matchIndex = None
                Text = ""
                for text in result:
                    Text += text
                Text = Text.upper()
                print(Text, '  ', len(Text))

                if len(Text) == 10:
                    numberPlate = Text[6:10]
                    if len(MainText) > 0:
                        countArr = []
                        for i in MainText:
                            tempNumberPlate = i[6:10]
                            countItem = 0
                            for x in range(6, 10):
                                if i[x] == Text[x]:
                                    countItem += 1
                            countArr.append(countItem)

                        if max(countArr) >= 3:
                            matchIndex = countArr.index(max(countArr))

                        if matchIndex is not None:
                            sanitizeText = MainText[matchIndex]
                            p1 = Text[:2]
                            p2 = Text[2:4]
                            p3 = Text[4:6]
                            p4 = Text[6:10]

                            c1 = sanitizeText[:2]
                            c2 = sanitizeText[2:4]
                            c3 = sanitizeText[4:6]
                            c4 = sanitizeText[6:10]

                            if p1 is not c1:
                                if p1[0] is not c1[0]:
                                    if p1[0].isalpha() and c1[0].isnumeric():
                                        TempText += p1[0]
                                    elif p1[0].isnumeric() and c1[0].isalpha():
                                        TempText += c1[0]
                                    else:
                                        TempText += p1[0]
                                else:
                                    TempText += p1[0]

                                if p1[1] is not c1[1]:
                                    if p1[1].isalpha() and c1[1].isnumeric():
                                        TempText += p1[1]
                                    elif p1[1].isnumeric() and c1[1].isalpha():
                                        TempText += c1[1]
                                    else:
                                        TempText += p1[1]
                                else:
                                    TempText += p1[1]
                            else:
                                TempText += p1

                            if p2 is not c2:
                                if p2[0] is not c2[0]:
                                    if p2[0].isalpha() and c2[0].isnumeric():
                                        TempText += c2[0]
                                    elif p2[0].isnumeric() and c2[0].isalpha():
                                        TempText += p2[0]
                                    else:
                                        TempText += p2[0]
                                else:
                                    TempText += p2[0]

                                if p2[1] is not c2[1]:
                                    if p2[1].isalpha() and c2[1].isnumeric():
                                        TempText += c2[1]
                                    elif p2[1].isnumeric() and c2[1].isalpha():
                                        TempText += p2[1]
                                    else:
                                        TempText += p2[1]
                                else:
                                    TempText += p2[1]
                            else:
                                TempText += p2

                            if p3 is not c3:
                                if p3[0] is not c3[0]:
                                    if p3[0].isalpha() and c3[0].isnumeric():
                                        TempText += p3[0]
                                    elif p3[0].isnumeric() and c3[0].isalpha():
                                        TempText += c3[0]
                                    else:
                                        TempText += p3[0]
                                else:
                                    TempText += p3[0]

                                if p3[1] is not c3[1]:
                                    if p3[1].isalpha() and c3[1].isnumeric():
                                        TempText += p3[1]
                                    elif p3[1].isnumeric() and c3[1].isalpha():
                                        TempText += c3[1]
                                    else:
                                        TempText += p3[1]
                                else:
                                    TempText += p3[1]
                            else:
                                TempText += p3

                            if p4 is not c4:
                                if p4[0] is not c4[0]:
                                    if p4[0].isalpha() and c4[0].isnumeric():
                                        TempText += c4[0]
                                    elif p4[0].isnumeric() and c4[0].isalpha():
                                        TempText += p4[0]
                                    else:
                                        TempText += p4[0]
                                else:
                                    TempText += p4[0]

                                if p4[1] is not c4[1]:
                                    if p4[1].isalpha() and c4[1].isnumeric():
                                        TempText += c4[1]
                                    elif p4[1].isnumeric() and c4[1].isalpha():
                                        TempText += p4[1]
                                    else:
                                        TempText += p4[1]
                                else:
                                    TempText += p4[1]

                                if p4[2] is not c4[2]:
                                    if p4[2].isalpha() and c4[2].isnumeric():
                                        TempText += c4[2]
                                    elif p4[2].isnumeric() and c4[2].isalpha():
                                        TempText += p4[2]
                                    else:
                                        TempText += p4[2]
                                else:
                                    TempText += p4[2]

                                if p4[3] is not c4[3]:
                                    if p4[3].isalpha() and c4[3].isnumeric():
                                        TempText += c4[3]
                                    elif p4[3].isnumeric() and c4[3].isalpha():
                                        TempText += p4[3]
                                    else:
                                        TempText += p4[3]
                                else:
                                    TempText += p4[3]
                            else:
                                TempText += p4

                            if len(TempText) == 10:
                                MainText[matchIndex] = TempText
                                print("MainText : ", MainText)
                                probability = 0
                                for i in MainText:
                                    probability = 0
                                    if i[0].isalpha():
                                        probability += 1
                                    if i[1].isalpha():
                                        probability += 1
                                    if i[2].isnumeric():
                                        probability += 1
                                    if i[3].isnumeric():
                                        probability += 1
                                    if i[4].isalpha():
                                        probability += 1
                                    if i[5].isalpha():
                                        probability += 1
                                    if i[6].isnumeric():
                                        probability += 1
                                    if i[7].isnumeric():
                                        probability += 1
                                    if i[8].isnumeric():
                                        probability += 1
                                    if i[9].isnumeric():
                                        probability += 1

                                    if probability == 10:
                                        if i in DeletedText:
                                            MainText.remove(i)
                                        elif i[:2] not in state:
                                            MainText.remove(i)
                                        else:
                                            print("DATA INSERT HERE : ", i)
                                            vehicle_no = i[:2] + '-' + i[2:4] + '-' +i[4:6] + '-' + i[6:10]
                                            vd = VehicleDetails(vehicle_no=vehicle_no, cameranum_id=104)
                                            vd.save()
                                            print("***********************Inserted**************************")

                                            # idv[0] = idv[0] + 1

                                            FinalText.append(i)
                                            if len(DeletedText) > 10:
                                                DeletedText.pop(0)
                                            DeletedText.append(i)

                        elif tempNumberPlate.isnumeric():
                            MainText.append(Text)
                            print("MainText : ", MainText)
                    elif Text[6:10].isnumeric():
                        MainText.append(Text)
                        print("MainText : ", MainText)

        # frame_flip = cv2.flip(img, 1)
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()


# class PhoneCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)
#         self.url = "http://192.168.1.100:8080/video"
#         # self.url = "http://10.11.100.105:8080/video"
#         # self.url = "http://[2402:3a80:e47:d0ea:0:1e:2c68:8f01]:8080/video"
#         self.video.open(self.url)
#
#     def __del__(self):
#         cv2.destroyAllWindows()
#
#     def get_frame(self):
#
#         success, img = self.video.read()
#
#         # imgResp = urllib.request.urlopen(self.url)
#         # imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
#         # img = cv2.imdecode(imgNp, -1)
#
#
#         # img = cv2.resize(img, (1080, 720))
#         height, width, _ = img.shape
#
#         blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
#         net.setInput(blob)
#         output_layers_names = net.getUnconnectedOutLayersNames()
#         layerOutputs = net.forward(output_layers_names)
#
#         boxes = []
#         confidences = []
#         class_ids = []
#
#         for output in layerOutputs:
#             for detection in output:
#                 scores = detection[5:]
#                 class_id = np.argmax(scores)
#                 confidence = scores[class_id]
#                 if confidence > 0.2:
#                     center_x = int(detection[0] * width)
#                     center_y = int(detection[1] * height)
#                     w = int(detection[2] * width)
#                     h = int(detection[3] * height)
#
#                     x = int(center_x - w / 2)
#                     y = int(center_y - h / 2)
#
#                     boxes.append([x, y, w, h])
#                     confidences.append((float(confidence)))
#                     class_ids.append(class_id)
#
#         indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)
#         countHP = 0
#         if len(indexes) > 0:
#             for i in indexes.flatten():
#                 x, y, w, h = boxes[i]
#                 label = str(classes[class_ids[i]])
#                 confidence = str(round(confidences[i], 2))
#                 color = colors[i]
#                 cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
#                 cv2.putText(img, confidence, (x, y), font, 2, (255, 255, 255), 2)
#
#                 imgRoi = img[y:y + h, x:x + w]
#                 countHP += 1
#                 print("*****************", countHP, " ", confidence, "********************")
#                 # cv2.imshow('Image', img)
#                 # cv2.imwrite('Cropped.jpg', imgRoi)
#                 # cv2.imshow('Cropped Image', imgRoi)
#                 # cv2.waitKey(0)
#
#                 gray = cv2.cvtColor(imgRoi, cv2.COLOR_BGR2GRAY)
#                 # cv2.imshow("gray",gray)
#                 # cv2.waitKey(0)
#                 # cv2.imwrite('Cropped1.jpg', gray)
#
#                 blur = cv2.GaussianBlur(gray, (7, 7), 0)
#                 # cv2.imshow("blur",blur)
#                 # cv2.waitKey(0)
#
#                 # Applied inversed thresh_binary
#                 binary = cv2.threshold(blur, 180, 255,
#                                        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#                 # cv2.imshow("binary",binary)
#                 # cv2.waitKey(0)
#
#                 ## Applied dilation
#                 kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
#
#                 thre_mor = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel3)
#                 # cv2.imshow("thresh",thre_mor)
#                 # cv2.waitKey(0)
#                 # cv2.imwrite('Cropped2.jpg', thre_mor)
#
#                 # text = pt.image_to_string(thre_mor,
#                 #                           config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8 --oem 3')
#                 # text1 = pt.image_to_string(thre_mor, config='--psm 11')
#                 # # text = pt.image_to_string(imgRoi,config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8 --oem 3')
#                 # # text1 = pt.image_to_string(imgRoi, config='--psm 11')
#                 #
#                 # print("Tesseract Results :")
#                 # print(text)
#                 # print("*************")
#                 # print(text1)
#
#                 print("EasyOCR Results :")
#                 read = easyocr.Reader(['en'], gpu=False)
#                 ALLOWED_LIST = string.ascii_uppercase + string.digits
#                 result = read.readtext(gray, detail=0, allowlist=ALLOWED_LIST)
#                 print(result)
#
#                 Text = ""
#                 for text in result:
#                     Text += text
#                 print("License Plate : ", Text)
#         # frame_flip = cv2.flip(img, 1)
#         ret, jpeg = cv2.imencode('.jpg', img)
#         return jpeg.tobytes()


# class LaptopCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)
#
#     def __del__(self):
#         self.video.release()
#
#     def get_frame(self):
#
#         success, img = self.video.read()
#         # img = cv2.resize(img, (1080, 720))
#         height, width, _ = img.shape
#
#         blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
#         net.setInput(blob)
#         output_layers_names = net.getUnconnectedOutLayersNames()
#         layerOutputs = net.forward(output_layers_names)
#
#         boxes = []
#         confidences = []
#         class_ids = []
#
#         for output in layerOutputs:
#             for detection in output:
#                 scores = detection[5:]
#                 class_id = np.argmax(scores)
#                 confidence = scores[class_id]
#                 if confidence > 0.2:
#                     center_x = int(detection[0] * width)
#                     center_y = int(detection[1] * height)
#                     w = int(detection[2] * width)
#                     h = int(detection[3] * height)
#
#                     x = int(center_x - w / 2)
#                     y = int(center_y - h / 2)
#
#                     boxes.append([x, y, w, h])
#                     confidences.append((float(confidence)))
#                     class_ids.append(class_id)
#
#         indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)
#         countHP = 0
#         if len(indexes) > 0:
#             for i in indexes.flatten():
#                 x, y, w, h = boxes[i]
#                 label = str(classes[class_ids[i]])
#                 confidence = str(round(confidences[i], 2))
#                 color = colors[i]
#                 cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
#                 cv2.putText(img, confidence, (x, y), font, 2, (0, 0, 0), 2)
#
#                 imgRoi = img[y:y + h, x:x + w]
#                 countHP += 1
#                 print("*****************", countHP, " ", confidence, "********************")
#                 # cv2.imshow('Image', img)
#                 # cv2.imwrite('Cropped.jpg', imgRoi)
#                 # cv2.imshow('Cropped Image', imgRoi)
#                 # cv2.waitKey(0)
#
#                 gray = cv2.cvtColor(imgRoi, cv2.COLOR_BGR2GRAY)
#                 # cv2.imshow("gray",gray)
#                 # cv2.waitKey(0)
#                 # cv2.imwrite('Cropped1.jpg', gray)
#
#                 blur = cv2.GaussianBlur(gray, (7, 7), 0)
#                 # cv2.imshow("blur",blur)
#                 # cv2.waitKey(0)
#
#                 # Applied inversed thresh_binary
#                 binary = cv2.threshold(blur, 180, 255,
#                                        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#                 # cv2.imshow("binary",binary)
#                 # cv2.waitKey(0)
#
#                 ## Applied dilation
#                 kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
#
#                 thre_mor = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel3)
#                 # cv2.imshow("thresh",thre_mor)
#                 # cv2.waitKey(0)
#                 # cv2.imwrite('Cropped2.jpg', thre_mor)
#
#                 # text = pt.image_to_string(thre_mor,
#                 #                           config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8 --oem 3')
#                 # text1 = pt.image_to_string(thre_mor, config='--psm 11')
#                 # # text = pt.image_to_string(imgRoi,config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8 --oem 3')
#                 # # text1 = pt.image_to_string(imgRoi, config='--psm 11')
#                 #
#                 # print("Tesseract Results :")
#                 # print(text)
#                 # print("*************")
#                 # print(text1)
#
#                 print("EasyOCR Results :")
#                 read = easyocr.Reader(['en'], gpu=False)
#                 ALLOWED_LIST = string.ascii_uppercase + string.digits
#                 result = read.readtext(gray, detail=0, allowlist=ALLOWED_LIST)
#                 print(result)
#
#                 Text = ""
#                 for text in result:
#                     Text += text
#                 print("License Plate : ", Text)
#         # frame_flip = cv2.flip(img, 1)
#         ret, jpeg = cv2.imencode('.jpg', img)
#         return jpeg.tobytes()
