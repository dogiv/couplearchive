# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 09:28:05 2019

@author: ejb
"""

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
from dateutil import parser
import os
#import urllib
import urllib.request
import pickle
from bs4 import BeautifulSoup

userid = input("User ID: ")
if len(userid) < 2: print("Need user ID.")
passwd = input("Password: ")
url = 'https://app.couple.me/login'
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
win_height = 1200
chrome_options.add_argument("window-size=1200,"+str(win_height))
chromedriver_path = input("Path to chromedriver executable (use forward slashes): ")
if len(chromedriver_path) < 2:
    print("Need chromedriver path.")
driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)
driver.get(url)

username = driver.find_element_by_id('text-userid')
password = driver.find_element_by_id('text-password')

username.send_keys(userid)
password.send_keys(passwd)
password.send_keys(Keys.ENTER)

outpath = input("Path to folder where data should be stored (use forward slashes): ")
if len(outpath) < 2:
    outpath = "c:/downloads/couple"
if not os.path.exists(outpath):
    os.mkdir(outpath)

os.chdir(outpath)

do_moments = input("Download moments? (y/n): ")
max_moments = 0
if do_moments == "y" or do_moments == "Y":
    do_moments = True
    max_moments = int(input("How many moments should be downloaded (maximum)?"))
else:
    do_moments = False

do_chats = input("Download chats? (y/n): ")
if do_chats == "y" or do_chats == "Y":
    do_chats = True
else:
    do_chats = False

if do_chats:
    min_date = input("Don't record chats before about (mm/dd/yyyy) (default 01/01/2000): ")
    #max_date = input("Don't record chats after about (mm/dd/yyyy) (default 01/01/2030): ")
    max_date = ""

    if len(min_date) > 2:
        datemin = parser.parse(min_date)
    else:
        datemin = parser.parse("01/01/2000")
    if len(max_date) > 2:
        datemax = parser.parse(max_date)
    else:
        datemax = parser.parse("01/01/2030")

    num_scrolls = input("Maximum number of times to scroll up in the chat log (default 100) (I've never gotten anything above 1500 to work, the page crashes): ")
    if len(num_scrolls) < 1:
        num_scrolls = 100
    else:
        num_scrolls = int(num_scrolls) + 1


print("Downloading emoticons...",end=" ")
if not os.path.exists("emoticons"):
    os.mkdir("emoticons")
for i in range(1,41):
    urllib.request.urlretrieve("http://app.couple.me/emoticons/" + str(i) + ".png", "emoticons/" + str(i) + ".png")
print("Done.")

if not os.path.exists("files"):
    os.mkdir("files")

print("Finding images...")
time.sleep(2)

file_subs = {}

useravatar = driver.find_element_by_id("user-avatar")
partneravatar = driver.find_element_by_id("partner-avatar")
user_image_url = useravatar.get_attribute("style").split()[1][5:-2]
urllib.request.urlretrieve(user_image_url.replace("https","http"),"files/user_image.jpg")
file_subs[user_image_url] = "files/user_image.jpg"
partner_image_url = partneravatar.get_attribute("style").split()[1][5:-2]
urllib.request.urlretrieve(partner_image_url.replace("https","http"),"files/partner_image.jpg")
file_subs[partner_image_url] = "files/partner_image.jpg"
background = driver.find_element_by_id("side-menu")
background_url = background.get_attribute("style").split('background-image: url("')[1].split('"')[0]
urllib.request.urlretrieve(background_url.replace("https","http"), "files/background.jpg")
file_subs[background_url] = "files/background.jpg"
pairs = []
pairs.append(("http://app.couple.me/images/couple-logo-f.png", "files/couple-logo-f.png"))
pairs.append(("http://app.couple.me/images/couple-logo-f.png", "files/couple-logo-f.png"))
pairs.append(("http://app.couple.me/images/spinner.gif", "files/spinner.gif"))
pairs.append(("http://app.couple.me/images/location-icon.png", "files/location-icon.png"))
pairs.append(("http://app.couple.me/images/Wordmark.png", "files/Wordmark.png"))
pairs.append(("http://app.couple.me/images/messages-icon-active-hover.png", "files/messages-icon-active-hover.png"))
pairs.append(("http://app.couple.me/images/moments-icon-active-hover.png", "files/moments-icon-active-hover.png"))
pairs.append(("http://app.couple.me/images/settings-icon-active-hover.png", "files/settings-icon-active-hover.png"))
pairs.append(("http://app.couple.me/images/thinking-of-you.png", "files/thinking-of-you.png"))

for pair in pairs:
    urllib.request.urlretrieve(pair[0],pair[1])
    file_subs[pair[0][21:]] = pair[1] #outpath + "/" + pair[1]


pagesoup = BeautifulSoup(driver.page_source,"html.parser")
urllib.request.urlretrieve("http://app.couple.me/static/1.4/stylesheets/style.css", "files/style.css")
file_subs["/static/1.4/stylesheets/style.css"] = "files/style.css"
urllib.request.urlretrieve("http://fonts.googleapis.com/css?family=Open+Sans:400,300", "files/css")
file_subs["//fonts.googleapis.com/css?family=Open+Sans:400,300"] = "files/css"
urllib.request.urlretrieve("http://app.couple.me/static/1.4/javascripts/jquery.js", "files/jquery.js")
file_subs["/static/1.4/javascripts/jquery.js"] = "files/jquery.js"



if do_moments:
    print("Loading moments...",end=" ")
    time.sleep(1)
    
    if not os.path.exists("moments"):
        os.mkdir("moments")
        
    # Now load all the moments
    moment_button = driver.find_element_by_id("menu-moments-button")
    moment_button.click()
    time.sleep(1)
    
    load_more = driver.find_element_by_id("load-more-moments-button")
    while load_more.get_attribute("style") == "":
        load_more.click()
        time.sleep(0.5)
        foo = 0
        while not load_more.get_attribute("style") == "" and foo < 5:
            time.sleep(0.5)
            foo += 1
    print("Done.")
    
    print("Downloading moments...")
    # Download all the moments
    soup = BeautifulSoup(driver.page_source,"html.parser")
    html = list(soup.children)[1]
    body = list(html.children)[1]
    appwrapper = list(body.children)[4]
    viewswrapper = list(appwrapper.children)[1]
    appview = list(viewswrapper.children)[2]
    momentsview = list(viewswrapper.children)[3]
    momentswrapper = list(momentsview.children)[0]
    moments = list(momentswrapper.children)
    moment_urls = []
    extensions = []
    nmoment = 0
    # It really shouldn't be necessary to click on the ones that are just images,
    # the URL should be available already. But sometimes it's not, I guess?
    for moment in moments:
        if nmoment > max_moments: break
        style = moment['style']
        if "background-image: url(" in style:
            moment_urls.append(style.split("background-image: url(")[1][1:-3])
            extension = moment_urls[-1].split("?")[0][-4:]
            extensions.append(extension)
        else: # movie or audio note
            nonpic = driver.find_element_by_id(moment['id'])
            nonpic.click()
#            print("Moment",nmoment,"non-picture")
            time.sleep(1)
            full = driver.find_element_by_id("full-moment-content")
            parts = full.find_elements_by_xpath(".//*")
            nonpic = BeautifulSoup(parts[0].get_attribute("outerHTML"),"html.parser")
            url = str(nonpic).split("src=")[1].split('"')[1]
            moment_urls.append(url)
            extension = moment_urls[-1].split("?")[0][-4:]
            extensions.append(extension)
            close = driver.find_element_by_id("full-moment-close-button")
            close.click()
        try:
            urllib.request.urlretrieve(moment_urls[-1].replace("&amp;","&").replace("https","http"),"moments/moment" + str(nmoment) + extension)
            print("Saved moment",nmoment,extension)
            file_subs[moment_urls[-1]] = "moments/moment" + str(nmoment) + extension
        except:
            print("Failed to save moment",nmoment,extension)
        nmoment += 1
    pickle.dump(moment_urls, open("moments/moment_urls.p","wb"))
    print("Done.")
else:
    if os.path.exists("moments/moment_urls.p"):
        moment_urls = pickle.load(open("moments/moment_urls.p","rb"))
        for j,url in enumerate(moment_urls):
            extension = url.split("?")[0][-4:]
            file_subs[url] = "moments/moment" + str(j) + extension

# Find all attributes of a WebElement:
#for k,el in enumerate(new): 
#    print(k, driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', el), el.text)


# Download chat history

if do_chats:
    messages_button = driver.find_element_by_id("menu-messages-button")
    messages_button.click()
    
    print("Finding message history...")
    time.sleep(3)
    
    chats = driver.find_element_by_id('chat-view')
    
    # Scroll all the way to the beginning, or at least pretty far
    last_scroll_height = 0
    scroll_height = driver.execute_script("return $(\"#chat-view\")[0].scrollHeight")
    n_scrolls = 0
    sleep_time = 0.3
    date = datetime.datetime.now()
    print("Scrolling up...", end=" ")
    while scroll_height > last_scroll_height and n_scrolls < num_scrolls-1 and date >= datemin:
        try:
            driver.execute_script("$(\"#chat-view\").animate({scrollTop:\"0px\"})")
        except:
            break
        last_scroll_height = scroll_height
        time.sleep(sleep_time)
        scroll_height = driver.execute_script("return $(\"#chat-view\")[0].scrollHeight")
        while scroll_height <= last_scroll_height and sleep_time < 100:
            sleep_time += 0.2
            time.sleep(sleep_time)
            scroll_height = driver.execute_script("return $(\"#chat-view\")[0].scrollHeight")
        n_scrolls += 1
        htm = chats.get_attribute("outerHTML")
        date_ind = htm.index("message-timestamp-text") + 24
        datestr = htm[date_ind:date_ind+12].split("<")[0]
        try:
            date = parser.parse(datestr)
        except:
            pass
        if datestr in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
            date = date - datetime.timedelta(7)
        if datestr == "Yesterday":
            date = datetime.datetime.now() - datetime.timedelta(1)
        if datestr == "Just now":
            date = datetime.datetime.now()
        if n_scrolls % 50 == 0:
            print("Scrolled up", n_scrolls, "times, now at ", datestr)
        if n_scrolls % 50 == 0 and date <= datemax:
            pickle.dump(htm, open("chats_" + str(n_scrolls) + ".p","wb"))
    
    print("Done.")
    print("Saving chat history...",end=" ")

    # Read and save the html when done scrolling up
    try:
        htm = chats.get_attribute("outerHTML")
    except:
        pass
    date_ind = htm.index("message-timestamp-text") + 24
    datestr = htm[date_ind:date_ind+12].split("<")[0]
    date = parser.parse(datestr)
    pickle.dump(htm, open("chats_" + str(n_scrolls) + ".p","wb"))
#    try:
#        all_htm = driver.page_source
#        with open("messages.html","w") as htmfile:
#            htmfile.write(BeautifulSoup(all_htm,"html.parser").prettify().encode('cp850','replace').decode('cp850'))
#    except:
#        pass
    print("Done.")

    
    chatsoup = BeautifulSoup(htm,"html.parser")
    messages = list(list(chatsoup.children)[0].children)
    
    # Break long chat lists into segments... may not be necessary actually
#    segment_length = 10 #10,000 chats each (10 for testing)
#    numsegs = len(messages) / segment_length
#    numsegs = int(round(numsegs + 0.5,0))
    
    # Modify HTML for offline viewing
    print("Modifying HTML to work offline...")
    
    pagehtml = pagesoup.html
    head = pagehtml.head
    for child in head.children:
        strchild = str(child)
        if strchild.startswith("<script"):
            try:
                if child["src"] in file_subs:
                    child["src"] = file_subs[child["src"]]
                else: 
                    child.extract()
            except: # script doesn't have a "src" field
                pass
        try:
            if child["href"] in file_subs:
                child["href"] = file_subs[child["href"]]
        except:
            pass
    print("Disabled login scripts...")
                    
    body = pagehtml.body
    appwrapper = list(body.children)[4]
#    list(body.children)[3].extract() # remove the "login" section
#    sidemenu = list(appwrapper.children)[0]
    appview = list(list(appwrapper.children)[1].children)[2]
    chatview = list(appview.children)[0]
    chatview.replaceWith(chatsoup)
    print("Inserted chat history...")

    strsoup = pagesoup.prettify()
    for key,val in file_subs.items():
        strsoup = strsoup.replace(key, val)
        key2 = key.replace("&","&amp;")
        strsoup = strsoup.replace(key2, val)

    print("Replaced URLs with file paths...")

    with open("couple.html","w") as outfile:
        outfile.write(strsoup.encode('cp850','replace').decode('cp850'))
    
    print("Saved couple.html for viewing.")

print("Done. You may close this window.")


    
