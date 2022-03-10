import requests

social_media_list = {
    "Facebook":"https://www.facebook.com/",
    "Instagram":"https://www.instagram.com/",
    "TikTok":"https://www.tiktok.com/@",
    "Twitch":"https://www.twitch.tv/",
    "Github":"https://github.com/",
}


def findUsername(username):
    session = requests.session()
    user_agent = ('Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 '
                        'Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) '
                        'Version/4.0 Mobile Safari/534.30')
    session.headers.update({'User-Agent': user_agent})

    for social_media in social_media_list.keys():
        link = social_media_list[social_media]+username
        response = session.get(link)
        if response.status_code == 200:
            print(social_media + ': User exists -> ' + link)
        else:
            print(social_media + ": User doesn't exist")

if __name__ == "__main__":
    username = input("What username should the program look for ? :\n")
    findUsername(username)