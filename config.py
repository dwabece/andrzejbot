import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

# file .env is required

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, 'data')

SLACK_ROOM = 'jbzd'
if os.environ.get('ENV') == 'TEST':
    SLACK_ROOM = 'andrzejtest'

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
BOT_ACCESS_TOKEN = os.getenv('BOT_ACCESS_TOKEN')


RABBIT_HOST = os.getenv('RABBIT_HOST')
RABBIT_USER = os.getenv('RABBIT_USER', 'guest')
RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD', 'guest')
RABBIT_URL = f'amqp://{RABBIT_USER}:{RABBIT_PASSWORD}@{RABBIT_HOST}:5672/'

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_TIMESTAMP_FIELD = 'jbzd'

MEMEPOST_INTERVAL = 60 * int(os.getenv('INTERVAL_DZIDA', 10))
