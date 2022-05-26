import sys


def mrz_opencv(bytes=None, path=None):
    from imutils import contours
    import imutils
    import numpy as np
    import cv2
    import pytesseract

    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))

    if not path:
        nparr = np.fromstring(bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    else:
        image = cv2.imread(path)
    image = imutils.resize(image, height=600)
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (H, W) = grey.shape
    gray = cv2.GaussianBlur(grey, (3, 3), 0)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)

    # cv2.imshow("blackhat", blackhat)
    # cv2.waitKey(0)

    grad = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    grad = np.absolute(grad)
    (minVal, maxVal) = (np.min(grad), np.max(grad))
    grad = (grad - minVal) / (maxVal - minVal)
    grad = (grad * 255).astype('uint8')

    # cv2.imshow("Gradient", grad)
    # cv2.waitKey(0)

    grad = cv2.morphologyEx(grad, cv2.MORPH_CLOSE, rectKernel)
    thresh = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # cv2.imshow("Rect close", thresh)
    # cv2.waitKey(0)

    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, (30, 30))
    thresh = cv2.dilate(thresh, None, iterations=11)

    # cv2.imshow("Square close", thresh)
    # cv2.waitKey(0)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = contours.sort_contours(cnts, method='bottom-to-top')[0]
    mrzBox = None

    # print(cnts)
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        precentWidth = w / float(W)
        precentHeight = h / float(H)

        if precentWidth > 0.8 and precentHeight > 0.04:
            mrzBox = (x, y, w, h)
            break

    if mrzBox is None:
        print('[INFO] not be found')
        sys.exit(0)
    (x, y, w, h) = mrzBox
    pX = int((x + w) * 0.03)
    pY = int((y + h) * 0.03)
    (x, y) = (x - pX, y - pY)
    (w, h) = (w + (pX * 2), h + (pY * 2))
    mrz = image[y:y + h, x:x + w]

    mrzText = pytesseract.image_to_string(mrz)
    mrzText = mrzText.replace(' ', '')

    return mrzText
    # cv2.imshow("MRZ", mrz)
    # cv2.waitKey(0)


def mrz_passporteye():
    from passporteye import read_mrz
    from pprint import pprint

    mrz = read_mrz("../../3.jpg")
    pprint(mrz.to_dict())


if __name__ == '__main__':
    mrz_opencv(path='../../3.jpg')
