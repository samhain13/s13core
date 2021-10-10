from urllib.error import URLError

from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.test import TestCase

from s13core.content_management.models import Article

from .models import APIKey
from .models import SocMedFeed
from .models import SocMedProcessor


def basic_setup():
    '''Helper. Sets up a basic 3 object arrangement for testing.'''

    api_key = APIKey(
        key='12345',
        label='Social Media Key'
    )

    if APIKey.objects.count() == 0:
        api_key.save()

    sm_proc = SocMedProcessor(
        label='Sociam Media Processor',
        uri='http://localhost:8000/?api_key={api_key}&account_id={account_id}',
        code='print(\'Hello, world.\')',
        notes='Just a test processor.'
    )

    if SocMedProcessor.objects.count() == 0:
        sm_proc.save()

    sm_feed = SocMedFeed(
        api_key=api_key,
        processor=sm_proc,
        account_id='username0987',
        max_results=0
    )

    if SocMedFeed.objects.count() == 0:
        sm_feed.save()

    return api_key, sm_proc, sm_feed


class SocMedCollectorTests(TestCase):
    def setUp(self):
        if User.objects.count() < 1:
            user = User.objects.create_user(
                'admin', 'admin@example.com', 'admin-password!')

    def test_apikey_label_unique(self):
        label = 'Social Media Key'
        api_key0 = APIKey(
            key='123456789A',
            label=label
        )
        api_key0.save()
        label = 'social media key'
        api_key1 = APIKey(
            key='123456789B',
            label=label
        )
        self.assertRaises(FieldError, api_key1.save)

    def test_apikey_str_method(self):
        label = 'Social Media Key'
        api_key = APIKey(
            key='123456789A',
            label=label
        )
        self.assertEqual(str(api_key), 'APIKey: {}'.format(label))

    def test_socmed_feed_uri(self):
        api_key, sm_proc, sm_feed = basic_setup()
        self.assertEqual(
            sm_proc.uri.format(
                api_key=api_key.key, account_id=sm_feed.account_id),
            sm_feed.uri
        )

    def test_socmed_feed_get_response(self):
        api_key, sm_proc, sm_feed = basic_setup()
        # Assuming localhost:8000 is not accepting connections.
        self.assertRaises(URLError, sm_feed.get_response)
        # Not sure how we can test HTTPError locally without opening an HTTP
        # server, so we'll just skip testing for that.

    def test_socmed_feed_process_response(self):
        api_key, sm_proc, sm_feed = basic_setup()
        # Since we cannot test the actual retrieval of a resource from a
        # social media site, we'll just use a JSON that is similar to what
        # Instagram returns.
        sm_feed.response = INSTAGRAM_SAMPLE_JSON_SNIPPET
        sm_proc.code = INSTAGRAM_SAMPLE_PROCESSOR
        sm_feed.process_response()
        # See INSTAGRAM_SAMPLE_* strings for values used.
        post = Article.objects.get(
            slug='instagram-1083349939758384497-2167128920')
        self.assertEqual(post.keywords, 'instagram, test post')
        self.assertEqual(
            post.body,
            '<p>This tricycle looks like a prop from Thunderdome.</p>'
        )
        # Clean up.
        post.delete()


# Here be long strings:
INSTAGRAM_SAMPLE_PROCESSOR = '''
from datetime import datetime
from s13core.content_management.models import Article

for d in self.response_json['data']:
    slug = 'instagram-{}'.format(d['id'].replace('_', '-'))

    # We don't want double posts so we have to check for double slugs.
    # We also want a caption because that's were we get some of our data.
    if not Article.objects.filter(slug=slug).first() and d['caption']:
        dt = datetime.fromtimestamp(int(d['created_time']))
        title = 'Instagram post from {}'.format(dt.strftime('%d %B %Y'))

        a = Article()
        a.slug = slug
        a.title = title
        a.description = title
        a.keywords = ', '.join(['instagram'] + d['tags'])
        a.body = '<p>{}</p>'.format(d['caption']['text'])
        a.body = a.body.replace('\\n', '\\n<br />')
        a.body = a.body.replace('\\n<br />\\n<br />', '</p>\\n\\n<p>')
        a.save()

    # We can also download any of the images from Instagram and save it as
    # a FileAsset and make a relationship between it and the Article.
'''

