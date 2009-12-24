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

from zope import interface
from zope.component import getUtility, getMultiAdapter
from zope.app.security.interfaces import IAuthentication, PrincipalLookupError

from zojax.wizard.step import WizardStep
from zojax.mail.interfaces import IMailAddress
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.principal.registration.interfaces import \
    _, IMailAuthorizationTemplate


class Authorizations(WizardStep):

    label = _('Authorizations')

    def update(self):
        request = self.request
        context = self.context

        auth = getUtility(IAuthentication)

        if 'form.button.authorize' in request:
            for authcode in request.get('authcodes', ()):
                context.authorizePrincipal(authcode)

            IStatusMessage(request).add(
                _('Principals have been authorized.'))

        elif 'form.button.resend' in request:
            for authcode in request.get('authcodes', ()):
                try:
                    principal = auth.getPrincipal(
                        context.principalByAuthcode(authcode))
                except PrincipalLookupError:
                    continue

                email = IMailAddress(principal, None)
                if email is not None:
                    template = getMultiAdapter(
                        (principal, authcode, request),
                        IMailAuthorizationTemplate)
                    template.send(
                        (formataddr((principal.title, email.address)),))

            IStatusMessage(request).add(
                _('Authorization information has been sent.'))

        principals = []
        for pid, authcode in context.listAuthorizations():
            try:
                principals.append(
                    {'pid': pid,
                     'title': auth.getPrincipal(pid).title,
                     'authcode': authcode})
            except:
                principals.append(
                    {'pid': pid,
                     'title': pid,
                     'authcode': authcode})

        self.principals = principals

        super(Authorizations, self).update()
