# from PIL import Image
import argparse
import time
import cv2
import shutil
import os
from detect_table_class import NutritionTableDetector
from crop import crop
from text_detection import text_detection, load_text_model
from process import *
from regex import *
from nutrient_list import *
from spacial_map import *
from matplotlib import pyplot as plt 
def detect_all(img_path, debug):
    dict1=detect(img_path, debug,True)
    print("first scan :",dict1)
    dict2=detect("./data/result/second-input.jpg", debug,False)
    print("second scan :",dict2)
    print("final result :",{**dict2,**dict1})
    return {**dict2,**dict1}
def load_model():
    """
    load trained weights for the model
    """    
    global obj,obj2
    obj = NutritionTableDetector()
    obj2 = NutritionTableDetector()

    print ("Weights Loaded!")

def detect(img_path, debug,firstCall=False):
    """
    @param img_path: Pathto the image for which labels to be extracted
    """

    #Start the time
    start_time = time.time()
    #Make the table detector class and predict the score

    image = cv2.imread(img_path)
    boxes, scores, classes, num  = obj.get_classification(image)
    #Get the dimensions of the image
    width = image.shape[1]
    height = image.shape[0]

    if debug:
        time_taken = time.time() - start_time
        print("Time taken to detect the table: %.5fs" % time_taken)

    #Select the bounding box with most confident output
    ymin = boxes[0][0][0]*height
    xmin = boxes[0][0][1]*width
    ymax = boxes[0][0][2]*height
    xmax = boxes[0][0][3]*width

    # print(xmin, ymin, xmax, ymax, scores[0][0])
    coords = (xmin, ymin, xmax, ymax)

    #Crop the image with the given bounding box
    if(firstCall):
        cropped_image = crop(image, coords, "./data/result/output.jpg", 0, True)

        cropped_image2= crop(image,(0,ymax-((height-ymax)/15),width,height),"./data/result/second-input.jpg", 0, True)
    else:
        cropped_image = crop(image, coords, "./data/result/output2.jpg", 0, True)
    #Apply several filters to the image for better results in OCR
    cropped_image = preprocess_for_ocr(cropped_image, 7)

    if debug:
        cv2.imwrite('./data/result/output-opt.png', cropped_image)

    #detecting the text
    text_blob_list = text_detection(cropped_image)

    if debug:
        time_taken = time.time() - start_time
        print("Time Taken to detect bounding boxes for text: %.5fs" % time_taken)
        # print(text_blob_list)

    text_location_list = []   #store all the metadata of every text box
    nutrient_dict = {}        # Dictionary to store nutrient labels and their values

    counter=0
    #Apply OCR to to blobs and save data in organized dict
    for blob_cord in text_blob_list:
        if debug:
            additional_text=""
            if(firstCall==False):
                additional_text="second"
            counter+=1
            word_image = crop(cropped_image, blob_cord, "./data/result/{}{}.jpg".format(additional_text,counter), 0, True)
        else:
            word_image = crop(cropped_image, blob_cord, "./", 0, False)
            
        _,coord_y,_ = np.shape(word_image)
        
        if coord_y==0:
            continue
        
        word_image = preprocess_for_ocr(word_image)
        if (word_image.shape[1]>0 and word_image.shape[0]>0):
            text = ocr(word_image,1,7)

            if debug:
                print(text)

            if text:
                center_x = (blob_cord[0]+blob_cord[2])/2
                center_y = (blob_cord[1]+blob_cord[3])/2
                box_center = (center_x, center_y)

                new_location = {
                    'bbox': blob_cord,
                    'text': text,
                    'box_center': box_center,
                    'string_type': string_type(text)
                }
                text_location_list.append(new_location)

    #Spatial algorithm that maps all boxes according to their location and append the string
    for text_dict in text_location_list:
        if(text_dict['string_type']==2):
            for text_dict_test in text_location_list:
                if position_definer(text_dict['box_center'][1], text_dict_test['bbox'][1], text_dict_test['bbox'][3]) and text_dict_test['string_type']==1:
                    text_dict['text'] = text_dict['text'].__add__(' '+text_dict_test['text'])
                    text_dict['string_type'] = 0

    fuzdict=make_fuzdict('data/nutrients.txt')
    # print("fuz dict",fuzdict)
    #Add the nutritional label and its value to the nutrient_dict
    for text_dict in text_location_list:

        if(text_dict['string_type']==0):
            text = clean_string(text_dict['text'])

#             if check_for_label(text, make_list('data/nutrients.txt')):
            if fuz_check_for_label(text, fuzdict, debug):
                print("===coming")
                label_name, label_value = get_fuz_label_from_string(text, fuzdict, debug)
                nutrient_dict[label_name] = separate_unit(label_value)

    if debug:
        time_taken = time.time() - start_time
        print("Total Time Taken: %.5fs" % time_taken)

    return nutrient_dict


#main function to test different functions independently
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to the input image")
    ap.add_argument("-d", "--debug", action='store_true', help="print some debug info")
    args = ap.parse_args()
    if args.debug:


# get the current working directory
        current_directory = os.getcwd()

# specify the relative path of the folder to be emptied
        folder_name = 'data/result'
        folder_path = os.path.join(current_directory, folder_name)

# remove the folder and all its contents
        shutil.rmtree(folder_path)

# create an empty folder with the same name
# if you want to keep the folder structure
# if not, skip this step
        os.mkdir(folder_path)

    load_model()
    load_text_model()

   


if __name__ == '__main__':
    main()
