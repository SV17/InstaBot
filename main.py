import requests
from pprint import pprint

#response = requests.get("https://json.io/b/59d0f30408be13271f7df29c").json()
APP_ACCESS_TOKEN = '1395856984.a729afe.d9003eb28fcc45c2ac8e2fab6e923ffb'
BASE_URL='https://api.instagram.com/v1/'

def self_info():
    r = requests.get(("%susers/self/?access_token=%s") % (BASE_URL,APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        # Code to print user's details
        if 'data' in r:
            print 'Username: %s' % (r['data']['username'])
            print 'Full name: %s ' % (r['data']['full_name'])
            print 'Number of followers: %s' % (r['data']['counts']['followed_by'])
            print 'Number of people you are following: %s' % (r['data']['counts']['follows'])
            print 'Number of posts: %s' % (r['data']['counts']['media'])
        else:
            print 'User does not exist!'

    else:
        print 'Status code other than 200 received!'

def get_user_id(insta_username):

    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print "Get request url: %s" % (request_url)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:

        if len(user_info['data']):
            print user_info['data'][0]['id']
        else:
            return None
    else:
        print 'status code other than 200.'
        exit()

def get_user_info(insta_username):

    user_id = get_user_id(insta_username)

    if user_id == None:

        print 'User does not exist!'
        exit()

    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:

        if 'data' in user_info:

            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])

        else:

            print 'There is no data for this user!'
    else:

        print 'Status code other than 200 received!'


def start_bot():
    show_menu = True
    while show_menu:

         print "*******<< Welcome to INSTABOT >>*******"
         menu_choice = input("\nWhat do you want to do? \n 1. Get your own details\n 2. Get user\'s details by the username.\n 3. Get user's info\n 0. Exit\n")

         if menu_choice == 1:
             self_info()
         elif menu_choice == 2:
             username = raw_input("Enter the username of the user: ")
             get_user_id(username)
         elif menu_choice == 3:
             username = raw_input("Enter the username of the user: ")
             get_user_info(username)

         elif menu_choice == 0:
             show_menu = False

         else:
            print "Invalid choice!!!"

start_bot()