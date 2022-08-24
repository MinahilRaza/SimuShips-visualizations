# import required libraries 
import xml.etree.ElementTree as ET
import numpy as np
import os
import cv2, json
import shutil
from PIL import Image

# this function reads the palette image file and returns the pixel values against each color
def GetColorMap(palette_image:str):
    im = Image.open(palette_image, 'r')
    width, height = im.size
    pixel_values = list(im.getdata())
    pixel_values = np.delete(np.array(pixel_values), -1, axis = 1)
    pixel_values = np.array(pixel_values).reshape((width, height, 3))
    return pixel_values

# this function gets the colorID for each pixel value
def GetColorID(color, pixel_values):
    i = 0
    bestI = 0
    bestDist = 999
    color = color[:-1]
    for col in pixel_values:
        if (np.array(col[0]) == np.array(color)).all():
            return i
        dist = np.absolute((col[0] - color)).sum()
        if dist <= 1:
            print("Near miss color: ", color)
            return i
        if dist < bestDist:
            bestI = i
            bestDist = dist
        i+=1
    return bestI

# this funciton maps categories to colorIDs from the GroundTruthColorMapping.xml file
def MapColorPalette(xml_file:str):
    mytree = ET.parse(xml_file)
    myroot = mytree.getroot()

    categories_to_colors = {}
    ordered_categories = [] # array is enough, ids are the key to the category name
    for i in range(256) :
        ordered_categories.append("Unknown")

    for rule in myroot.iter("Rule"):
        colorID = rule.attrib.get('colorID')
        colorRange = rule.attrib.get('colorRange')		
        color_start = color_end = 0
        if colorID:
            color_start = color_end = int(colorID)
        if colorRange:
            color_start = int(colorRange.split(':')[0])
            color_end = int(colorRange.split(':')[1])
        while color_start <= color_end:
            category = rule.attrib.get('category')
            if not category:
                print("error, no categry found in the rule: ",rule)
                continue
            ordered_categories[color_start] = category
            if categories_to_colors.get(category) :
                if color_start not in categories_to_colors[category]: 
                    categories_to_colors[category].append(color_start)
            else:
                categories_to_colors[category] = [color_start]
            color_start += 1
    return categories_to_colors, ordered_categories

# this function returns a dictionary with color mapping
def GetCategoriesDict(categories_to_colors):
    categories_text = {}
    for i, cat in enumerate(categories_to_colors):
        if cat== 'default':
            continue
        categories_text[i] = cat
    return categories_text

# get boxes on the image. Each box has 4 parameters 
# (x,y) is centre of the box
# w is the width and h is the height
def GetBoxes(image_gt:str):
    mask = np.array(Image.open(image_gt))
    box_list = []
    for color in  np.unique(mask.reshape(-1, mask.shape[2]), axis=0 ):
        lower = np.array(color, dtype="uint8")
        upper = np.array(color, dtype="uint8")
        img_mask = cv2.inRange(mask, lower, upper)
        
        thresh = cv2.threshold(img_mask,128,255,cv2.THRESH_BINARY)[1]
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        if len(contours)==2:
            for cntr in contours: 
                x, y, w, h = cv2.boundingRect(cntr)
                count = np.sum(np.all(mask == color, axis=2))
                box_list.append((x,y,w,h, color, int(count)))
        else:
            x, y, w, h = cv2.boundingRect(img_mask)
            count = np.sum(np.all(mask == color, axis=2))
            box_list.append((x,y,w,h, color, int(count)))
        
        
        
        #x, y, w, h = cv2.boundingRect(img_mask)
        #count = np.sum(np.all(mask == color, axis=2))
        #box_list.append((x,y,w,h, color, int(count)))
    return box_list

# get a dictionary of boxes on the image
def GetBoxesJson(box_list, categories_to_colors, ordered_categories, pixel_array):
    box_text = []
    for (x,y,w,h, color,num_pix) in box_list:
        colorID = GetColorID(color, pixel_array)
        category = ordered_categories[colorID]
        if category == "Unknown":
            continue
        bbox = [x, y, w, h]
        colorrec = (int(color[0]), int(color[1]),int(color[2]))#rgb
        box_str = {"category": category, "bbox":bbox,"color":colorrec, "instance_id":colorID, "num_pixels":num_pix}
        box_text.append(box_str)
    return box_text

# Get a dictionary of categories. This specifies which number is used for each category
def GetCategoriesJson(categories_to_colors):
    categories_text = {}
    for i, cat in enumerate(categories_to_colors):
        categories_text[cat] = i
    categories_text.pop('default')
    return categories_text

# generate image information in a json format
def GetImageJson(image_file:str):
    image_text = []
    img = Image.open(image_file)
    width, height = img.size
    image_text.append({"file_name":image_file,"width":width, "height": height, "license":"AILiveSim Confidential"})
    return image_text
