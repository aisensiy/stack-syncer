# -*- coding: utf-8 -*-

from .context import syncer

import unittest

class TestEventHandller(unittest.TestCase):
    def test_should_fail_get_None_when_login_failed(self):
        self.assertRaises(Exception, syncer)


if __name__ == '__main__':
    print syncer
    unittest.main()