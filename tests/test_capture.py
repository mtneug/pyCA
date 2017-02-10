# -*- coding: utf-8 -*-

'''
Tests for basic capturing
'''

import os
import shutil
import tempfile
import unittest

from pyca import capture, config, db, utils


class TestPycaCapture(unittest.TestCase):

    dbfile = None
    cadir = None
    event = None

    def setUp(self):
        _, self.dbfile = tempfile.mkstemp()
        self.cadir = tempfile.mkdtemp()
        config.config()['agent']['database'] = 'sqlite:///' + self.dbfile
        config.config()['capture']['command'] = 'touch {{dir}}/{{name}}.mp4'
        config.config()['capture']['directory'] = self.cadir
        config.config()['service-ingest'] = ['']
        config.config()['service-capture.admin'] = ['']

        # Mock event

        db.init()
        self.event = db.BaseEvent()
        self.event.uid = '123123'
        self.event.start = utils.timestamp()
        self.event.end = self.event.start + 1
        data = [{'data': u'äüÄÜß',
                 'fmttype': 'application/xml',
                 'x-apple-filename': 'episode.xml'},
                {'data': u'äüÄÜß',
                 'fmttype': 'application/xml',
                 'x-apple-filename': 'series.xml'},
                {'data': u'event.title=äüÄÜß\n' +
                         u'org.opencastproject.workflow.config.x=123\n' +
                         u'org.opencastproject.workflow.definition=fast',
                 'fmttype': 'application/text',
                 'x-apple-filename': 'org.opencastproject.capture.agent' +
                                     '.properties'}]
        self.event.set_data({'attach': data})

    def tearDown(self):
        os.remove(self.dbfile)
        shutil.rmtree(self.cadir)

    def test_start_capture(self):
        # Mock some methods
        capture.http_request = lambda x, y=False: b'xxx'
        capture.start_capture(self.event)


if __name__ == '__main__':
    unittest.main()