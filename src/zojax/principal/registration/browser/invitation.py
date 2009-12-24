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
from zope import interface, schema, component
from zope.component import getUtility
from zope.schema.interfaces import ValidationError

from z3c.form.widget import FieldWidget
from z3c.form.browser.text import TextWidget
from z3c.form.interfaces import IFormLayer, IFieldWidget
from z3c.form.validator import SimpleFieldValidator

from zojax.layoutform import button, Fields, PageletEditSubForm
from zojax.principal.invite.interfaces import IInvitations
from zojax.principal.registration.interfaces \
    import _, IPortalRegistration, IMemberRegisterAction, IMembershipInvitation


class InvitationField(schema.TextLine):
    pass


class IInvitation1Form(interface.Interface):

    code = InvitationField(
        title = _(u'Invitation code'),
        required = False)


class IInvitation2Form(interface.Interface):

    code = InvitationField(
        title = _(u'Invitation code'),
        required = True)


class InvitationForm(PageletEditSubForm):

    prefix = 'invitation'

    def update(self):
        self.regtool = getUtility(IPortalRegistration)

        super(InvitationForm, self).update()

    def getContent(self):
        return {'code': self.request.get('invitationCode', u'')}

    @property
    def fields(self):
        if getUtility(IPortalRegistration).public:
            return Fields(IInvitation1Form)
        else:
            return Fields(IInvitation2Form)

    @button.handler(IMemberRegisterAction)
    def handleRegister(self, action):
        data, errors = self.extractData()

        if not errors:
            if self.regtool.public and not data['code']:
                return

            invitation = getUtility(IInvitations).get(data['code'])
            invitation.accept(self.parentForm.registeredPrincipal)

    def isAvailable(self):
        if not self.regtool.invitation:
            return False

        return super(InvitationForm, self).isAvailable()


class InvitationWidget(TextWidget):

    size = 26


class InvitationCodeError(ValidationError):
    __doc__ = _(u'Invitation code is wrong.')


class InvitationExpiredError(ValidationError):
    __doc__ = _(u'Invitation code expired.')


class InvitationValidator(SimpleFieldValidator):
    component.adapts(
        interface.Interface,
        interface.Interface,
        interface.Interface,
        InvitationField,
        interface.Interface)

    def validate(self, value):
        super(InvitationValidator, self).validate(value)

        if getUtility(IPortalRegistration).public and not value:
            return

        invitation = getUtility(IInvitations).get(value)

        if not IMembershipInvitation.providedBy(invitation):
            raise InvitationCodeError()

        if invitation.isExpired():
            raise InvitationExpiredError()


@interface.implementer(IFieldWidget)
@component.adapter(InvitationField, IFormLayer)
def InvitationFieldWidget(field, request):
    return FieldWidget(field, InvitationWidget(request))
