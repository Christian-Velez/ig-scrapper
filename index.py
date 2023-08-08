

from IgDownloader import IgDownloader

## Your account
username = "my_username"
password = "my_password"
downloader = IgDownloader(username, password)

username_to_download = ""
downloader.downloadPosts(username_to_download, amount=20)
downloader.downloadStories(username_to_download)

