# Importing requests
import requests

# Importing termcolor for color
from termcolor import colored

# Takes the URL from user and coverts it into json format
response = requests.get('https://api.jsonbin.io/b/59d0f30408be13271f7df29c').json()
# Gets the access token in response
APP_ACCESS_TOKEN = response['access_token']
# Base URL remains same so storing it in a variable
BASE_URL='https://api.instagram.com/v1/'

# Method to display self info
def self_info():
    r = requests.get(("%susers/self/?access_token=%s") % (BASE_URL,APP_ACCESS_TOKEN)).json()
    print colored("\nMy Info is : ","magenta")
    if r['meta']['code'] == 200:                # HTTP 200 means transmission is OK
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

# Method to get the user id
def get_user_id(insta_username):
    info = requests.get((BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)).json()
    
    if info['meta']['code'] == 200:  # HTTP 200 means transmission is OK
        if len(info['data']):               # Checking length using len() function
            return info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'      # If transmission is not OK


# Method to get the information about the user
def get_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    else:
        info = requests.get((BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)).json()
        print colored("\nUser Info is :","magenta")
        if info['meta']['code'] == 200:
            if len(info['data']):
                print 'ID : %s' % (info['data']['id'])
                print 'Username : %s' % (info['data']['username'])
                print 'Full name : %s ' % (info['data']['full_name'])
                print 'Profile picture URL : %s' % (info['data']['profile_picture'])
                print 'Short bio : %s' % (info['data']['bio'])
                print 'Website : %s' % (info['data']['website'])
                print 'Business profile(True(Yes) or False(No) : %s' % (info['data']['is_business'])
                print 'Number of followers: %s' % (info['data']['counts']['followed_by'])
                print 'Number of people you are following: %s' % (info['data']['counts']['follows'])
                print 'Number of posts: %s' % (info['data']['counts']['media'])
            else:
                print 'There is no data for this user!'
        else:
            print 'Status code other than 200 received!'

print colored("\n*******<< Welcome to INSTABOT >>*******","magenta")


# Starting application

def start_bot():
    # Initializing show_menu with True value
    show_menu = True
    while show_menu:
         # Asking the user's choice
         menu_choice = input(colored("\nWhat do you want to do? \n 1. Get your own details\n 2. Get user\'s id by the username\n 3. Get user's information\n 0. Exit\n","blue"))

         if menu_choice == 1:
             self_info()           # Calling method
         elif menu_choice == 2:
             # Asking the user name
             insta_username = raw_input("Enter the username of the user: ")
             user_id = get_user_id(insta_username)          # Calling get_user_id method
             print(colored("User ID is : %s ","magenta")) % (user_id)
         elif menu_choice == 3:
             # Asking the user name
             username = raw_input("Enter the username of the user: ")
             get_info(username)                       # Calling the get_info method
         elif menu_choice ==0:
             show_menu = False

         else:
            # If user chooses something other than the menu choices
            print "Invalid choice!!!"

# Calling the start_bot() method to start the application
start_bot()