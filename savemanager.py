import datetime, json, subprocess, click

class SaveManager:

    def __init__(self, rcloneDirectory, minecraftDirectory):
        self.rcloneDirectory = rcloneDirectory
        self.minecraftDirectory = minecraftDirectory
    
    def execute(self, command): # Executes a command
        try:
            return subprocess.run(command.split(" "), stdout=subprocess.PIPE).stdout.decode('utf-8')
        
        except:
            raise ValueError("You don't have the command '{0}' or the command failed.".format(command))
    
    def getFiles(self): # Returns a JSON containing too much information about your files *on the cloud*
        return json.loads(self.execute("rclone lsjson {0}".format(self.rcloneDirectory)))

    def getTimestamp(self): # Searches through that long JSON to find a timestamp, getting the last uploaded time
        return list( filter( lambda x:x[ "Name" ]=="timestamp", self.getFiles() ) )[ 0 ][ "ModTime" ]
    
    def getLocalTimestamp(self): # Gets the timestamp stored on your machine
        localtimestamp = self.execute("cat {0}/saves/timestamp".format(self.minecraftDirectory))
        if len(localtimestamp) == 0: # If the file doesn't exist or something
            return "Jan 01 1970 12:00:00AM " # Haha unix epoch
        else:
            return localtimestamp
    
    def getTimestamps(self): # Retrieves and formats all timestamps
        localtimestamp = datetime.datetime.strptime(self.getLocalTimestamp(), "%b %d %Y %I:%M:%S%p ")
        return {
            "local": datetime.datetime.utcfromtimestamp(localtimestamp.timestamp()),
            "cloud": datetime.datetime.strptime(self.getTimestamp(), "%Y-%m-%dT%H:%M:%SZ"),
        }

    def download(self): # Creates a timestamp, backs up the stuff, then updates the timestamp. All in Bash! And in a painful one-liner!
        self.execute('''date +"%b %d %Y %I:%M:%S%p" > {0}/saves/timestamp; rclone sync {0}/saves {1} -v; date +"%b %d %Y %I:%M:%S%p" > {0}/timestamp"'''.format(self.minecraftDirectory, self.rcloneDirectory))
        self.finishMessage()

    def upload(self): # Restores saves
        self.execute("rclone sync {1} {0}/saves -v".format(self.minecraftDirectory, self.rcloneDirectory))
        self.finishMessage()

    def finishMessage(self):
        print("--> Done! Thanks for using this program!")

    def wizard(self): # Automatically downloads/uploades saves
        timestamps = self.getTimestamps()
        if timestamps["local"] < timestamps["cloud"]: # If true, time to restore. If false, time to back up.
            if click.confirm('The program determined you need to download saves from the cloud. Do you want to continue?', default=True):
                self.upload()
            else:
                print("Did not download saves.")
        else:
            if click.confirm('The program determined you need to push saves to the cloud. Do you want to continue?', default=True):
                self.download()
            else:
                print("Did not upload saves.")
