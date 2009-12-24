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

from zope.component import getUtility
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL
from zope.dublincore.interfaces import IDCDescriptiveProperties

from zojax.mail.interfaces import IMailer, IMailAddress
from zojax.mailtemplate.interfaces import IMailTemplate


class AuthorizationMailTemplate(object):

    def update(self):
        request = self.request
        principal = self.context
        self.authcode = self.contexts[0]

        configlet = getUtility(IMailer)
        self.email_from_name = configlet.email_from_name
        self.email_from_address = configlet.email_from_address

        site = getSite()

        self.url = '%s/authorizeprincipal.html/%s/'%(
            absoluteURL(site, request), self.authcode)

        self.portal = IDCDescriptiveProperties(site).title

    @property
    def subject(self):
        return u'%s: registration confirmation'%self.portal
