# Move Game Save Files to this docker image

### Step 1: Start the Docker Container once and mount the volumes
Start your nitrox docker container once to create the necessary folders.<br>
Go to the folder where your config is mounted and open the "saves" folder. You should see a folder with `My World`.

### Step 2: Locate the Existing Save Folder
Nitrox server saves on Windows are usually in: `C:\Users\<YourUser>\AppData\Roaming\Nitrox\saves\<YourServerName>`<br>
If you don't know how to get to the Nitrox folder, you can open the nitrox app go to your server settings and click on "Open world Folder".
in the folder you will find multiple files and folders, Those are your save files.

### Step 3: Copy the Save Files
Copy all files and folders from the existing save folder to the "My World" folder in your mounted docker volume.
Start the nitrox container again, and your server should now load the copied save files.
