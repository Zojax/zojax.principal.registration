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

from zope import interface, schema, event
from zope.component import getUtility, getMultiAdapter, queryMultiAdapter
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL

from zojax.mail.interfaces import IMailAddress
from zojax.layoutform import button, Fields, PageletForm
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.authentication.utils import getPrincipalByLogin

from zojax.principal.registration.interfaces import _, IPortalRegistration
from zojax.principal.registration.interfaces import IMailAuthorizationTemplate


class IAuthForm(interface.Interface):

    code = schema.TextLine(
        title = _('Authorization code'),
        description = _('Enter authorization code.'),
        required = True)


class AuthorizePrincipal(PageletForm):

    authorized = False
    ignoreContext = True
    fields = Fields(IAuthForm)

    label = _('Authorization')

    def publishTraverse(self, request, name):
        if getUtility(IPortalRegistration).authorizePrincipal(name):
            self.authorized = True
            IStatusMessage(request).add(_("Authorization completed."))
        else:
            IStatusMessage(request).add(
                _("Authorization code is invalid."), 'warning')

        return self

    def render(self):
        if self.authorized:
            return self.redirect('%s/'%absoluteURL(getSite(), self.request))
        else:
            return super(AuthorizePrincipal, self).render()

    @button.buttonAndHandler(_("Authorize"))
    def authorize(self, action):
        data, errors = self.extractData()

        if errors:
            IStatusMessage(self.request).add(self.formErrorsMessage, 'error')
        else:
            if getUtility(IPortalRegistration).authorizePrincipal(data['code']):
                self.redirect(
                    u'%s/login.html'%absoluteURL(getSite(), self.request))
                IStatusMessage(self.request).add(_("Authorization completed."))
            else:
                IStatusMessage(self.request).add(
                    _("Authorization code is invalid."), 'warning')



class IAuthEmailForm(interface.Interface):

    login = schema.TextLine(
        title = _('Login'),
        description = _('Enter your login.'),
        required = True)


class ResendAuthorization(PageletForm):

    ignoreContext = True
    fields = Fields(IAuthEmailForm)

    title = label = _('Re-send authorization')

    @button.buttonAndHandler(_("Send"))
    def authorize(self, action):
        data, errors = self.extractData()

        if errors:
            IStatusMessage(self.request).add(self.formErrorsMessage, 'error')
        else:
            principal = getPrincipalByLogin(data['login'])
            if principal is None:
                IStatusMessage(self.request).add(
                    _("Can't find user with this login."), 'warning')
            else:
                authcode = getUtility(
                    IPortalRegistration).authcodeForPrincipal(principal.id)
                if authcode is not None:
                    email = IMailAddress(principal, None)
                    if email is not None:
                        template = getMultiAdapter(
                            (principal, authcode, self.request),
                            IMailAuthorizationTemplate)
                        template.send(
                            (formataddr((principal.title, email.address)),))

                IStatusMessage(self.request).add(
                    _("Authorization has been sent."))
