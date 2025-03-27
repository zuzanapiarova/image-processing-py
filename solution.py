#!/usr/bin/env python3

# resolution vs size ???
# handle input errors 
# threads ?

import numpy as np
from PIL import Image

ERROR = 1
SUCCESS = 0
DATABASE_PATH = "data/basic/dataset/"
TO_SEARCH_FILE = "data/basic/labels.csv"
EMOJI_DATA_FILE = "data/basic/emojis.csv"
MASK_TOLERANCE = 240
ACCEPT_MATCH_TOLERANCE = 95 # in percent
MINIMAL_MATCH_TOLERANCE = 50 # in percent
NO_MATCH = 10 # in percent

################################ GETTING EMOJI DATA #####################################

# creates a map of emoji which is an array with 1 in place of emoji and 0 in place of background
def mask_emoji(emoji_square):
    mask = np.all(emoji_square > MASK_TOLERANCE, axis=-1).astype(int) # checks if the z axis(rgb values) all fulfill requirement
    inverse_mask = 1 - mask
    return inverse_mask

# checks the images where the emojis are
# stores 2D array of emoji with size em_h x em_w
# if multiple emoji faces, can accept more and store them in array
def get_emoji_collection():
    emoji_collection=[]
    with open(EMOJI_DATA_FILE, "r") as file:
        next(file) # jumps over the first line containing column names
        for line in file:
            data = get_input_data(line.strip()) # parsing
            try:
                with Image.open(DATABASE_PATH + data["file"]) as image:
                    img = np.array(image) 
                    emoji_square = img[data["y_s"]:data["y_s"] + data["em_h"], data["x_s"]:data["x_s"] + data["em_w"]] # cropped square of the emoji,
                    emoji_data = {
                                    "id": data["id"],
                                    "arr": emoji_square,
                                    "mask": mask_emoji(emoji_square), # keeps only relevant emoji data - where there is color (some deviation allowed),
                                    "color": "black", 
                                    "mood": data["mood"],
                                    "h": data["em_h"],
                                    "w": data["em_w"]
                                    # size will prob be added
                                 }
                    # binary_image = Image.fromarray(emoji_data["mask"] * 255)  # Multiply by 255 to make it visible
                    # binary_image.show()
                emoji_collection.append(emoji_data)
            except OSError as e:
                print(f"Error opening image: {e}")
                return ERROR  
    return emoji_collection

################################ GETTING INPUT DATA OF IMAGE TO PROCESS #####################################

# gets data from the description line - img name, moods, emoji size, coords if provided
def get_input_data(text):
    result = text.split(";")
    if len(result) != 5:
        print("Input not correct")
        return ERROR
    data = {
            "id": int(result[0]),
            "file": result[1],
            "mood": result[2].split(","),
            "x_s": int((result[3].strip("[]"))),
            "y_s": int((result[4].strip("[]"))),
            "em_h": 50,
            "em_w": 50
            }
    return data

# WORKS - USES MASKS
# returns data of the emoji it matched with the most, or None if match was < 50 %
# def check_for_emo(data, window, height, width, emoji_collection):
#     best_match = MINIMAL_MATCH_TOLERANCE # minimum match, else nothing is returned
#     result = None
#     # for emoji in emoji_collection:
#     emoji = emoji_collection[0]
#    #if emoji["h"] == height and emoji["w"] == width:
#     matches_map = (window[emoji["mask"] == 1] == emoji["arr"][emoji["mask"] == 1])
#     matches_count = np.sum(matches_map) # count matches
#     total_count = np.sum(emoji["mask"]) # count total emoji pixels
#     try:
#         match = matches_count / total_count * 100 # get percentage of match
#         if (match < NO_MATCH):
#             return  None
#         print(f"Match for emoji {emoji["id"]}: {match} %")
#         if match > best_match:
#             best_match = match
#             result = emoji 
#             result["percent"] = match
#             # result["mask"] = window[emoji["mask"] == 1]
#         if match > ACCEPT_MATCH_TOLERANCE: # if result is sufficient do not check the rest
#             return result
#     except ZeroDivisionError as e:
#         print("Cannot divide by 0: {e}")
#     # different colors ?
#     # try rotations ?
#     return result
def check_for_emo(img, window, width, height, emoji_collection):
    if np.allclose(window, emoji_collection[0]["arr"], atol=10):  # Adjust tolerance as needed
        diff = np.abs(window - emoji_collection[0]["arr"])
        pixel_differences = np.any(np.abs(diff) > 5, axis=-1)
        # Count how many values in the array are smaller than 10
        count_small_differences = np.count_nonzero(pixel_differences)
        print(f"Images are nearly identical, difference {count_small_differences} ({count_small_differences / (width * height) * 100} %)")
        return True
    else:
        return False

 
