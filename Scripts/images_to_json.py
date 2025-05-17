import os
import json

def update_image_paths(image_folder='images', json_path='posts.json'):
    # Load all image filenames from the image folder
    image_filenames = os.listdir(image_folder)
    
    # Create a map: post_id -> image filename
    image_map = {}
    for filename in image_filenames:
        if filename.startswith("insta_image_post_") and filename.endswith((".jpg", ".png", ".jpeg")):
            post_id = filename.split("post_")[-1].split(".")[0]
            image_map[post_id] = filename

    # Load the JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        posts = json.load(f)

    # Update the image_path for each post if image exists
    for post in posts:
        post_id = post.get("post_id")
        if post_id in image_map:
            post["image_path"] = image_map[post_id]

    # Save the updated JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print("Image paths updated successfully.")

# Example usage:
# update_image_paths()


update_image_paths()
