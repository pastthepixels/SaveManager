Save Manager
============
# Dependencies
- `rclone`, set up (run `rclone config` after installing)
- Module `click` from pip
- Python 3 + Some knowledge of Python

# Description
This program works by creating a timestamp at your save location which tracks when it was last saved. Whenever you run the wizard, it checks the time difference with the timestamp on the cloud and the timestamp on your computer and determines if you need to download or upload saves. With user confirmation, the wizard then automatically uploads/downloads game files. I've recently noticed, though, that it doesn't just work for Minecraft (which I developed it for)! This can theoretically sync any folder on your computer with the cloud.  
Note that it is a program that I originally devloped the "backend" some time ago but has had a the `SaveManager` class hacked together in an hour. Expect some errors.

# Sample Usage
```
import SaveManager from savemanager
savemanager = SaveManager("[rclone server]:[folder]", "[absolute file path you wish to sync]")
savemanager.wizard()
```

# Where's my Minecraft folder?
Flatpak (Linux): `/home/$USER/.var/app/com.mojang.Minecraft/data/minecraft/`
Linux Default: `/home/$USER/.minecraft`
Windows: `%AppData%\.minecraft`
MacOS: `/home/$USER/Library/Application Support/minecraft`

# Roadmap for the future
        - GUI counterpart, maybe in GTK 4?
        - Automatic syncing, likely with the GUI program.
