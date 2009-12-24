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
from zope import interface, component
from zope.component import getUtility
from zope.viewlet.viewlet import ViewletBase
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zojax.personal.bar.personalbar import PersonalBarTag
from zojax.principal.registration.interfaces import _, IPortalRegistration


class JoinMenuItem(ViewletBase):

    weight = 999999

    def isAvailable(self):
        if not self.manager.isAnonymous:
            return False

        configlet = getUtility(IPortalRegistration)

        try:
            if configlet.getActions().next():
                return True
        except:
            pass

        return False


@component.adapter(IPortalRegistration, IObjectModifiedEvent)
def portalRegistrationChanged(configlet, ev):
    PersonalBarTag.update()
