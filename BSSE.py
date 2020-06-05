#! python 3.8.2
# EDBIV - 2020
# BSSE: Beat Saber Song Extractor, aka Bessie

import zipfile, os, re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

print('Bessie wants to know where to look for songs.')
print('Ex.: C:\\Desktop\\PhatBeats')
# Where you download the .zip files from bsaber.com to:
songsPath = Path(filedialog.askdirectory(initialdir="/", title="Downloaded Song Zips"))
print('Pulling songs from ' + str(songsPath) + '\n')
# songsPath = Path(r'D:\Beats'), my own place (for the time being)

print('Bessie wants to know where to install your new songs.')
print('Ex.: D:\\SteamLibrary\\steamapps\\common\\Beat Saber\\Beat Saber_Data\\CustomLevels')
# Where your custom levels for beat saber are installed:
installPath = Path(filedialog.askdirectory(initialdir="/", title="Where to Install Songs"))
print('Installing songs to ' + str(installPath) + '\n')
# installPath = Path(r'D:\SteamLibrary\steamapps\common\Beat Saber\Beat Saber_Data\CustomLevels'), my own place

# Regular expression to find name of each song installed using text from "info.dat" in .zip file
# "\s*" is included because very rarely there is no space following the colon
infoRegex = re.compile(r'"_songName":\s*'r'"(.*?)"')

# Operate on each file in the .zip file download folder
for filename in os.listdir(songsPath):
    # Only operate on zip files, or zipfile.Zipfile will break
    if (songsPath / filename).suffix == '.zip':
        beatZip = zipfile.ZipFile(songsPath / filename)
    else:
        # Skip file if not zipped
        continue

    # Check if zip is actually a bsaber song
    try:
        # "str(beatZip.read('info.dat'))" opens text from level info file
        songName = infoRegex.search(str(beatZip.read('info.dat'))).group(1)
        # A space at the end of a song name makes stuff break, this should fix that
        if list(songName)[-1] == ' ':
            songName = songName[:-1]
        # This undoes some escape character activity when a ' appears
        # which would usually cause the song name to split and open a subdirectory
        if '\\\'' in songName:
            songName = songName.replace('\\', '')

    except (KeyError, AttributeError):
        print('The file \"' + filename + '\" either isn\'t a song or '
              'you\'ve found something that Bessie can\'t handle yet.')
        continue

    # Save extracted files in folder with name of song
    beatZip.extractall(installPath / songName)
    print(songName + " added to Beat Saber Library")

    # Close current zip
    beatZip.close()
