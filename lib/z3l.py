# -*- coding: utf-8 -*-

"""Python wrapper for the Zazzle Product RSS API.

http://asset.zcache.com/assets/graphics/z2/mk/sell/RSSGuide1.03.pdf
http://www.zazzle.com/sell/developers/rss
"""

import feedparser
import urllib

class Z3L:
    params = {
        'qs': '', # query string for searching text fields
        'cg': '', # Zazzle gallery product line
        'pt': '', # Zazzle product type string "zazzle_shirt" or "zazzle_mug"
        'st': '', # sort type; value can be "popularity" or "date_created"
        'sp': '', # sort period used for "popularity" sorts, values: 0 = all time, 1=today, 7=this week, 30=this month
        'pg': 1, # page number specifying the result page on which the feed starts
        'ps': 10, # page size the number of products per page
        'ft': 'rss', # feed type, value can be either "rss" or "gb" for RSS or Google Base
        'isz': '', # image size: "tiny", "medium", "large", "huge"
        'bg': '', # background color for images as string in the form RRGGBB
        'opensearch': 1, # puts the opensearch extension into Google Base feeds
        'at': 238355915198956003 # Your associate referral id
    }

    store_id = None
    store_url = 'http://feed.zazzle.com/%s/rss'


    def __init__(self, store_id):
        self.store_id = store_id
        self.store_url = self.store_url % store_id


    def get_products(self, params):
        self.params.update(params)

        # filter empty params, encode remaining ones and request feed
        feed = feedparser.parse('%s?%s' % (self.store_url, urllib.urlencode(
            filter(lambda x: True if x[1] else False, self.params.items()))))

        if 'status' in feed and 200 == feed['status'] and 'feed' in feed and 'entries' in feed:

            f = feed.feed

            result = Result()
            result.page = int(self.params['pg'])
            result.limit = int(self.params['ps'])
            if 'opensearch_totalresults' in f:
                result.total = int(f['opensearch_totalresults'])

            for e in feed.entries:
                i = Item()
                i.link = e.link
                i.title = e.title
                i.description = e.media_description
                i.imageurl = e.media_thumbnail[0]['url']
                i.created = e.published
                i.tags = e.media_keywords.split(', ')
                if i.tags: result.tags += i.tags
                result.items.append(i)

            result.tags = sorted(set(result.tags))
            return result

        raise Exception('No data fetched.')


class Result(object):
    def __init__(self):
        self.items = []
        self.tags = []

class Item(object):
    def __init__(self):
        self.tags = []
