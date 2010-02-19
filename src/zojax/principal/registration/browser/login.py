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
from zope.component import getUtility, queryUtility, queryMultiAdapter
from zope.app.security.interfaces import IAuthentication

from zojax.layoutform import Fields, PageletEditSubForm
from zojax.authentication.interfaces import ILoginService, ISuccessLoginAction
#from zojax.authentication.browser.login import LoginForm

from zojax.principal.registration.interfaces import _


class LoginSubForm(PageletEditSubForm):

    title = _(u'Login')
    
    logins = ()

    def update(self):
        super(LoginSubForm, self).update()
        request = self.request
        auth = getUtility(IAuthentication)
        loginService = queryMultiAdapter((auth, request), ILoginService)
        if loginService is not None:
            self.logins = filter(lambda x: x.id != 'default.login', \
                                 loginService.challengingActions())