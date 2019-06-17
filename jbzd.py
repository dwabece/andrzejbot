from requests_html import HTMLSession
import utils

PAGES_LIMIT = 2
TARGET_URL = 'https://jbzd.pl/'
CLIENT_PREFIX = __name__.split('.')[-1]


def fetch_page_images(page_body):
    images = page_body.html.find('img[class*="resource-image"]')
    if not images:
        return True, []

    timestamp = utils.get_timestamp()
    cancelled = False
    result = []

    for i in images:
        text, url = i.attrs.get('alt'), i.attrs.get('src')
        if timestamp == url:
            cancelled = True
            break
        result.append([text, url])

    return cancelled, result


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

    utils.set_timestamp(images)
    return images
