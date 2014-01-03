from authorization import get_access_token

from instagram.client import InstagramAPI


if __name__ == '__main__':
    access_token = get_access_token()
    instagram_api = InstagramAPI(access_token=access_token)
    media_feed, _ = instagram_api.user_media_feed()
    print media_feed
