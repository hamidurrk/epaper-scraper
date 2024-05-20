from PIL import Image, ImageDraw
from bs4 import BeautifulSoup
import requests
from io import BytesIO
import os

html_content = """<img data-src="https://images.eprothomalo.com/PA/2012/01/04/Dhaka/dh/5_32/7b7ab4f7_32_mr.jpg" class="img_jpg" page_id="134543" pheight="2840" pwidth="1800" pageno="32" seno="32" xhighres="https://images.eprothomalo.com/PA/2012/01/04/Dhaka/dh/5_32/7b7ab4f719c5851d_32_hr.jpg" highres="https://images.eprothomalo.com/PA/2012/01/04/Dhaka/dh/5_32/7b7ab4f7_32_mr.jpg" pgname="Page" sequence="5" ishdview="0" paywallpage="3" img_0="0" id="pg_id_134543" onload="imgLoad(this);" onerror="imgLoadError();" src="https://images.eprothomalo.com/PA/2012/01/04/Dhaka/dh/5_32/7b7ab4f7_32_mr.jpg" style="display: block;"><div curstory="0" pageid="134543" pageno="32" objtype="2" storyid="990363" orgid="a990363z" class="pagerectangle" style="top: 30px; left: 5px; width: 941px; height: 554px; cursor: pointer; z-index: 5; background-color: rgba(255, 0, 0, 0);" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div><div curstory="1" pageid="134543" pageno="32" objtype="2" storyid="990364" orgid="a990364z" class="pagerectangle" style="top: 593px; left: 5px; width: 748px; height: 662px; cursor: pointer; z-index: 6;" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div><div curstory="2" pageid="134543" pageno="32" objtype="2" storyid="990369" orgid="a990369z" class="pagerectangle" style="top: 1546px; left: 0px; width: 572px; height: 580px; cursor: pointer; z-index: 7;" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div><div curstory="3" pageid="134543" pageno="32" objtype="2" storyid="990368" orgid="a990368z" class="pagerectangle" style="top: 1285px; left: 574px; width: 570px; height: 526px; cursor: pointer; z-index: 8;" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div><div curstory="4" pageid="134543" pageno="32" objtype="2" storyid="990372" orgid="a990372z" class="pagerectangle" style="top: 2126px; left: -5px; width: 773px; height: 304px; cursor: pointer; z-index: 9;" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div><div curstory="5" pageid="134543" pageno="32" objtype="2" storyid="990362" orgid="a990362z" class="pagerectangle" style="top: 23px; left: 943px; width: 393px; height: 563px; cursor: pointer; z-index: 10; background-color: rgba(255, 0, 0, 0);" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div><div curstory="6" pageid="134543" pageno="32" objtype="2" storyid="990366" orgid="a990366z" class="pagerectangle" style="top: 605px; left: 761px; width: 575px; height: 378px; cursor: pointer; z-index: 11;" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div><div curstory="7" pageid="134543" pageno="32" objtype="2" storyid="990371" orgid="a990371z" class="pagerectangle" style="top: 1811px; left: 574px; width: 575px; height: 315px; cursor: pointer; z-index: 12;" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div><div curstory="8" pageid="134543" pageno="32" objtype="2" storyid="990370" orgid="a990370z" class="pagerectangle" style="top: 1274px; left: 0px; width: 569px; height: 268px; cursor: pointer; z-index: 13;" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div><div curstory="9" pageid="134543" pageno="32" objtype="2" storyid="990367" orgid="a990367z" class="pagerectangle" style="top: 986px; left: 759px; width: 569px; height: 262px; cursor: pointer; z-index: 14;" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div><div curstory="10" pageid="134543" pageno="32" objtype="2" storyid="990373" orgid="a990373z" class="pagerectangle" style="top: 2132px; left: 765px; width: 379px; height: 296px; cursor: pointer; z-index: 15;" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div><div curstory="11" pageid="134543" pageno="32" objtype="2" storyid="990365" orgid="a990365z" class="pagerectangle" style="top: 848px; left: 1333px; width: 198px; height: 409px; cursor: pointer; z-index: 16;" autozoom="false" autorotate="false" onmouseover="mouseOver(event,this)" onmouseout="mouseOut(event,this)"></div>"""

output_directory = "cropped_images"

def process_for_article_image(html_content, output_directory):
    soup = BeautifulSoup(html_content, 'html.parser')

    image_url = soup.find('img', class_='img_jpg')['xhighres']

    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    image_width, image_height = image.size

    div_elements = soup.find_all("div", class_="pagerectangle")

    total_width = 0
    total_height = 0

    os.makedirs(output_directory, exist_ok=True)

    for div in div_elements:
        top = int(div['style'].split(';')[0].split(':')[1].strip().replace('px', ''))
        left = int(div['style'].split(';')[1].split(':')[1].strip().replace('px', ''))
        width = int(div['style'].split(';')[2].split(':')[1].strip().replace('px', ''))
        height = int(div['style'].split(';')[3].split(':')[1].strip().replace('px', ''))

        total_width = max(total_width, left + width)
        total_height = max(total_height, top + height)

    rectangles = []
    for i, div in enumerate(div_elements):
        top = int(div['style'].split(';')[0].split(':')[1].strip().replace('px', '')) * image_height / total_height
        left = int(div['style'].split(';')[1].split(':')[1].strip().replace('px', '')) * image_width / total_width
        width = int(div['style'].split(';')[2].split(':')[1].strip().replace('px', '')) * image_width / total_width
        height = int(div['style'].split(';')[3].split(':')[1].strip().replace('px', '')) * image_height / total_height

        cropped_image = image.crop((left, top, left + width, top + height))
        cropped_image.save(os.path.join(output_directory, f"article_{i+1}.jpg"))

        rectangles.append((left, top, left + width, top + height))

    draw = ImageDraw.Draw(image)

    for rect in rectangles:
        draw.rectangle(rect, outline="red")
    
    image.save(os.path.join(output_directory, "output_image.jpg"))

    print("Total Width:", total_width)
    print("Total Height:", total_height)
    
process_for_article_image(html_content, output_directory)