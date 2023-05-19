# vlctv-gui-3.0b.py
# May 19, 2023

import PySimpleGUI as sg
import requests
import vlc
import time
import os
import pickledb

version = 'VLC-TV 3.0b'
tvdb = 'D:\\Dev\\Python\\VLC\\tv.db'  # Change this to the location of your pickledb file
tvlist = ''
selected = False
previousvalue = 25

# Load pickledb with our channels
try:
    db = pickledb.load(tvdb, False)
except:
    print(f'Unable to open pickledb file at {tvdb}')
    quit()

# Put db values into a list
db.lcreate(tvlist)
for value in db.getall():
    db.ladd(tvlist, value)
allChannels = db.lgetall(tvlist)


# Function to play channel when called
def PlayChannel():
    playlists = set(['pls', 'm3u'])
    url = channel
    try:
        r = requests.get(url, stream=True)
        found = r.ok
    except ConnectionError as e:
        print('failed to get stream: {e}'.format(e=e))
        quit()

    if found:
        Media = Instance.media_new(url)
        # Media_list = Instance.media_list_new([url])
        Media.get_mrl()
        player.set_media(Media)

        if player.play() == -1:
            print("\nError playing Stream")


# Create new base instance of VLC
Instance = vlc.Instance()
player = Instance.media_player_new()


# Create layout for the GUI
layout = [
    [sg.Text('Search:'), sg.Input(key='Search', enable_events=True)],
    [sg.Listbox(list(allChannels), size=(30, 20), key='ChannelList', select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                enable_events=True, visible=True), sg.Text('Volume', key='Volume', size=(6, 1)),
     sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=50, enable_events=True,
               key='VolumeSlider'),
     sg.Checkbox('Mute', key='Mute', enable_events=True)],
    [sg.Button(' Select '), sg.Button(' Stop '), sg.Button(' Add '), sg.Button(' Exit ')],
    [sg.Text('Name:', key='ChannelTitleText', size=(5, 1), visible=False),
     sg.InputText('', key='ChannelTitle', size=(30, 1), visible=False),
     sg.Text('URL:', key='ChannelURLText', visible=False), sg.InputText('', key='ChannelURL', size=(30, 1), visible=False)],
    [sg.Button(' Add Channel ', visible=False), sg.Button(' Cancel ', visible=False)]
]

# Start the GUI
window = sg.Window(version, layout=layout, margins=(10, 10), return_keyboard_events=True, keep_on_top=True, finalize=True)

while True:
    event, values = window.read()

    if event in (' Exit ', None):
        break

    if event == ' Select ':
        choice = values['ChannelList'][0]
        channel = db.get(choice)
        PlayChannel()

    if event == ' Stop ':
        player.stop()

    if event == ' Add ':
        window['ChannelTitleText'].update(visible=True)
        window['ChannelTitle'].update(visible=True)
        window['ChannelURLText'].update(visible=True)
        window['ChannelURL'].update(visible=True)
        window[' Add Channel '].update(visible=True)
        window[' Cancel '].update(visible=True)

    if event == ' Add Channel ':
        channelname = ''
        channelurl = ''
        channelname = values['ChannelTitle']
        channelurl = values['ChannelURL']
        if channelname and channelurl:
            db.set(channelname, channelurl)
            db.dump()
            window['ChannelTitle'].update(value='')
            window['ChannelURL'].update(value='')

    if event == ' Cancel ':
        channelname = ''
        channelurl = ''
        window['ChannelTitleText'].update(visible=False)
        window['ChannelTitle'].update(visible=False)
        window['ChannelURLText'].update(visible=False)
        window['ChannelURL'].update(visible=False)
        window[' Add Channel '].update(visible=False)
        window[' Cancel '].update(visible=False)

    if event == 'Search':
        search_query = values['Search']
        if search_query:
            filtered_channels = [channel for channel in allChannels if search_query.lower() in channel.lower()]
            window['ChannelList'].update(values=filtered_channels)
        else:
            window['ChannelList'].update(values=allChannels)

    volumelevel = int(values['VolumeSlider'])
    player.audio_set_volume(volumelevel)

    if event == 'Mute':
        currentlevel = player.audio_get_volume()
        if currentlevel == 1:
            window['VolumeSlider'].update(value=previousvalue)
            player.audio_set_volume(previousvalue)
        if currentlevel > 1:
            previousvalue = currentlevel
            window['VolumeSlider'].update(value=1)
            player.audio_set_volume(1)

window.close()
