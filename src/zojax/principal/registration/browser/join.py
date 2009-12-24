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
from zope.location import LocationProxy
from zope.publisher.interfaces import NotFound
from zope.component import getUtility, queryUtility, queryMultiAdapter

from zojax.principal.registration.interfaces import _
from zojax.principal.registration.interfaces import IPortalRegistration
from zojax.principal.registration.interfaces import IMemberRegistrationAction

from interfaces import IRegistrationWorkspace


class RegistrationForm(object):
    interface.implements(IRegistrationWorkspace)

    title = _('Portal registration')

    def __init__(self, context, request):
        self.context = context
        self.request = request

        self.configlet = getUtility(IPortalRegistration)

    def publishTraverse(self, request, name):
        if name in self.configlet.actions:
            action = queryUtility(IMemberRegistrationAction, name)
            if action is not None:
                return LocationProxy(action, self, name)

        view = queryMultiAdapter((self, request), name=name)
        if view is not None:
            return view

        raise NotFound(self, name, request)

    def browserDefault(self, request):
        actions = self.configlet.actions
        if len(actions) > 1:
            return self, ('select.html',)
        elif len(actions) == 1:
            return self, actions

        raise NotFound(self, '', request)
