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
from z3c.schema.email import RFC822MailAddress
from zojax.authentication.utils import getPrincipalByLogin

import interfaces


class LoginField(schema.TextLine):
    interface.implements(interfaces.ILoginField)

    def set(self, context, value):
        """ lower login before set """
        if value:
            value = value.lower()
        super(LoginField, self).set(context, value)

    def validate(self, value):
        super(LoginField, self).validate(value)

        if self.context is None:
            return

        login = value.lower()
        oldlogin = self.query(self.context)

        if login != oldlogin and getPrincipalByLogin(login) is not None:
            raise interfaces.LoginAlreadyInUse()


class NewLoginField(LoginField):
    interface.implements(interfaces.INewLoginField)

    def validate(self, value):
        super(NewLoginField, self).validate(value)

        if getPrincipalByLogin(value.lower()) is not None:
            raise interfaces.LoginAlreadyInUse()


class EMailLoginField(RFC822MailAddress, LoginField):
    interface.implements(interfaces.IEMailLoginField)


class NewEMailLoginField(RFC822MailAddress, NewLoginField):
    interface.implements(interfaces.INewEMailLoginField)
