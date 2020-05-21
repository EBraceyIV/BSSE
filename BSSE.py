#! python 3.8.2
# EDBIV - 2020
# BSSE: Beat Saber Song Extractor, aka Bessie

import zipfile, os, re
from pathlib import Path

print('Bessie wants to know where to look for songs.')
print('Ex.: C:/Desktop/PhatBeats')
# Where you download the .zip files from bsaber.com to:
songsPath = input('Enter directory: ')
p = Path(songsPath)
#p = Path(r'D:\Beats'), my own place (for the time being)


print('Bessie wants to know where to install your new songs.')
print('Ex.: D:\SteamLibrary\steamapps\common\Beat Saber\Beat Saber_Data\CustomLevels')
# Where your custom levels for beat saber are installed:
installPath = input('Enter directory: ')
beatSaberLevels = Path(installPath)
#beatSaberLevels = Path(r'D:\SteamLibrary\steamapps\common\Beat Saber\Beat Saber_Data\CustomLevels'), my own place
# Regular expression to find name of each song installed using text from "info.dat" in .zip file
infoRegex = re.compile(r'"_songName": "(.*?)"')

try:
    # Operate on each file in the .zip file download folder
    for filename in os.listdir(p):
        beatZip = zipfile.ZipFile(p / filename)
        # Check if zip is actually a bsaber song
        try:
            # "str(beatZip.read('info.dat'))" opens text from level info file
            songName = infoRegex.search(str(beatZip.read('info.dat'))).group(1)
        except KeyError:
            print('That\'s not a song!')
            continue
        # Save extracted files in folder with name of song
        try:
            beatZip.extractall(beatSaberLevels / songName)
        except FileNotFoundError:
            print('The path you entered, "' + installPath + '" does not seem to be valid. Please check and try again.')
        else:
            # Confirm song added to library
            print(songName + " added to Beat Saber Library")
            beatZip.close()
except FileNotFoundError:
    print('The path you entered, "' + songsPath + '" does not seem to be valid. Please check and try again.')