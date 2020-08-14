# Insta-Bot
This is an instagram bot written with selenium. It would follow 15 followers per hour. and you can also specify a maximum number so if it wont follow more than that number (it's not accurate tho)<br>
It follows from the followers of the pages you tell and unfollows from the followed ones (not your own followings). And everytime it follows or unfollows someone it puts the log in a file called results.txt

# How-To-Use
Open the info.txt file and put your username and password inside that (put them in their specified places)<br>
Open target_pages.txt and put the id of pages you want (without @), each in one line (like the specified places). You can put as much pages as you want.

Note: If it didn't work you have to add the chromedriver.exe to path. Search for it in the internet.<br>
Note2: It runs forever. If you don't want this to happen you can change the code appropriately or simply close the running file.