# iterates the image by blocks with dimensions emoji_w x emoji_h
# stores the pixel information of the block
# return list of possible results
def search_frames(img, emoji_collection):
    results=[]
    for y in range (img["h"] - img["em_h"] + 1): # for each row
        for x in range(img["w"] - img["em_w"] + 1): # for each pixel in a row (=columns)
            window = img["img"][y:y + img["em_h"], x:x + img["em_w"]] # cut out part of image in size em_w x em_h
            new_match = check_for_emo(img, window, img["em_w"], img["em_h"], emoji_collection)
            if new_match:
                result = {
                            "x": x,
                            "y": y
                         }
                print(f"New match at {result['x'], result['y']}")
                # print(result)
                results.append(result)
    print(f"For {img['id']}) found {len(results)} results.")
    return results 

# def get_test_input():
#     success = 0
#     count = 0 

#     try: 
#         with open(TO_SEARCH_FILE, "r") as file:
#             next(file)
#             for line in file:
#                 #     data = get_input_data(line.strip())
#                 #     with Image.open(DATABASE_PATH + data["file"]) as image:
#                 #         data["img"] = np.array(image)
#                 #         data["w"], data["h"] = image.size
#                 #     # all data is collected into results array
#                 #     results = search_frames(data, emoji_collection)
           
#     except OSError as e:
#         print(f"Error opening input file: {e}")
#         return ERROR

# def get_test_output(data, test_input):
#     if results:
#             for result in results:
#                 print(f"{data["id"]}) Found at: {result["x"], result["y"]}")
#                 if result["x"] == data["x_s"] and result["y"] == data["y_s"]:
#                     print(f"{data['id']}) matches !")
#                     success += 1
#                 else:
#                     print(f"{data['id']}) does not match !")   
#     except OSError as e:
#         print(f"Error opening image: {e}")
#         return ERROR
#     if results:
#     for result in results:
#         print(f"{data["id"]}) Found at: {result["x"], result["y"]}")
#         if result["x"] == data["x_s"] and result["y"] == data["y_s"]:
#             print(f"{data['id']}) matches !")
#             success += 1
#         else:
#             print(f"{data['id']}) does not match !")   
#         count += 1
#     print(f"Success rate: {success}/{count} ({success/count}%)")

# gets the collection of emoji data 
# gets data of the input image
def main():
    emoji_collection = get_emoji_collection() # collection of optimized emoji data to earch for 
    print(f"Searching for {len(emoji_collection)} emojis.")
    input = "2;emoji_10.jpg;['happy'];[310];[207]"
    try:
        img = get_input_data(input.strip())
        with Image.open(DATABASE_PATH + img["file"]) as image:
            img["img"] = np.array(image)
            img["w"], img["h"] = image.size
        results = search_frames(img, emoji_collection) # all identified frames are collected into results array
        print(f"final results: {len(results)}")
    except OSError as e:
        print(f"Error opening image: {e}")
        return ERROR

# prevent file being executed when importing it elsewhere
if __name__ == "__main__":
    main()
