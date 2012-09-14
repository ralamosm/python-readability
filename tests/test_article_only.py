import os
import unittest

from readability import Document
import lxml.html


SAMPLES = os.path.join(os.path.dirname(__file__), 'samples')


def load_sample(filename):
    """Helper to get the content out of the sample files"""
    return open(os.path.join(SAMPLES, filename)).read()


class TestArticleOnly(unittest.TestCase):
    """The option to not get back a full html doc should work

    Given a full html document, the call can request just divs of processed
    content. In this way the developer can then wrap the article however they
    want in their own view or application.

    """

    def test_si_sample(self):
        """Using the si sample, load article with only opening body element"""
        sample = load_sample('si-game.sample.html')
        doc = Document(
            sample,
            url='http://sportsillustrated.cnn.com/baseball/mlb/gameflash/2012/04/16/40630_preview.html')
        res = doc.summary()
        self.assertEqual('<html><body><div><div class', res[0:27])

    def test_si_sample_html_partial(self):
        """Using the si sample, make sure we can get the article alone."""
        sample = load_sample('si-game.sample.html')
        doc = Document(sample, url='http://sportsillustrated.cnn.com/baseball/mlb/gameflash/2012/04/16/40630_preview.html')
        res = doc.summary(html_partial=True)
        self.assertEqual('<div><div class="', res[0:17])

    def test_nyt_sample_html_iframe(self):
        """Using the nyt sample, make sure the summary holds an <iframe> element (youtube video)"""
        sample = load_sample('nyt-article-video.sample.html')
        doc = Document(sample, url='http://nytimes.com/')
        res = doc.summary()
        self.assertTrue('<iframe ' in res)

    def test_lxml_obj_result(self):
        """Feed Document with an lxml obj instead of an html string. Expect an lxml response"""
        utf8_parser = lxml.html.HTMLParser(encoding='utf-8')
        sample = lxml.html.document_fromstring(load_sample('nyt-article-video.sample.html'), parser=utf8_parser)
        doc = Document(sample, url='http://nytimes.com/')
        res = doc.summary()
        self.assertFalse(isinstance(res, basestring))
