import requests
import os
import pandas as pd



def image_downloads(folder_path:str,url:str, counter):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        f = open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {url} - as {folder_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

if __name__=='__main__':
    #https://cdn.ineuron.ai/assets/uploads/thumbnails/63fdad6d87f6119423b4875b.jpg
    persist_image('', 'https://cdn.ineuron.ai/assets/uploads/thumbnails/63fdad6d87f6119423b4875b.jpg', 1)