import os


#GETS BASE OR SOURCE PATH AND INNER PATH OR PATH TO BE ADDED. IT JOINS BOTH TO ONE PATH
def join_paths(base_path, added_path):
    return os.path.join(base_path, added_path)