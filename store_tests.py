# -*- coding: utf-8 -*-
"""
    Store Tests
    ~~~~~~~~~~~~

    Tests the store application.
"""
import os
import store
import unittest


class StoreTestCase(unittest.TestCase):
    """Test cases for the store application."""

    def setUp(self):
        store.app.config['TESTING'] = True
        self.app = store.app.test_client()

    def test_search(self):
        response = self.app.get('/search/geek')
        assert 200 == response.status_code
        assert 0 < response.data.find('geek')

    def test_tag(self):
        response = self.app.get('/tag/geek/')
        assert 200 == response.status_code
        assert 0 < response.data.find('geek')

    def test_unknowntag(self):
        response = self.app.get('/tag/unknowntag/')
        assert 404 == response.status_code

    def test_404(self):
        response = self.app.get('/404')
        assert 404 == response.status_code


if __name__ == '__main__':
    unittest.main()
