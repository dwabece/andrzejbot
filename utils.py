import json
import redis
import requests
import config


def make_filename(base, ext='html'):
    f_date = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
    return f'{base}_{f_date}.{ext}'


def _get_redis():
    return redis.Redis(
        host=config.REDIS_HOST,
        port=6379, db=0
    )


def set_timestamp(images):
    """
    Saving first in line image as a timestamp
    so craler in next iteration won't go further
    than saved one
    """
    redis_ = _get_redis()
    redis_.set(config.REDIS_TIMESTAMP_FIELD, images[0][1])


def get_timestamp():
    redis_ = _get_redis()
    timestamp = redis_.get(config.REDIS_TIMESTAMP_FIELD)
    if timestamp:
        return timestamp.decode('utf-8')


def dump2json(images):
    json_data = json.dumps(images)
    fname = make_filename('json')
    output_path = path.join(config.DATA_PATH, fname)

    with open(output_path, 'w+') as f:
        f.writelines(json_data)


def dump2html(images, save_to_file=True):
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

    export_filename = utils.make_filename('jbzd')
    output_path = path.join(config.DATA_PATH, export_filename)

    if save_to_file:
        with open(output_path, 'w+') as f:
            f.writelines(body)

    return body


def fetch_page(url: str):
    result = requests.get(url)
    result.raise_for_status()

    return result.content
