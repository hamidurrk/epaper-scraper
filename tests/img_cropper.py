from PIL import Image, ImageDraw
from bs4 import BeautifulSoup
import requests
from io import BytesIO
import os
import re

html_content = """<div class="image_layer turn-page p10 active" pgids="134398" id="image_layer134398" style="width: 869px; height: 1373.5px; position: absolute; inset: 0px auto auto 0px; transform-origin: 0% 100% 0px;"><img data-src="https://images.eprothomalo.com/PA/2012/01/01/Dhaka/dh/5_10/43d8178d_10_mr.jpg" class="img_jpg" page_id="134398" pheight="2808" pwidth="1800" pageno="10" seno="10" xhighres="https://images.eprothomalo.com/PA/2012/01/01/Dhaka/dh/5_10/43d8178d16c5f22b_10_hr.jpg" highres="https://images.eprothomalo.com/PA/2012/01/01/Dhaka/dh/5_10/43d8178d_10_mr.jpg" pgname="Page" sequence="5" ishdview="0" paywallpage="3" img_0="0" id="pg_id_134398" onerror="onError(this);" style="display: block;" src="https://images.eprothomalo.com/PA/2012/01/01/Dhaka/dh/5_10/43d8178d_10_mr.jpg"><img style="display:none" src="https://epaper.prothomalo.com//img/slow-net.gif?v=610" class="pg_load_img" id="loading_img_slow134398"><div curstory="0" pageid="134398" pageno="10" objtype="2" storyid="989523" orgid="a989523z" class="pagerectangle" style="top: 331px; left: 109px; width: 328px; height: 395px; cursor: pointer; z-index: 5; background-color: rgba(255, 0, 0, 0);" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div><div curstory="1" pageid="134398" pageno="10" objtype="2" storyid="989527" orgid="a989527z" class="pagerectangle" style="top: 17px; left: 433px; width: 434px; height: 246px; cursor: pointer; z-index: 6; background-color: rgba(255, 0, 0, 0);" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div><div curstory="2" pageid="134398" pageno="10" objtype="2" storyid="989525" orgid="a989525z" class="pagerectangle" style="top: 269px; left: 535px; width: 216px; height: 290px; cursor: pointer; z-index: 7; background-color: rgba(255, 0, 0, 0);" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div><div curstory="3" pageid="134398" pageno="10" objtype="2" storyid="989528" orgid="a989528z" class="pagerectangle" style="top: 188px; left: -28px; width: 267px; height: 207px; cursor: pointer; z-index: 8; background-color: rgba(255, 0, 0, 0);" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div><div curstory="4" pageid="134398" pageno="10" objtype="2" storyid="989524" orgid="a989524z" class="pagerectangle" style="top: 262px; left: 431px; width: 110px; height: 462px; cursor: pointer; z-index: 9; background-color: rgba(255, 0, 0, 0);" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div><div curstory="5" pageid="134398" pageno="10" objtype="2" storyid="989521" orgid="a989521z" class="pagerectangle" style="top: 402px; left: 2px; width: 106px; height: 332px; cursor: pointer; z-index: 10; background-color: rgba(255, 0, 0, 0);" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div><div curstory="6" pageid="134398" pageno="10" objtype="2" storyid="989526" orgid="a989526z" class="pagerectangle" style="top: 262px; left: 751px; width: 109px; height: 306px; cursor: pointer; z-index: 11; background-color: rgba(255, 0, 0, 0);" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div></div>"""
output_directory = "cropped_images/test"

def process_for_article_image(html_content, output_directory):
    soup = BeautifulSoup(html_content, 'html.parser')

    pagerectangle_page_ids = set(div['pageid'] for div in soup.find_all("div", class_="pagerectangle"))
    print("Pagerectangle page IDs:", pagerectangle_page_ids)

    os.makedirs(output_directory, exist_ok=True)

    for img_tag in soup.find_all('img', class_='img_jpg'):
        img_page_id = img_tag.get('page_id')
        
        if img_page_id in pagerectangle_page_ids:
            image_layer_elements = [div for div in soup.find_all("div", class_="image_layer") if div['id'].replace('image_layer', '') in pagerectangle_page_ids]
            print(image_layer_elements)
            for image_layer in image_layer_elements:
                print(f"Found image_layer with page_id: {image_layer['id'].replace('image_layer', '')}")
                print(image_layer['style'])
                style_string = image_layer['style']
                width_pattern = r'width:\s*([\d.]+)px'
                height_pattern = r'height:\s*([\d.]+)px'
                
                width_match = re.search(width_pattern, style_string)
                height_match = re.search(height_pattern, style_string)
                
                total_width = int(float(width_match.group(1))) if width_match else None
                total_height = int(float(height_match.group(1))) if height_match else None
            
            image_url = img_tag['xhighres']
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            # image = image.resize((869, 1373))
            image_width, image_height = image.size

            div_elements = [div for div in soup.find_all("div", class_="pagerectangle") if div['pageid'] == img_page_id]


            for div in div_elements:
                top = int(div['style'].split(';')[0].split(':')[1].strip().replace('px', ''))
                left = int(div['style'].split(';')[1].split(':')[1].strip().replace('px', ''))
                width = int(div['style'].split(';')[2].split(':')[1].strip().replace('px', ''))
                height = int(div['style'].split(';')[3].split(':')[1].strip().replace('px', ''))

                # total_width = 869
                # total_height = 1373

            rectangles = []
            for i, div in enumerate(div_elements):
                top = int(div['style'].split(';')[0].split(':')[1].strip().replace('px', '')) * image_height / total_height
                left = int(div['style'].split(';')[1].split(':')[1].strip().replace('px', '')) * image_width / total_width
                width = int(div['style'].split(';')[2].split(':')[1].strip().replace('px', '')) * image_width / total_width
                height = int(div['style'].split(';')[3].split(':')[1].strip().replace('px', '')) * image_height / total_height

                cropped_image = image.crop((left, top, left + width, top + height))
                cropped_image.save(os.path.join(output_directory, f"article_{img_page_id}_{i+1}.jpg"))

                rectangles.append((left, top, left + width, top + height))

            draw = ImageDraw.Draw(image)

            for rect in rectangles:
                draw.rectangle(rect, outline="red")
            
            image.save(os.path.join(output_directory, f"output_image_{img_page_id}.jpg"))

            print("Total Width:", total_width)
            print("Total Height:", total_height)
        else:
            # print(f"Image with page_id {img_page_id} not found")
            pass
process_for_article_image(html_content, output_directory)