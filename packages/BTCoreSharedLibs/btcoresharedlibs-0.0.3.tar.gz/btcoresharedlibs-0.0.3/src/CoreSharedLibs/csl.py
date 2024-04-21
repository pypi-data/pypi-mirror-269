# Commonly used modules and functions that I had written up.
# Makes for hopefully easier deployment / reuse.

import re
import logging
from pathlib import Path
import numpy as np
import threading
from queue import Queue


# Helper functions
def char_entry_value_strip(char_entry):
    """
    Takes a string, spits out first set of integers
    :param char_entry: Type: String or Path
    :return: Int
    """
    char_entry_str = str(char_entry)
    return int(re.search(r"\d+", char_entry_str).group())


def listdir_int_match(source, target):
    """
    Function to return first matching int file/folder name from list.
    :param source: List of directory contents or Path object.
    :param target: String to match against.
    :return: String of int value.
    """
    source2 = []
    if isinstance(source, list):
        source2 = [entry.name for entry in source]
    elif isinstance(source, Path):
        source2 = [entry.name for entry in source.iterdir()]

    try:
        result = [j for j in source2 if str(char_entry_value_strip(str(target))) in j][
            0
        ]
    except IndexError:
        logging.info("%s | %s", source, target)
        result = "0"
    return result


def img_to_numpy(image):
    """
    Converts Image to numpy, and skips over the annoying IDE warnings about unexpected type.
    :param image: Image type
    :return: Numpy array
    """
    return np.asarray(image)


def background_only(image):
    """
    Checks for if the image is entirely background, no char sprites.
    :param image: Image type. Takes in image to check.
    :return: Boolean
    """
    # Convert the image to a NumPy array
    image_array = img_to_numpy(image)

    # Check if all elements of the array are the same
    is_single_color = np.all(image_array == image_array[0])

    return is_single_color


def process_list_queue(file_list, func_proc):
    """
    Handles images and prepares them for spreading out of jobs
    :param file_list: List of images. Includes the fill path to image.
    :param func_proc: Function to multi-thread.
    :return: List of cut images. Sequence is preserved. FIFO.
    """
    try:
        q = Queue(maxsize=0)
        numthreads = min(15, len(file_list))
        results = [{} for _ in file_list]
        for i in range(len(file_list)):
            q.put((i, file_list[i]))

        for i in range(numthreads):
            process = threading.Thread(target=func_proc, args=(q, results))
            process.daemon = True
            process.start()
        q.join()
        if len(file_list) > 0:
            print("All complete! Moving on.")
        return results
    except Exception as f:
        logging.error(f"An error occurred: {f}")


def get_filename_from_path(file_path):
    # Define the regex pattern to match a filename
    pattern = r"[\\/]([^\\/]+)$"

    # Use re.search to find the last segment which is the filename
    match = re.search(pattern, file_path)

    if match:
        # Return the matched filename
        return match.group(1)
    else:
        # If no match found, return None
        return None


def pos_int_input():
    verify = True
    char_val = 0
    while verify:
        try:
            char_val = int(input("Please input an integer. : "))
            if char_val < 0:
                raise ValueError("Negative integers are not allowed.")
            else:
                char_verify = input(f"{char_val} entered! Correct? Y/N: ").lower()[
                              :1
                              ]
                while True:
                    if char_verify in ["y", "n"]:
                        if char_verify == "y":
                            print("Understood. Moving on.")
                            verify = False
                        else:
                            print("Understood. Trying again.")
                            verify = True
                        break
                    else:
                        print("Invalid input. Please enter Y or N.")
        except ValueError:
            logging.warning("Invalid entry. Integers only,")
    return char_val
