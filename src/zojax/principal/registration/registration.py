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
import random
from BTrees.OOBTree import OOBTree

from zope import interface, event, component
from zope.component import subscribers, queryUtility, getUtility
from zope.lifecycleevent import ObjectCreatedEvent

from zojax.ownership.interfaces import IOwnership
from zojax.principal.invite.interfaces import IInvitations
from zojax.authentication.utils import getPrincipal
from zojax.authentication.interfaces import IPrincipalRemovingEvent
from zojax.authentication.interfaces import IPrincipalInitializedEvent
from zojax.authentication.interfaces import PrincipalInitializationFailed

import interfaces
from invitation import MembershipInvitation


class PortalRegistration(object):
    """
    >>> from zope import interface, component
    >>> from zojax.principal.registration.interfaces import IMemberRegistrationAction

    >>> class Action(object):
    ...     interface.implements(IMemberRegistrationAction)
    ...     def __init__(self, name, title, avialable):
    ...         self.name = name
    ...         self.title = title
    ...         self.avialable = avialable
    ...     def isAvailable(self):
    ...         return self.avialable

    >>> component.provideUtility(Action('a1', 'Action 1', True), name='a1')

    >>> from zojax.principal.registration.registration import PortalRegistration
    >>> tool = PortalRegistration()

    >>> tool.actions = ['a1']
    >>> for action in tool.getActions():
    ...     print action
    <zojax.principal.registration.TESTS.Action ...>

    >>> principal = object()
    >>> status = tool.registerPrincipal(principal, object())

    >>> from zope.component.eventtesting import getEvents
    >>> event = getEvents()[-1]
    >>> event
    <zojax.principal.registration.interfaces.PrincipalRegisteredEvent ...>

    >>> event.principal is principal
    True
    """

    interface.implements(interfaces.IPortalRegistration)

    def getActions(self):
        actions = []

        for name in self.actions:
            action = queryUtility(interfaces.IMemberRegistrationAction, name)
            if action is not None:
                yield action

    def registerPrincipal(self, principal, request=None):
        event.notify(interfaces.PrincipalRegisteredEvent(principal))

        if request is not None:
            for action in subscribers((self, principal, request),
                                      interfaces.IAfterRegistrationAction):
                if action.process():
                    return interfaces.STATUS_PROCESSED

        return interfaces.STATUS_CONTINUE

    def invitePerson(self, principal, name, email, subject, message):
        invitation = MembershipInvitation(name, email, subject, message)
        IOwnership(invitation).ownerId = principal
        event.notify(ObjectCreatedEvent(invitation))

        getUtility(IInvitations).storeInvitation(invitation)

        return invitation

    def listAuthorizations(self):
        return iter(self.pid_authcode.items())

    def authorizePrincipal(self, authcode):
        pid_authcode, authcode_pid = self.pid_authcode, self.authcode_pid

        if authcode in authcode_pid:
            pid = authcode_pid.get(authcode)

            if pid in pid_authcode:
                del pid_authcode[pid]

            del authcode_pid[authcode]

            return True

        return False

    def principalAuthorization(self, principal):
        principalId = principal.id

        pid_authcode, authcode_pid = self.pid_authcode, self.authcode_pid

        authcode = genAuthcode()
        pid_authcode[principalId] = authcode
        authcode_pid[authcode] = principalId
        return authcode

    def authcodeForPrincipal(self, pid):
        return self.pid_authcode.get(pid)

    def principalByAuthcode(self, authcode):
        return self.authcode_pid.get(authcode, u'')

    def removePrincipalAuthorization(self, pid):
        authcode = self.pid_authcode.get(pid)

        if pid in self.pid_authcode:
            del self.pid_authcode[pid]

        if authcode in self.authcode_pid:
            del self.authcode_pid[authcode]

    @property
    def pid_authcode(self):
        pid_authcode = self.data.get('pid_authcode')
        if pid_authcode is None:
            pid_authcode = OOBTree()
            self.data['pid_authcode'] = pid_authcode

        return pid_authcode

    @property
    def authcode_pid(self):
        authcode_pid = self.data.get('authcode_pid')
        if authcode_pid is None:
            authcode_pid = OOBTree()
            self.data['authcode_pid'] = authcode_pid

        return authcode_pid


def genAuthcode(length=32, chars='23456qwertasdfgzxcvb789yuiophjknm'):
    nchars = len(chars)

    return ''.join(
        [chars[random.randint(0,nchars-1)] for i in range(0, length)])


@component.adapter(IPrincipalInitializedEvent)
def principalInitialized(event):
    configlet = getUtility(interfaces.IPortalRegistration)
    if configlet.authcodeForPrincipal(event.principal.id) is not None:
        raise PrincipalInitializationFailed(
            interfaces._(u'Your account is not authorized.'))


@component.adapter(IPrincipalRemovingEvent)
def principalRemoved(event):
    configlet = getUtility(interfaces.IPortalRegistration)
    configlet.removePrincipalAuthorization(event.principal.id)
