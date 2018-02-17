import requests
from pprint import pprint

#response = requests.get("https://json.io/b/59d0f30408be13271f7df29c").json()
APP_ACCESS_TOKEN = '1395856984.a729afe.d9003eb28fcc45c2ac8e2fab6e923ffb'
BASE_URL='https://api.instagram.com/v1/'

def self_info():
    r = requests.get(("%susers/self/?access_token=%s") % (BASE_URL,APP_ACCESS_TOKEN)).json()
    print "My Info is :\n"
    if r['meta']['code'] == 200:
        # Code to print user's details
        if 'data' in r:
            print 'ID : %s' %(r['data']['id'])
            print 'Username : %s' % (r['data']['username'])
            print 'Full name : %s ' % (r['data']['full_name'])
            print 'Profile picture URL : %s' %(r['data']['profile_picture'])
            print 'Short bio : %s' %(r['data']['bio'])
            print 'Website : %s' %(r['data']['website'])
            print 'Business profile(True(Yes) or False(No) : %s' %(r['data']['is_business'])
            print 'Number of followers: %s' % (r['data']['counts']['followed_by'])
            print 'Number of people I am following: %s' % (r['data']['counts']['follows'])
            print 'Number of posts: %s' % (r['data']['counts']['media'])
        else:
            print 'User does not exist!'

    else:
        print 'Status code other than 200 received!'

def get_user_id(insta_username):

    r = requests.get((BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)).json()

    if r['meta']['code'] == 200:

        if len(r['data']):
            print "User ID : "
            print (r['data'][0]['id'])
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

    r = requests.get((BASE_URL + 'users/{user-id}/?access_token==%s') % (user_id, APP_ACCESS_TOKEN)).json()

    if r['meta']['code'] == 200:

        if 'data' in r:

            print 'Username: %s' % (r['data']['username'])
            print 'No. of followers: %s' % (r['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (r['data']['counts']['follows'])
            print 'No. of posts: %s' % (r['data']['counts']['media'])

        else:

            print 'There is no data for this user!'
    else:

        print 'Status code other than 200 received!'


def start_bot():
    show_menu = True
    while show_menu:

         print "\n*******<< Welcome to INSTABOT >>*******"
         menu_choice = input("\nWhat do you want to do? \n 1. Get your own details\n 2. Get user\'s details by the username.\n 3. Get user's info\n 0. Exit\n")

         if menu_choice == 1:
             self_info()
         elif menu_choice == 2:
             insta_username = raw_input("Enter the username of the user: ")
             get_user_id(insta_username)
         elif menu_choice == 3:
             username = raw_input("Enter the username of the user: ")
             get_user_info(username)

         elif menu_choice == 0:
             show_menu = False

         else:
            print "Invalid choice!!!"

start_bot()