import pytesseract
import base64
from PIL import Image
import cv2
from io import StringIO, BytesIO
import numpy as np

def readb64(base64_string):
    # nparr = np.fromstring(base64_string.decode('base64'), np.uint8)
    im_bytes = base64.b64decode(base64_string)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img


def detectText(base64_string):
    img = readb64(base64_string)
    img = cv2.copyMakeBorder(img,50,50,50,50,cv2.BORDER_CONSTANT)
    # cv2.imshow('text', img)
    # cv2.waitKey(0)
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
    pytesseract.pytesseract.tesseract_cmd = r'/app/.apt/usr/share/tesseract-ocr/4.00/tessdata'
    # convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # threshold the grayscale image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # use morphology erode to blur horizontally
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (151, 3))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)

    # use morphology open to remove thin lines from dotted lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 17))
    morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

    # find contours
    cntrs = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntrs = cntrs[0] if len(cntrs) == 2 else cntrs[1]

    # find the topmost box
    ythresh = 1000000
    for c in cntrs:
        box = cv2.boundingRect(c)
        x,y,w,h = box
        if y < ythresh:
            topbox = box
            ythresh = y

    # Draw contours excluding the topmost box
    result = img.copy()
    for c in cntrs:
        box = cv2.boundingRect(c)
        print(box)
        if box != topbox:
            x,y,w,h = box
            cv2.rectangle(result, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # write result to disk
    boxes = pytesseract.image_to_string(thresh,lang='eng')
    f = open("demofile3.txt", "w")
    f.write(boxes)
    f.close()

    cv2.imwrite("text_above_lines_threshold.png", thresh)
    # cv2.imwrite("text_above_lines_morph.png", morph)
    # cv2.imwrite("text_above_lines_lines.jpg", result)

    #cv2.imshow("GRAY", gray)
    # cv2.namedWindow('THRESH', cv2.WINDOW_NORMAL)
    # cv2.imshow("THRESH", thresh)
    # cv2.imshow("MORPH", morph)
    # cv2.imshow("RESULT", result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return boxes

if __name__ == "__main__":
    pass