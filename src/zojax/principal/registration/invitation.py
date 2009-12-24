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
from zojax.principal.invite.invitation import Invitation

from interfaces import IMembershipInvitation


class MembershipInvitation(Invitation):
    interface.implements(IMembershipInvitation)

    name = u''

    def __init__(self, name, email, subject, message):
        super(MembershipInvitation, self).__init__(email)

        self.name = name
        self.subject = subject
        self.message = message

    @property
    def email(self):
        return self.principal

    def accept(self, principal):
        self.principal = principal
        super(MembershipInvitation, self).accept()
