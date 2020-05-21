import zipfile, os, re
from pathlib import Path

# Where you download the .zip files from bsaber.com to:
p = Path(r'D:\Beats')
# Where your custom levels for beat saber are installed:
beatSaberLevels = Path(r'D:\SteamLibrary\steamapps\common\Beat Saber\Beat Saber_Data\CustomLevels')

# Regular expression to find name of each song installed using text from "info.dat" in .zip file
infoRegex = re.compile(r'"_songName": "(.*?)"')

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
    beatZip.extractall(beatSaberLevels / songName)
    # Confirm song added to library
    print(songName + " added to Beat Saber Library")
    beatZip.close()
