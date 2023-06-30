from datetime import datetime

from flask import Flask, request

from chatgpt.logger import logging
from chatgpt.helper.database_api import get_user, get_coupon, update_coupon, update_user, update_messages, create_user
from chatgpt.helper.twilio_api import send_message
from chatgpt.helper.utils import generate_messages
from chatgpt.helper.conversation import chat_completion

logger = logging.getLogger(__name__)


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return 'OK', 200


@app.route('/twilio', methods=['POST'])
def twilio():
    try:
        logger.info('A new twilio request...')
        data = request.form.to_dict()
        query = data['Body']
        sender_id = data['From']
        user_name = data['ProfileName']

        logger.info(sender_id)
        logger.info(query)
        logger.info(user_name)

        user = get_user(sender_id)

        if user:
            words = query.split(' ', maxsplit=1)
            if words[0] == '/code':
                coupon_code = words[1]
                coupon = get_coupon(coupon_code)
                if coupon:
                    update_user(
                        sender_id,
                        {
                            'messageCount': user['messageCount'] + int(coupon['messages'])
                        }
                    )
                    update_coupon(
                        coupon_code,
                        {
                            'used': True,
                            'userId': sender_id,
                            'userAt': datetime.now().strftime('%d/%m/%Y, %H:%M')
                        }
                    )
                    send_message(
                        sender_id, f'You have successfully redeemed coupon {coupon_code}, {coupon["messages"]} messages are added to your account.')
                else:
                    send_message(
                        sender_id, f'The coupon {coupon_code} is either used or invalid.')
            elif user['messageCount'] == 0:
                send_message(
                    sender_id, 'You have reached the maximum limit of free messages, please subscribe for more messages using /code YOURCOUPONCODE')
            else:
                messages = generate_messages(user['messages'], query)
                response = chat_completion(messages)
                update_messages(sender_id, query, response, user['messageCount'])
                send_message(sender_id, response)
        else:
            # if not create
            messages = generate_messages([], query)
            response = chat_completion(messages)
            message = {
                'query': query,
                'response': response,
                'createdAt': datetime.now().strftime('%d/%m/%Y, %H:%M')
            }
            user = {
                'userName': user_name,
                'senderId': sender_id,
                'messages': [message],
                'messageCount': 10,
                'mobile': sender_id.split(':')[-1],
                'channel': 'WhatsApp',
                'is_paid': False,
                'created_at': datetime.now().strftime('%d/%m/%Y, %H:%M')
            }
            create_user(user)
            send_message(sender_id, response)
        logger.info('Request success.')
    except:
        logger.info('Request failed.')
        pass

    return 'OK', 200
