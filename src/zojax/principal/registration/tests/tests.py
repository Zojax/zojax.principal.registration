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



import os
import unittest, doctest
from zope import interface, component, event
from zope.component import getUtility
from zope.app.testing import setup
from zope.app.testing.functional import ZCMLLayer
from zope.app.rotterdam import Rotterdam
from zope.session import session
from zope.app.component.hooks import getSite, setSite
from zope.app.testing import functional
from zope.app.security.interfaces import IAuthentication
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectCreatedEvent

from zojax.layoutform.interfaces import ILayoutFormLayer

from zojax.authentication import principalinfo
from zojax.authentication.authentication import PluggableAuthentication
from zojax.authentication.interfaces import ICredentialsPluginFactory
from zojax.authentication.credentials import factory as defaultCreds


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


def FunctionalDocFileSuite(*paths, **kw):
    layer = zojaxRegistration

    globs = kw.setdefault('globs', {})
    globs['http'] = functional.HTTPCaller()
    globs['getRootFolder'] = functional.getRootFolder
    globs['sync'] = functional.sync

    kw['package'] = doctest._normalize_module(kw.get('package'))

    kwsetUp = kw.get('setUp')
    def setUp(test):
        functional.FunctionalTestSetup().setUp()

    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')
    def tearDown(test):
        setSite(None)
        functional.FunctionalTestSetup().tearDown()

    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old|doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = layer
    return suite


def test_suite():

    authorization = FunctionalDocFileSuite("authorization.txt")

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

    return unittest.TestSuite((fields, tool, voc,
                               reg, invitation, authorization))
