#!/usr/bin/env python3

from PIL import Image
import numpy as np
# resolution ??? 

def get_input_data(text):
    # result = input("Enter input (id(opt.);img_to_process.jpg;[emotions];[width];[height]): ").split(";")
    # text = "0;emoji_0.jpg;['happy'];[437];[284]"
    result = text.split(";")
    if len(result) == 4:
        i = 0
    elif len(result) == 5:
        i = 1
    else:
        print("Input not correct")
        return 1
    data = {
            "file": result[0 + i],
            "moods": result[1 + i].split(","),
            "x_s": int(result[2 + i].strip("[]")),
            "y_s": int(result[3 + i].strip("[]")),
            "em_h": 50,
            "em_w": 50
            }
    return data

def get_test_data():
    with open(TEST_DATA_FILE, "r") as file:
        for line in file:
            data = get_input_data(line.strip()) # parsing and error handling
    try:
        with Image.open(DATABASE_PATH + data["file"]) as image:
            # data["img"] = image #(image.convert("RGB")).getdata() # convert to rgb from jpg for array representation
            data["img"] = np.array(image)
            data["w"], data["h"] = image.size
            emoji_array = data["img"][data["y_s"]:data["y_s"] + data["em_h"], data["x_s"]:data["x_s"] + data["em_w"]]
        return emoji_array
    except OSError as e:
        print(f"Error opening image: {e}")
        return 1  

def handle_input_errors(img, moods, img_width, img_height):
    return

def check_for_emo(data, emoji_data):
    # draw a circle
    # center = [data["em_w"], data["em_h"]]

    # check circle corners - top center, left center, bottom center, 
    # if emoji_data[0][data["em_w"]//2][0] > 210  or emoji_data[data["em_h"] // 2][0][0] > 210 :
    # and   and emoji_data[data["em_h"] / 2][data["em_w"]][0] > 210: # too light, almost white
        # return 1
    # for row in emoji_data:
    #     for pixel in row:
    #         if pixel[0] != 255:
    #             print(f"here ({emoji_data[row][column]})\n")
    #             return 0
    if np.all(array1 == array2):  # Output: True
        return 0

    return 1
    

# iterates the image by blocks with dimensions emoji_w x emoji_h
# stores the pixel information of the block
def find_emo(data):
    test_array = get_test_data()
    for y in range (data["h"] - data["em_h"] + 1): # for each row
        for x in range(data["w"] - data["em_w"] + 1): # for each pixel in a row (columns in that row)
            window = data["img"][y:y + data["em_h"], x:x + data["em_w"]]
            if (check_for_emo(data, window, test_array) == 0):
                result = {"x": x, "y": y}
                print(f"found at {result} ({window[y, x]})")
            else:
                x = x + (data["em_w"]//2)
            #   print(f"here: {data['img'][w + data['em_w']][data['em_h']][0]}")
            # emoji_array = data["img"][y:y + data["em_h"], x:x + data["em_w"]]
            # emoji_array = ((data["img"].crop((x, y, x + data["em_w"], y + data["em_h"]))).convert("RGB")).getdata() # convert to rgb from jpg for array representation
    #return result

  

# input: (0;)emoji_0.jpg;['happy'];[437];[284]
def main():
    # handle_input_errors(img, moods, x_s, y_s)
    data = get_input_data("1;emoji_1.jpg;['happy'];[361];[82]")
    # loading the picture and error handling
    try:
        with Image.open(DATABASE_PATH + data["file"]) as image:
            # data["img"] = image #(image.convert("RGB")).getdata() # convert to rgb from jpg for array representation
            data["img"] = np.array(image)
            data["w"], data["h"] = image.size
            find_emo(data)
    except OSError as e:
        print(f"Error opening image: {e}")
        return 1
    
   

    # calculate how may threads we need, calculate size of each block for a thread and start them
    # cleanup ?

# prevent file being executed when importing it elsewhere
if __name__ == "__main__":
    DATABASE_PATH = "data/basic/dataset/"
    TEST_DATA_FILE = "data/basic/labels.csv"
    main()
