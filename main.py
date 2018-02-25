# Importing requests
import requests

# Importing urllib to download posts
import urllib

from textblob import TextBlob

# For sentimental analysis
from textblob.sentiments import NaiveBayesAnalyzer

# Importing termcolor for colour
from termcolor import colored

# Takes the URL from user and coverts it into json format
response = requests.get('https://api.jsonbin.io/b/59d0f30408be13271f7df29c').json()
# Gets the access token in response
APP_ACCESS_TOKEN = response['access_token']
# Common for all the Instagram API endpoints
BASE_URL = 'https://api.instagram.com/v1/'


# Method to display info of owner
def self_info():
    r = requests.get("%susers/self/?access_token=%s" % (BASE_URL, APP_ACCESS_TOKEN)).json()
    print colored("\nMy Info is : ", "magenta")
    if r['meta']['code'] == 200:  # HTTP 200 means transmission is OK
        # Code to print user's details
        if 'data' in r:
            print 'ID : %s' % (r['data']['id'])
            print 'Username : %s' % (r['data']['username'])
            print 'Full name : %s ' % (r['data']['full_name'])
            print 'Profile picture URL : %s' % (r['data']['profile_picture'])
            print 'Short bio : %s' % (r['data']['bio'])
            print 'Website : %s' % (r['data']['website'])
            print 'Business profile(True(if Yes) or False(if No) : %s' % (r['data']['is_business'])
            print 'Number of followers: %s' % (r['data']['counts']['followed_by'])
            print 'Number of people I am following: %s' % (r['data']['counts']['follows'])
            print 'Number of posts: %s' % (r['data']['counts']['media'])
        else:
            # If user doesn't exist
            print colored("User does not exist!", "red")

    else:
        # Transmission is not okay
        print colored("Status code other than 200 received!", "red")


# Method to get the recent post of owner
def owner_recent_post():
    user_post = requests.get('%susers/self/media/recent/?access_token=%s' % (BASE_URL, APP_ACCESS_TOKEN)).json()
    if user_post['meta']['code'] == 200:  # HTTP 200 means transmission is OK
        if len(user_post['data']):
            r = user_post['data'][0]['images']['standard_resolution']['url']  # Image in standard resolution
            print (colored("\nThe URL of recent post is : ", "magenta"))  # Displaying URL of pic
            print (r)
            if user_post['data'][0]['caption']:  # if caption exists
                caption = user_post['data'][0]['caption']['text']
                print (colored("Caption of recent post is : ", "magenta"))  # Displaying the caption of the post
                print caption
            else:
                print (colored("There isn't any caption for this post!", "red"))
        else:
            print (colored("There are no posts!", "red"))
    else:
        print (colored("Status code other than 200 received!", "red"))

# Method to download owner's recent post
def download_owner_recent_post():
        user_post = requests.get('%susers/self/media/recent/?access_token=%s' % (BASE_URL, APP_ACCESS_TOKEN)).json()
        if user_post['meta']['code'] == 200:  # HTTP 200 means transmission is OK
            if len(user_post['data']):
                r = user_post['data'][0]['images']['standard_resolution']['url']  # Image in standard resolution
                if user_post['data'][0]['type'] == "image":  # Checking whether the post is an image or not
                    image_name = user_post['data'][0]['id'] + '.jpeg'
                    image_url = user_post['data'][0]['images']['standard_resolution']['url']
                    urllib.urlretrieve(image_url, image_name)  # Downloading post using urlretrieve method
                    print (colored("Your image has been downloaded!", "magenta", attrs=["dark", "bold"]))
                elif user_post['data'][0]['type'] == "video":
                    video_name = user_post['data'][0]['id'] + '.mp4'
                    video_url = user_post['data'][0]['videos']['standard_resolution']['url']
                    urllib.urlretrieve(video_url, video_name)  # Downloading the post if its a video
                    print (colored("Your video has been downloaded!", "magenta", attrs=["dark", "bold"]))
                else:
                    print (colored("The post is neither an image nor a video.", "red"))  # If the post is not an image
            else:
                print (colored("There are no posts!", "red"))
        else:
            print (colored("Status code other than 200 received!", "red"))


# Method to get the user id
def get_user_id(user_name):
    r = requests.get("%susers/search?q=%s&access_token=%s" % (BASE_URL, user_name, APP_ACCESS_TOKEN)).json()

    if r['meta']['code'] == 200:  # HTTP 200 means transmission is OK
        if len(r['data']):  # Checking length using len() function
            return r['data'][0]['id']
        else:
            return None
    else:
        print (colored("Status code other than 200 received!", "red"))  # If transmission is not OK


