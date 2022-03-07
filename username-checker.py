import requests

social_media_list = {
    "Facebook":"https://www.facebook.com/",
    "Twitter":"https://twitter.com/",#http code not working
    "Instagram":"https://www.instagram.com/",#http code not working
    "TikTok":"https://www.tiktok.com/@",#http code not working
    "Twitch":"https://www.twitch.tv/",#http code not working
    "Github":"https://github.com/"
}


def findUsername(username):
    for social_media in social_media_list.keys():
        link = social_media_list[social_media]+username
        response = requests.get(link)
        if response.status_code == 200:
            print(social_media + ': User exists -> ' + link)
        else:
            print(social_media + ": User doesn't exist")

if __name__ == "__main__":
    username = input("What username should the program look for ? :\n")
    findUsername(username)