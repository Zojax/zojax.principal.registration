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
from zope import interface, schema
from zope.component import getUtility, queryUtility
from zope.app.security.interfaces import IAuthentication
from zope.app.authentication.principalfolder import Principal, InternalPrincipal
from zope.app.authentication.interfaces import IAuthenticatorPlugin

from zojax.layoutform import button, Fields, PageletForm
from zojax.principal.registration.interfaces import STATUS_CONTINUE
from zojax.principal.registration.interfaces import IPortalRegistration
from zojax.principal.registration.interfaces import IMemberRegisterAction
from zojax.principal.registration.interfaces import IMemberRegistrationForm
from zojax.principal.registration.interfaces import IMailAuthorizationAware


class IRegForm1(interface.Interface):

    id = schema.TextLine(title=u'User Id')

    title = schema.TextLine(title=u'User Title')


class IRegForm2(interface.Interface):

    name = schema.TextLine(title=u'User Name')

    title = schema.TextLine(title=u'User Title')


class TestingAction1Form(PageletForm):
    interface.implements(IMemberRegistrationForm)

    fields = Fields(IRegForm1)
    ignoreContext = True

    @button.buttonAndHandler(u"Register", provides=IMemberRegisterAction)
    def handle_register(self, action):
        request = self.request

        data, errors = self.extractData()

        if not errors:
            principal = Principal(data['id'], data['title'], '')
            interface.alsoProvides(principal, IMailAuthorizationAware)

            auth = getUtility(IAuthentication)

            users = queryUtility(IAuthenticatorPlugin, 'users')

            if users is not None:
                id = 1
                while str(id) in users:
                    id = id + 1

                users[str(id)] = InternalPrincipal(
                    data['id'], '12345', data['title'])

                principal.id = auth.prefix + users.prefix + str(id)

            status = getUtility(IPortalRegistration).registerPrincipal(
                principal, request)
            if status == STATUS_CONTINUE:
                self.redirect('/test.html')

            # IMemberRegistrationForm attribute
            self.registeredPrincipal = principal


class TestingAction2Form(PageletForm):

    fields = Fields(IRegForm2)
    ignoreContext = True
