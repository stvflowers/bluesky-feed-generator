#!/usr/bin/env python3
# YOU MUST INSTALL ATPROTO SDK
# pip3 install atproto

from atproto import Client, models
import os
from dotenv import load_dotenv

def main():

    load_dotenv()

    HANDLE: str = os.getenv('HANDLE')
    PASSWORD: str = os.getenv('PASSWORD')
    HOSTNAME: str = os.getenv('HOSTNAME')
    RECORD_NAME: str = os.getenv('RECORD_NAME')
    DISPLAY_NAME: str = os.getenv('DISPLAY_NAME')
    DESCRIPTION: str = os.getenv('DESCRIPTION')
    AVATAR_PATH: str = os.getenv('AVATAR_PATH')
    SERVICE_DID: str = os.getenv('SERVICE_DID')

    client = Client()
    client.login(HANDLE, PASSWORD)

    feed_did = SERVICE_DID
    if not feed_did:
        feed_did = f'did:web:{HOSTNAME}'

    avatar_blob = None
    if AVATAR_PATH:
        with open(AVATAR_PATH, 'rb') as f:
            avatar_data = f.read()
            avatar_blob = client.upload_blob(avatar_data).blob


    response = client.com.atproto.repo.delete_record(models.ComAtprotoRepoDeleteRecord.Data(
        repo=client.me.did,
        collection=models.ids.AppBskyFeedGenerator,
        rkey=RECORD_NAME,
        record=models.AppBskyFeedGenerator.Record(
            did=feed_did,
            display_name=DISPLAY_NAME,
            description=DESCRIPTION,
            avatar=avatar_blob,
            created_at=client.get_current_time_iso(),
        )
    ))

    print('Successfully un-published!')


if __name__ == '__main__':
    main()
