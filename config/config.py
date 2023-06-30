import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
FROM = os.getenv('FROM')
MONGODB_URL = os.getenv('MONGODB_URL')
DATABASE_NAME = os.getenv('DATABASE_NAME')
USER_COLLECTION_NAME = os.getenv('USER_COLLECTION_NAME')
COUPON_COLLECTION_NAME = os.getenv('COUPON_COLLECTION_NAME')

ERROR_MESSAGE = 'We are facing a techincal issue at this time.'
