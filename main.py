# -*- coding: utf-8 -*-

import googleapiclient.errors
import googleapiclient.discovery
import google_auth_oauthlib.flow
import os
import time
from decouple import config
from email_sender import EmailSender

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

email_sender = EmailSender()

api_service_name = "youtube"
api_version = "v3"


def main():
    SHOULD_RUN = True
    playlist_itemCount = 0
    while SHOULD_RUN:
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=config('API_KEY', cast=str))

        # Get the requested playlist's information
        request = youtube.playlists().list(
            part="contentDetails",
            id=config('YT_PLAYLIST_ID', cast=str)
        )

        response = request.execute()
        # Get the current playlist items count from the response dict.
        response_itemCount = response['items'][0]['contentDetails']['itemCount']
        # Update the count if itemCount is larger than the current playlist_itemCount
        if response_itemCount > playlist_itemCount:
            playlist_itemCount = response_itemCount

            # Once the value has been updated, send an email to notify that a new video is uploaded. 
            email_sender.send_email()
        time.sleep(config('DELAY_BETWEEN_CHECKS', cast=int))


if __name__ == "__main__":
    main()
