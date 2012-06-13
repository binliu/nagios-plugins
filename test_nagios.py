'''
Created on May 30, 2012

@author: appfirst
'''
import unittest
import nagios
import sys
from StringIO import StringIO
import mock


class TestBaseAnalysis(unittest.TestCase):
    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()

    def test_result_str(self):
        r = nagios.Result('MYSQL_SLOW_QUERIES', nagios.Status.OK, '2 queries')
        self.assertEqual(str(r), 'MYSQL_SLOW_QUERIES OK: 2 queries')
        r.add_performance_data('slow_queries', 2, warn=10, crit=20)
        self.assertEqual(str(r), 'MYSQL_SLOW_QUERIES OK: 2 queries | \'slow_queries\'=2;10;20')
        r.add_performance_data('slow_queries_rate', 0.2, warn=0.5, crit=1)
        self.assertEqual(str(r), 'MYSQL_SLOW_QUERIES OK: 2 queries | \'slow_queries\'=2;10;20 \'slow_queries_rate\'=0.2;0.5;1')

    def test_verdict(self):
        ba = nagios.BasePlugin()
        request = mock.Mock()
        request.warn = 6
        request.crit = 8
        self.assertEqual(ba.verdict(2, request), nagios.Status.OK)

        request = mock.Mock()
        request.warn = 5
        request.crit = None
        self.assertEqual(ba.verdict(2, request), nagios.Status.OK)

        request = mock.Mock()
        request.warn = None
        request.crit = None
        self.assertEqual(ba.verdict(2, request), nagios.Status.OK)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_']
    unittest.main()