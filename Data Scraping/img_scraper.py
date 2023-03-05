import requests
import os
import pandas as pd
import mysql.connector


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
    
    conn = mysql.connector.connect(user='root', password='MyLocal@pass@8155',database='ineuron_data',host='localhost')
    mycursor = conn.cursor(buffered=True)

    mycursor.execute('select img_link from course_details;')
    img_links = mycursor.fetchall()
    df = pd.DataFrame(img_links).to_dict('list')
    conn.close()
    for i in range(len(df[0])):
        row_url = df[0][i]
        #https://cdn.ineuron.ai/assets/uploads/thumbnails/63fdad6d87f6119423b4875b.jpg
        image_downloads('/home/lol/Desktop/data_test/images', f'https://cdn.ineuron.ai/assets/uploads/thumbnails/{row_url}', i+1)
        