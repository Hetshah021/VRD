from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from detect.camera import VideoCamera
# from detect.camera import PhoneCamera
# from detect.camera import LaptopCamera

# Create your views here.


def index(request):
	return render(request, 'detect.html')


def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')

# def phone_feed(request):
# 	return StreamingHttpResponse(gen(PhoneCamera()),
# 					content_type='multipart/x-mixed-replace; boundary=frame')

# def laptopCam_feed(request):
# 	return StreamingHttpResponse(gen(LaptopCamera()),
# 					content_type='multipart/x-mixed-replace; boundary=frame')



































# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponseRedirect
# from django.core.files.storage import FileSystemStorage
#
# import cv2
# import numpy as np
# import  pytesseract as pt
#
# pt.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
# net = cv2.dnn.readNet('./model/yolov3_training_last.weights', './model/yolov3_testing.cfg')
#
# classes = []
# with open("./model/classes.txt", "r") as f:
#     classes = f.read().splitlines()
#
#
# # Create your views here.
# def detect(request):
#     context = {}
#     img = cv2.imread('./model/Resources/v10.jpg')
#     # img = cv2.resize(img, (640, 480))
#     font = cv2.FONT_HERSHEY_PLAIN
#     colors = np.random.uniform(0, 255, size=(100, 3))
#
#     height, width, _ = img.shape
#
#     blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
#     net.setInput(blob)
#     output_layers_names = net.getUnconnectedOutLayersNames()
#     layerOutputs = net.forward(output_layers_names)
#
#     boxes = []
#     confidences = []
#     class_ids = []
#
#     for output in layerOutputs:
#         for detection in output:
#             scores = detection[5:]
#             class_id = np.argmax(scores)
#             confidence = scores[class_id]
#             if confidence > 0.5:
#                 center_x = int(detection[0] * width)
#                 center_y = int(detection[1] * height)
#                 w = int(detection[2] * width)
#                 h = int(detection[3] * height)
#
#                 x = int(center_x - w / 2)
#                 y = int(center_y - h / 2)
#
#                 boxes.append([x, y, w, h])
#                 confidences.append((float(confidence)))
#                 class_ids.append(class_id)
#
#     indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)
#
#     if len(indexes) > 0:
#         for i in indexes.flatten():
#             x, y, w, h = boxes[i]
#             label = str(classes[class_ids[i]])
#             confidence = str(round(confidences[i], 2))
#             color = colors[i]
#             cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
#             cv2.putText(img, confidence, (x, y), font, 2, (255, 255, 255), 2)
#         imgRoi = img[y:y + h, x:x + w]
#
#     # cv2.imshow('Image', img)
#     # cv2.imshow('Cropped Image', imgRoi)
#     cv2.imwrite('Cropped.jpg', imgRoi)
#     cv2.imwrite('./static/img/Cropped.jpg', imgRoi)
#
#     gray = cv2.cvtColor(imgRoi, cv2.COLOR_BGR2GRAY)
#     # cv2.imshow("gray", gray)
#     # cv2.waitKey(0)
#
#     blur = cv2.GaussianBlur(gray, (7, 7), 0)
#     # cv2.imshow("blur", blur)
#     # cv2.waitKey(0)
#
#     # Applied inversed thresh_binary
#     binary = cv2.threshold(blur, 180, 255,
#                            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#     # cv2.imshow("binary", binary)
#     # cv2.waitKey(0)
#
#     ## Applied dilation
#     kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
#
#     thre_mor = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel3)
#     # cv2.imshow("thresh", thre_mor)
#     # cv2.waitKey(0)
#
#     # text = pt.image_to_string(imgRoi,config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8 --oem 3')
#     text = pt.image_to_string(thre_mor, config='--psm 11')
#     print(text)
#
#     context['text']= text;
#
#     # key = cv2.waitKey(0)
#
#     cv2.destroyAllWindows()
#
#     return render(request, 'detect.html', context)