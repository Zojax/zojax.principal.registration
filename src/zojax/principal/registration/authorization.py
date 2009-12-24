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
from email.Utils import formataddr

from zope import interface, component
from zope.component import getMultiAdapter
from zope.security.interfaces import IPrincipal
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL
from zope.publisher.interfaces.browser import IBrowserRequest

from zojax.mail.interfaces import IMailAddress
from zojax.statusmessage.interfaces import IStatusMessage

from interfaces import _
from interfaces import IPortalRegistration, IAfterRegistrationAction
from interfaces import IMailAuthorizationAware, IMailAuthorizationTemplate


class EmailAuthorization(object):
    interface.implements(IAfterRegistrationAction)
    component.adapts(IPortalRegistration, IPrincipal, IBrowserRequest)

    def __init__(self, registration, principal, request):
        self.registration = registration
        self.principal = principal
        self.request = request

    def process(self):
        if not self.registration.authorization or \
                not IMailAuthorizationAware.providedBy(self.principal):
            return False

        authcode = self.registration.principalAuthorization(self.principal)

        email = IMailAddress(self.principal, None)
        if email is None:
            return False

        request = self.request
        template = getMultiAdapter(
            (self.principal, authcode, request), IMailAuthorizationTemplate)
        template.send((formataddr((self.principal.title, email.address)),))

        request.response.redirect(
            '%s/mailconfirm.html'%absoluteURL(getSite(), request))

        return True
