##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
import os
import unittest, doctest
from zope import interface
from zope.app.testing import setup
from zope.app.testing.functional import ZCMLLayer
from zope.app.rotterdam import Rotterdam
from zojax.layoutform.interfaces import ILayoutFormLayer
from zojax.authentication.tests.install import installAuthentication


class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ skin """


zojaxRegistration = ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxRegistration', allow_teardown=True)


def setUp(test):
    site = setup.placefulSetUp(True)
    site.__name__ = u'portal'
    installAuthentication(site)
    setup.setUpTestAsModule(test, name='zojax.principal.registration.TESTS')


def tearDown(test):
    setup.placefulTearDown()
    setup.tearDownTestAsModule(test)


def test_suite():
    fields = doctest.DocFileSuite(
        '../fields.txt',
        setUp=setUp, tearDown=tearDown,
        optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)

    tool = doctest.DocTestSuite(
        'zojax.principal.registration.registration',
        setUp=setUp, tearDown=tearDown,
        optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)

    voc = doctest.DocTestSuite(
        'zojax.principal.registration.vocabulary',
        optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)

    reg = doctest.DocFileSuite(
        "registration.txt",
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)
    reg.layer = zojaxRegistration

    invitation = doctest.DocFileSuite(
        "invitation.txt",
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)
    invitation.layer = zojaxRegistration

    authorization = doctest.DocFileSuite(
        "authorization.txt",
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)
    authorization.layer = zojaxRegistration

    return unittest.TestSuite((fields, tool, voc,
                               reg, invitation, authorization))
