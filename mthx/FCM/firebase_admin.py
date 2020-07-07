
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from firebase_admin import datetime



cred = credentials.Certificate('service-account.json')
default_app = firebase_admin.initialize_app(cred)

# This registration token comes from the client FCM SDKs.
#registration_token = 'ANDROID_CLIENT_TOKEN'
topic = 'capstone'

# See documentation on defining a message payload.
message = messaging.Message(
    android=messaging.AndroidConfig(
        ttl=datetime.timedelta(seconds=3600),
        priority='normal',
        notification=messaging.AndroidNotification(
            title='알림인데',
            body='백그라운드 자비 좀',
            icon='',
            color='#f45342',
            sound='default'
        ),
    ),
    data={
        'score': '850',
        'time': '2:45',
    },
    webpush=messaging.WebpushConfig(
        notification=messaging.WebpushNotification(
            title='웹 알림',
            body='여긴 어떨까',
            icon='',
        ),
    ),
    topic=topic
    #token=registration_token
)

# Send a message to the device corresponding to the provided
# registration token.
response = messaging.send(message)
# Response is a message ID string.



#print 'Successfully sent message:', response
