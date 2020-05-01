from PIL import Image
import pytesseract
import argparse
import cv2
import os
import pandas as pd
import sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--function", required=True, help="function to perform (ocr, csv)")
    ap.add_argument("-g", "--grayscale", type=bool, default=False, help="whether to grayscale the image")
    ap.add_argument("-i", "--image", required=True, help="path to the input image")
    ap.add_argument("-r", "--rows", type=int, required=True, help="number of rows")
    ap.add_argument("-c", "--cols", type=int, required=True, help="number of columns")
    
    args = vars(ap.parse_args())

    fn = args["function"]

    if fn == "ocr":
        doOcr(args["image"], args["grayscale"])
    elif fn == "csv":
        makeCsv(rows=args["rows"], columns=args["cols"])
    else:
        print("Invalid function provided. Choose either 'ocr' or 'csv'")

def doOcr(image, makeGrey):
    image = cv2.imread(image)
    if makeGrey:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, image)

    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)

    f = open("imagetext.txt", "w")
    f.write(text)
    f.close()

def makeCsv(rows, columns):

    indices = []
    data = {}

    # read the file
    lines = []
    with open("imagetext.txt") as f:
        for line in f:
            if not line.isspace():
                lines.append(line.replace('\n', ''))

    lineIdx = 0

    while lineIdx < rows:
        indices.append(lines[lineIdx])
        lineIdx += 1

    linePtr = 0
    currentCol = ''

    while lineIdx <  len(lines):
        if linePtr == 0:
            currentCol = lines[lineIdx]
            data[currentCol] = [] 
        else:
            data[currentCol].append(lines[lineIdx])
        
        if linePtr >= rows:
            linePtr = 0
        else:
            linePtr += 1
        lineIdx += 1

    df = pd.DataFrame(data, indices)

    df.to_csv('output.csv')

if __name__ == "__main__":
    main()