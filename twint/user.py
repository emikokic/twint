import datetime
import logging as logme


class user:
    type = "user"

    def __init__(self):
        pass


User_formats = {
    'join_date': '%Y-%m-%d',
    'join_time': '%H:%M:%S %Z'
}


# ur object must be a json from the endpoint https://api.twitter.com/graphql
def User(ur):
    logme.debug(__name__ + ':User')
    if 'data' not in ur or 'user' not in ur['data'] or 'legacy' not in ur['data']['user']:
        msg = 'malformed json! cannot be parsed to get user data'
        if 'errors' in ur:
            msg = ur['errors'][0]['message']
        logme.fatal(msg)
        return

    _user_data = ur['data']['user']
    _user_data_legacy = _user_data['legacy']
    _usr = user()

    _usr.id = _user_data.get('rest_id', '')
    _usr.name = _user_data_legacy.get('name', '')
    _usr.username = _user_data_legacy.get('screen_name', '')
    _usr.bio = _user_data_legacy.get('description', '')
    _usr.location = _user_data_legacy.get('location', '')
    _usr.url = _user_data_legacy.get('url', '')

    # parsing date to user-friendly format
    _dt = _user_data_legacy.get('created_at', None)
    if _dt:
        _dt = datetime.datetime.strptime(_dt, '%a %b %d %H:%M:%S %z %Y')
        # date is of the format year,
        _usr.join_date = _dt.strftime(User_formats['join_date'])
        _usr.join_time = _dt.strftime(User_formats['join_time'])

    # :type `int`
    _usr.tweets = int(_user_data_legacy.get('statuses_count', 0))
    _usr.following = int(_user_data_legacy.get('friends_count', 0))
    _usr.followers = int(_user_data_legacy.get('followers_count', 0))
    _usr.likes = int(_user_data_legacy.get('favourites_count', 0))
    _usr.media_count = int(_user_data_legacy.get('media_count', 0))

    _usr.is_private = _user_data_legacy.get('protected', False)
    _usr.is_verified = _user_data_legacy.get('verified', False)
    _usr.avatar = _user_data_legacy.get('profile_image_url_https', '')
    _usr.background_image = _user_data_legacy.get('profile_banner_url', '')
    # TODO : future implementation
    # legacy_extended_profile is also available in some cases which can be used to get DOB of user
    return _usr
