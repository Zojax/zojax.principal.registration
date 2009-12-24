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
from zope import interface
from zojax.principal.registration.interfaces import IMemberRegistrationAction


class TestingAction1(object):
    interface.implements(IMemberRegistrationAction)

    name = 'testing-action1'
    title = u'Testing registration 1'
    description = u'First registration method.'

    def isAvailable(self):
        return True


class TestingAction2(object):
    interface.implements(IMemberRegistrationAction)

    name = 'testing-action2'
    title = u'Testing registration 2'
    description = u'Second registration method.'

    def isAvailable(self):
        return True