INSTAGRAM_SAMPLE_JSON_SNIPPET = '''{
    "meta": {"code": 200},
    "data": [
        {
            "created_time": "1443365398",
            "user_has_liked": false,
            "attribution": null,
            "link": "https://instagram.com/p/8I1QfGvUVx",
            "caption": {
                "created_time": "1443365398",
                "text": "This tricycle looks like a prop from Thunderdome.",
                "id": "1083350629989827809",
                "from": {
                    "id": "2167128920",
                    "profile_picture": "https://igcdn-photos-c-a.akamaihd.net/hphotos-ak-xaf1/t51.2885-19/s150x150/11428365_939021869498234_1590396807_a.jpg",
                    "username": "abcruz2310",
                    "full_name": "Arielle Cruz"
                }
            },
            "images": {
                "thumbnail": {
                    "height": 150,
                    "width": 150,
                    "url": "https://scontent.cdninstagram.com/hphotos-xaf1/t51.2885-15/s150x150/e35/11906095_1687210724843377_233205085_n.jpg"
                },
                "standard_resolution": {
                    "height": 640,
                    "width": 640,
                    "url": "https://scontent.cdninstagram.com/hphotos-xaf1/t51.2885-15/s640x640/sh0.08/e35/11906095_1687210724843377_233205085_n.jpg"
                },
                "low_resolution": {
                    "height": 320,
                    "width": 320,
                    "url": "https://scontent.cdninstagram.com/hphotos-xaf1/t51.2885-15/s320x320/e35/11906095_1687210724843377_233205085_n.jpg"
                }
            },
            "id": "1083349939758384497_2167128920",
            "users_in_photo": [],
            "filter": "Normal",
            "type": "image",
            "user": {
                "id": "2167128920",
                "profile_picture": "https://igcdn-photos-c-a.akamaihd.net/hphotos-ak-xaf1/t51.2885-19/s150x150/11428365_939021869498234_1590396807_a.jpg",
                "username": "abcruz2310",
                "full_name": "Arielle Cruz"
            },
            "tags": ["test post"],
            "likes": {
                "count": 3,
                "data": [
                    {
                        "id": "375787057",
                        "profile_picture": "https://igcdn-photos-f-a.akamaihd.net/hphotos-ak-xpa1/t51.2885-19/10725176_573121836150189_934875017_a.jpg",
                        "username": "donnaongkingco",
                        "full_name": "Shelly Ongkingco"
                    },
                    {
                        "id": "420496998",
                        "profile_picture": "https://igcdn-photos-f-a.akamaihd.net/hphotos-ak-xfp1/t51.2885-19/10864669_624421657686085_2108994325_a.jpg",
                        "username": "drinkinton",
                        "full_name": ""
                    },
                    {
                        "id": "1548933062",
                        "profile_picture":
                        "https://igcdn-photos-h-a.akamaihd.net/hphotos-ak-xfa1/t51.2885-19/11386493_1615699115380327_410937989_a.jpg",
                        "username": "tapiocaaaaaaa",
                        "full_name": "Taffy Salazar"
                    }
                ]
            },
            "comments": {
                "count": 0,
                "data": []
            },
            "location": {
                "name": "Parola, Cainta",
                "id": 794993399,
                "longitude": 121.10160507,
                "latitude": 14.62110331
            }
        }
    ],
    "pagination": {
        "next_url": "https://api.instagram.com/v1/users/2167128920/media/recent?access_token=2167128920.8d37ab1.a458c8dae8be4bb5895b694e824d8611&count=20&max_id=1068818471334003993_2167128920",
        "next_max_id": "1068818471334003993_2167128920"
    }
}'''
