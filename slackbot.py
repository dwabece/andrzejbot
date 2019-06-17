from time import sleep
import config
import jbzd
import slack


def _return_attachment(text, url):
    return [{'fallback': text, 'image_url': url}]


def post(payload):
    client = slack.WebClient(config.BOT_ACCESS_TOKEN)
    default_payload = {
        'channel': config.SLACK_ROOM,
        'icon_emoji': 'unicorn_face:',
    }
    default_payload.update(payload)

    client.chat_postMessage(**default_payload)


def post_meme(meme_data):
    text, img_url = meme_data
    payload = {
        'text': f'#dailycozncz - {text}',
        'attachments': _return_attachment(text, img_url),
    }

    post(payload)


def spam2slack():
    images = jbzd.fetch()
    if not images:
        return None

    for image in images:
        post_meme(image)
        sleep(.5)
    post({'text': 'No i chuj no i cześć'})
