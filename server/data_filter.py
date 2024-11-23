from datetime import datetime, timedelta

from collections import defaultdict

from atproto import models

from server.logger import logger
from server.database import db, Post

textFilterList = [
    "microsoft",
    "#microsoft",
    "#msazure",
    "microsoft azure",
    "#microsoftazure",
    "msft",
    "#msft",
    "satya nadella"
]


def operations_callback(ops: defaultdict) -> None:
    # Here we can filter, process, run ML classification, etc.
    # After our feed alg we can save posts into our DB
    # Also, we should process deleted posts to remove them from our DB and keep it in sync

    # for example, let's create our custom feed that will contain all posts that contains alf related text

    #myTimestamp = datetime.today() - timedelta(days=1)
    #strTimestamp = myTimestamp.strftime('%Y-%m-%d')

    posts_to_create = []
    for created_post in ops[models.ids.AppBskyFeedPost]['created']:
        author = created_post['author']
        record = created_post['record']

        # print all texts just as demo that data stream works
        post_with_images = isinstance(record.embed, models.AppBskyEmbedImages.Main)
        inlined_text = record.text.replace('\n', ' ')
        # logger.info(
        #     f'NEW POST '
        #     f'[CREATED_AT={record.created_at}]'
        #     f'[AUTHOR={author}]'
        #     f'[WITH_IMAGE={post_with_images}]'
        #     f': {inlined_text}'
        # )

        # only posts relating to keywords list in the last day
        #if any(keyword in record.text.lower() for keyword in textFilterList) and record.created_at > strTimestamp:
        if any(keyword in record.text.lower() for keyword in textFilterList):
            reply_root = reply_parent = None
            if record.reply:
                reply_root = record.reply.root.uri
                reply_parent = record.reply.parent.uri

            logger.info(
                f'NEW POST '
                f'[CREATED_AT={record.created_at}]'
                f'[AUTHOR={author}]'
                f'[WITH_IMAGE={post_with_images}]'
                f': {inlined_text}'
            )


            post_dict = {
                'uri': created_post['uri'],
                'cid': created_post['cid'],
                'reply_parent': reply_parent,
                'reply_root': reply_root,
            }
            posts_to_create.append(post_dict)

    posts_to_delete = ops[models.ids.AppBskyFeedPost]['deleted']
    if posts_to_delete:
        post_uris_to_delete = [post['uri'] for post in posts_to_delete]
        Post.delete().where(Post.uri.in_(post_uris_to_delete))
        #logger.info(f'Deleted from feed: {len(post_uris_to_delete)}')

    if posts_to_create:
        with db.atomic():
            for post_dict in posts_to_create:
                Post.create(**post_dict) # ** unpacks dict {"uri, cid, etc"}
        logger.info(f'Added to feed: {len(posts_to_create)}')
