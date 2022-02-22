# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import logging
from scrapy.mail import MailSender

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter



class MailNotificationPipeline:

    def _get_already_seen_posts(self):
        try: 
            with open("seen_posts.txt") as f:
                seen_posts = f.readlines()
                seen_posts = [id.rstrip() for id in seen_posts]
        except FileNotFoundError:
            return []

        
        return seen_posts
    
    def _add_post_to_seen(self, id):
        with open("seen_posts.txt", "a+") as f:
            f.write("\n" + id)


    def _already_seen(self, post):
        return post["id"] in self._get_already_seen_posts()

    def _match(self, post):
        return (
            (post["rooms"] >= 3.0) 
        and (post["area"] == "stadt")
        and (post["city"] == "zuerich")
        and (post["price"] <= 3000)
        and (post["limited"] != "Y")
        and (post["zip_code"] in [8001, 8002, 8003, 8004, 8005, 8006, 8037, 8032, 8008])
        and not self._already_seen(post)
        )

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Inform via mail if post matches fitler criteria
        if self._match(adapter):
            mailer = MailSender.from_settings(spider.settings)
            mailer.send(
                to=spider.settings.getlist("MAIL_TO"), 
                subject="New Posting on Ron Orp", 
                body=adapter["url"],)
            self._add_post_to_seen(adapter["id"])


        return item