# Method to get the information about the user
def get_user_info(user_name):
    user_id = get_user_id(user_name)
    if user_id is None:
        print (colored("User does not exist!", "red"))
        exit()
    else:
        info = requests.get("%susers/%s?access_token=%s" % (BASE_URL, user_id, APP_ACCESS_TOKEN)).json()
        print colored("\nUser Info is :", "magenta")
        if info['meta']['code'] == 200:                  # HTTP 200 means transmission is OK
            if len(info['data']):
                # Displaying the info of other user
                print 'ID : %s' % (info['data']['id'])
                print 'Username : %s' % (info['data']['username'])
                print 'Full name : %s ' % (info['data']['full_name'])
                print 'Profile picture URL : %s' % (info['data']['profile_picture'])
                print 'Short bio : %s' % (info['data']['bio'])
                print 'Website : %s' % (info['data']['website'])
                print 'Business profile(True(if Yes) or False(if No) : %s' % (info['data']['is_business'])
                print 'Number of followers: %s' % (info['data']['counts']['followed_by'])
                print 'Number of people you are following: %s' % (info['data']['counts']['follows'])
                print 'Number of posts: %s' % (info['data']['counts']['media'])
            else:
                print (colored("There is no data of this user!", "red"))
        else:
            print (colored("Status code other than 200 received!", "red"))


# Method to get recent post of a user
def get_user_post(u_name):
    user_id = get_user_id(u_name)
    if user_id is None:
        print (colored("User does not exist!", "red"))
        exit()
    else:
        post = requests.get('%susers/%s/media/recent/?access_token=%s' % (BASE_URL, user_id, APP_ACCESS_TOKEN)).json()
        if post['meta']['code'] == 200:                 # HTTP 200 means transmission is OK
            if len(post['data']):
                r = post['data'][0]['images']['standard_resolution']['url']
                print (colored("\nThe URL of post is : ", "magenta"))
                print (r)
                if post['data'][0]['caption']:
                    caption = post['data'][0]['caption']['text']
                    print (colored("Caption of post is : ", "magenta"))
                    print caption
                else:
                    print (colored("There isn't any caption of this post!", "red"))
            else:
                print (colored("There are no posts for this user!", "red"))
        else:
            print (colored("Status code other than 200 received!", "red"))


# Method to download recent post of a user
def download_user_post(u_name):
    user_id = get_user_id(u_name)
    if user_id is None:
        print (colored("User does not exist!", "red"))
        exit()
    else:
        post = requests.get('%susers/%s/media/recent/?access_token=%s' % (BASE_URL, user_id, APP_ACCESS_TOKEN)).json()
        if post['meta']['code'] == 200:                            # HTTP 200 means transmission is OK
            # Checking whether some post exist or not
            if len(post['data']) > 0:
                if post['data'][0]['type'] == "image":  # Checking if the post is an image or not
                    image_name = post['data'][0]['id'] + '.jpeg'
                    image_url = post['data'][0]['images']['standard_resolution']['url']
                    urllib.urlretrieve(image_url, image_name)  # Downloading the post if its an image
                    print (colored("Your image has been downloaded!", "blue", attrs=["dark", "bold"]))
                elif post['data'][0]['type'] == "video":
                    video_name = post['data'][0]['id'] + '.mp4'
                    video_url = post['data'][0]['videos']['standard_resolution']['url']
                    urllib.urlretrieve(video_url, video_name)  # Downloading the post if its a video
                    print (colored("Your video has been downloaded!", "blue", attrs=["dark", "bold"]))
                else:
                    print(colored("The post is neither an image nor a video", "red"))
            else:
                print (colored("Post does not exist!", "red"))
        else:
            print (colored("Status code other than 200 received!", "red"))


# Method to get the id of post
def get_media_id(username):
    user_id = get_user_id(username)
    if user_id is None:
        print (colored("User does not exist!", "red"))
        exit()
    else:
        post = requests.get('%susers/%s/media/recent/?access_token=%s' % (BASE_URL, user_id, APP_ACCESS_TOKEN)).json()
        if post['meta']['code'] == 200:                                      # HTTP 200 means transmission is OK
            # Checking whether some post exist or not
            if len(post['data']) > 0:
                return post['data'][0]['id']  # Returning the media id
            else:
                print (colored("Post does not exist!", "red"))
        else:
            print (colored("Status code other than 200 received!", "red"))


# Method to like a post
def like_a_post(insta_username):
    media_id = get_media_id(insta_username)
    payload = {"access_token": APP_ACCESS_TOKEN}
    url = '%smedia/%s/likes' % (BASE_URL, media_id)
    post_a_like = requests.post(url, payload).json()
    if post_a_like['meta']['code'] == 200:                                 # HTTP 200 means transmission is OK
        print colored("Like was successful!","magenta")
    else:
        print colored("Your like was unsuccessful. Try again!","red")


