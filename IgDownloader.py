from instagrapi import Client
from instagrapi.exceptions import (
   RateLimitError
)
import os
import sys


def handle_exception(client, e):
   if isinstance(e, RateLimitError):
      print("Limit reached. Please wait a few minutes before you try again.")

class IgDownloader():
   def __init__(self, username, password): 
      print("Login account: %s" % username)
      self.cl = Client()
      self.cl.handle_exception = handle_exception
      self.cl.login(username, password)

      print("Login successful")

   def _createFolder(self, username, clasification):
      userFolder = os.path.exists(username)

      if(not userFolder):
         os.mkdir(username)

      subFolderPath = username + "/" + clasification
      subFolder = os.path.exists(subFolderPath)

      if(not subFolder):
         os.mkdir(subFolderPath)

      return subFolderPath

   def downloadPosts(self, username, amount = 0):
      folder = self._createFolder(username, clasification="posts")

      print("Fetching posts...")
      user_id = self.cl.user_id_from_username(username)
      medias = self.cl.user_medias(user_id, amount)
      sys.stdout.write("\033[F") # Cursor up one line

      for index, media in enumerate(medias):
         print("Downloading posts... [" + str(index) + "/" + str(len(medias)) + "]")
         sys.stdout.write("\033[F") # Cursor up one line
         pk = media.pk

         # Photo
         if(media.media_type == 1):
            self.cl.photo_download(pk, folder)

         #Video
         if(media.media_type == 2 and media.product_type == "feed"):
            self.cl.video_download(pk, folder)

         #IGTV
         if(media.media_type == 2 and media.product_type == "igtv"):
            self.cl.igtv_download(pk, folder)

         if(media.media_type == 2 and media.product_type =="clips"):
            self.cl.clip_download(pk, folder)

         if(media.media_type == 8):
            self.cl.album_download(pk, folder)

      sys.stdout.write("\033[F") # Cursor up one line
      print("✅ Posts download complete. Folder: " + folder + "\n\n\n")
      

   def downloadStories(self, username):
      folder = self._createFolder(username, clasification="stories")

      print("Getting stories...")
      user_id = self.cl.user_id_from_username(username)
      stories = self.cl.user_stories(user_id)

      for index, story in enumerate(stories):
         print("Downloading stories... [" + str(index) + "/" + str(len(stories)) + "]")
         sys.stdout.write("\033[F") # Cursor up one line
         pk = story.pk
         self.cl.story_download(pk)

      print("✅ Stories download complete. Folder: " + folder)

      