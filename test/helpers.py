

def os_get_side_effect(arg):
    values = {
        'BOT_ID': 'bot_id',
        'GIPHY_KEY': 'giphy_key',
        'GROUPME_TOKEN': 'groupme_token',
        'REDDIT_CLIENT_ID': 'reddit_client_id',
        'REDDIT_CLIENT_SECRET': 'reddit_client_secret',
        'REDDIT_PASSWORD': 'reddit_password',
        'REDDIT_USERNAME': 'reddit_username',
        'USER_AGENT': 'user_agent'
    }

    try:
        return values[arg]
    except Exception:
        return ''