# Method to post a comment
def post_a_comment(insta_username):
    media_id = get_media_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    url = '%smedia/%s/comments' % (BASE_URL, media_id)
    make_comment = requests.post(url, payload).json()
    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


# Method to get the list of comments
def get_comments_list(insta_username):
    media_id = get_media_id(insta_username)
    request_url = ('%smedia/%s/comments/?access_token=%s' % (BASE_URL, media_id, APP_ACCESS_TOKEN))
    comment = requests.get(request_url).json()
    if comment['meta']['code'] == 200:
        if len(comment['data']):
            number_of_comments = 0
            print "The list of comments on the post are : \n"
            for index in range(0, len(comment['data'])):
                c_text = comment['data'][index]['text']
                print (c_text)
                number_of_comments = number_of_comments + 1
            print "Number of comments on the post are : " + str(number_of_comments)
        else:
            print (colored("There are no comments on the post!", "red"))
    else:
        print (colored("Status code other than 200 received!", "red"))


# Method to delete negative comments from a post
def delete_negative_comments(insta_username):
    media_id = get_media_id(insta_username)
    request_url = ('%smedia/%s/comments/?access_token=%s' % (BASE_URL, media_id, APP_ACCESS_TOKEN))
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code'] == 200:                                 # HTTP 200 means transmission is OK
        if len(comment_info['data']):                                       # Checking whether any comment exits or not
            for index in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][index]['id']
                comment_text = comment_info['data'][index]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if ((blob.sentiment.p_neg) > (blob.sentiment.p_pos)):
                    print "Negative comment : %s" % (comment_text)            # Displaying the negative comment
                    r = requests.delete('%smedia/%s/comments/%s?access_token=%s' % (BASE_URL, media_id, comment_id, APP_ACCESS_TOKEN)).json()
                    if r['meta']['code'] == 200:
                        print "Comment deleted successfully !"
                    else:
                        print "Unable to delete comment !"
                else:
                    print "Positive comment : %s" %(comment_text)               # Displaying the positive comment
        else:
            print (colored("There are no comments on the post!", "red"))
    else:
        print (colored("Status code other than 200 received!", "red"))


# Start greeting
print colored("\nHELLO !", "blue")
print colored("*******<< Welcome to INSTABOT >>*******", "magenta", attrs=["dark", "bold"])


# Starting application
def start_bot():
    # Initializing show_menu with True value
    show_menu = True
    while show_menu:
        # Asking the user's choice
        print (colored("\nWhat do you want to do? \n 1. Get your own details\n 2. Get your own recent post\n 3. Download owner's recent post\n 4. Get user's information\n 5. Get user's recent post\n 6. Download user's recent post\n 7. Like a post\n 8. Comment on a post\n 9. Get list of comments on a post\n 10. Delete negative comments\n 0. Exit\n","green"))
        menu_choice = input(colored("Select your choice : ", "blue", attrs=["dark", "bold"]))
        if menu_choice == 1:
            self_info()  # Calling self_info() method to display info of owner
        elif menu_choice == 2:
            owner_recent_post()  # Calling owner_recent_post() method to get the recent post of owner
        elif menu_choice ==3:
            download_owner_recent_post()  # Calling download_owner_recent_post() method to download the recent post of owner
        elif menu_choice == 4:
            # Asking the user name
            insta_username = raw_input("\nEnter the username of the user: ")
            get_user_info(insta_username)  # Calling the get_user_info() method to get other user's info
        elif menu_choice == 5:
            insta_username = raw_input("\nEnter the username of the user: ")
            get_user_post(insta_username)  # Calling the get_user_post() method to get other user's post
        elif menu_choice == 6:
            insta_username = raw_input("\nEnter the username of the user: ")
            download_user_post(insta_username)  # Calling the download_user_post() method to download other user's post
        elif menu_choice == 7:
            insta_username = raw_input("\nEnter the username of the user: ")
            like_a_post(insta_username)  # Calling the like_post() method to like other user's post
        elif menu_choice == 8:
            insta_username = raw_input("\nEnter the username of the user: ")
            post_a_comment(insta_username)  # Calling the post_a_comment() method to post a comment
        elif menu_choice == 9:
            insta_username = raw_input("\nEnter the username of the user: ")
            get_comments_list(insta_username)   # Calling the get_comments_list() method to display all the comments from a post
        elif menu_choice == 10:
            insta_username = raw_input("\nEnter the username of the user: ")
            delete_negative_comments(insta_username)  # Calling the delete_negative_comments() method to delete negative comments from a post
        elif menu_choice == 0:
            show_menu = False                         # For exitting from menu
        else:
            # If user chooses something other than the menu choices
            print (colored("Invalid choice!!!", "red", attrs=["dark", "bold"]))


# Calling the start_bot() method to start the application
start_bot()

