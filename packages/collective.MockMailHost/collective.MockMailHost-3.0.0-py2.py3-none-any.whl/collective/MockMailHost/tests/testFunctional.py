# -*- coding: utf-8 -*-
from collective.MockMailHost.testing import \
    COLLECTIVE_MOCKMAILHOST_FUNCTIONAL_TESTING
from collective.MockMailHost.testing import optionflags
from plone.testing import layered
from plone.app.testing import applyProfile

import doctest
import unittest


doctests = (
    'SendEmail.txt',
)


def setUp(self):
    # this is a workaround, because the profile loaded in the layer is
    # not present in the tests
    portal = self.globs['layer']['portal']
    applyProfile(portal, 'collective.MockMailHost:default')


def test_suite():
    suite = unittest.TestSuite()
    tests = [
        layered(
            doctest.DocFileSuite(
                'tests/{0}'.format(test_file),
                package='collective.MockMailHost',
                optionflags=optionflags,
                setUp=setUp,
            ),
            layer=COLLECTIVE_MOCKMAILHOST_FUNCTIONAL_TESTING,
        )
        for test_file in doctests
    ]
    suite.addTests(tests)
    return suite
