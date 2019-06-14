import json
import os.path as path
from datetime import datetime
from requests_html import HTMLSession

import config

PAGES_LIMIT = 5
TARGET_URL = 'https://jbzd.pl/'
CLIENT_PREFIX = __name__.split('.')[-1]
TIMESTAMP_FNAME = '{}_timestamp.txt'.format(CLIENT_PREFIX)
TIMESTAMP_FILE_PATH = path.join(config.DATA_PATH, TIMESTAMP_FNAME)


def make_filename(ext='html'):
    file_date = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
    return '{prefix}_{date}.{f_ext}'.format(prefix=CLIENT_PREFIX,
                                            date=file_date,
                                            f_ext=ext)


def set_timestamp(images):
    """
    Saving first in line image as a timestamp
    so craler in next iteration won't go further
    than saved one
    """
    first_image_url = images[0][1]
    with open(TIMESTAMP_FILE_PATH, 'w+') as f:
        f.writelines(first_image_url)


def get_timestamp():
    try:
        with open(TIMESTAMP_FILE_PATH, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None


def fetch_page_images(page_body):
    images = page_body.html.find('img[class*="resource-image"]')
    if not images:
        return True, []

    timestamp = get_timestamp()
    cancelled = False
    result = []

    for i in images:
        text, url = i.attrs.get('alt'), i.attrs.get('src')
        if timestamp == url:
            cancelled = True
            break
        result.append([text, url])

    return cancelled, result


def htmlize(images, save_to_file=True):
    body = """
    <html>
        <head>
        <style type="text/css">
            body {{text-align: center;font-family: arial; background-color: #222;}}
            div {{border: 1px solid #333; width: 600px; margin: 45px auto; padding: 5px;}}
            h1 {{color: #fff; font-size: 20px;}}
        </style>
        </head>
        <body>{images}</body>
    </html>
    """
    elem = '<div><h1>{}</h1><img src="{}"></div>'

    img_buff = ''
    for i in images:
        img_buff += elem.format(*i)
    body = body.format(images=img_buff)

    export_filename = make_filename()
    output_path = path.join(config.DATA_PATH, export_filename)

    if save_to_file:
        with open(output_path, 'w+') as f:
            f.writelines(body)

    return body


def get_next_page_url(page_body):
    return page_body.html.find('a[class*="btn-next-page"]')[0].attrs.get('href')


def fetch():
    session = HTMLSession()
    p_body = session.get(TARGET_URL)

    cancelled, images = fetch_page_images(p_body)
    current_page = 1

    while not cancelled:
        if current_page >= PAGES_LIMIT:
            break

        p_body = session.get(get_next_page_url(p_body))
        cancelled, images_list = fetch_page_images(p_body)
        images += images_list
        current_page += 1

    if not images:
        print('::: NOTHING WAS FETCHED, CHEERIO!')
        return None

    set_timestamp(images)
    return images


def dump2json(images):
    json_data = json.dumps(images)
    fname = make_filename('json')
    output_path = path.join(config.DATA_PATH, fname)

    with open(output_path, 'w+') as f:
        f.writelines(json_data)


def jbzd2html(images):
    htmlize(images)
