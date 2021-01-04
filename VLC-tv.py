# VLCTV.py
# November 4, 2020

import requests
import vlc
import time
import os
import pickledb

tvdb = 'D:\\Dev\\Python\\VLC\\tv.db' #Change this to the location of your pickledb file
help = 'clear, list, quit, exit'

try:
    db = pickledb.load(tvdb, False)
except:
    print(f'Unable to open pickledb file at {tvdb}')
    quit()
   
Instance = vlc.Instance()
player = Instance.media_player_new()
clear_screen = os.system('cls') #Clears the screen 

def PlayChannel():
    playlists = set(['pls','m3u'])
    url = channel
    try:
        r = requests.get(url, stream=True)
        found = r.ok
    except ConnectionError as e:
        print('failed to get stream: {e}'.format(e=e))
        quit()

    if found:
        Media = Instance.media_new(url)
        Media_list = Instance.media_list_new([url])
        Media.get_mrl()
        player.set_media(Media)

        if player.play() == -1:
            print ("\nError playing Stream")

print('VLC TV Channel Player')
print('Use \'help\' to show available commands')
print('--------------------------------------------------------------\n')
while True:
    choice = input('VLCTV: ')

    if db.exists(choice):
        channel = db.get(choice)
        PlayChannel()
        clear_screen = os.system('cls') #Clears the screen
        print('Use \'quit\' to exit channel\n\n')
        continue
    else:
        if choice == 'exit':
            quit()
        if choice == 'quit':
            player.stop()
            clear_screen = os.system('cls')            
            continue
        if choice == '':
            continue
        if choice == 'clear':
            clear_screen = os.system('cls')
            continue
        if choice == 'list':
            print(db.getall())
            continue 
        if choice == 'help':
            print(help)
            continue			
        print(f'{choice} not found, try again')
        continue