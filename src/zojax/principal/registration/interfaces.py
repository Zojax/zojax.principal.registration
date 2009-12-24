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
from zope import schema, interface
from zope.i18nmessageid import MessageFactory
from zope.component.interfaces import IObjectEvent, ObjectEvent
from zojax.principal.invite.interfaces import IInvitation

_ = MessageFactory('zojax.principal.registration')


class InvalidAuthorizationCode(Exception):
    """Invalid authorization code"""


class ILoginField(schema.interfaces.IText):
    """ principal login field """


class INewLoginField(ILoginField):
    """ new login field """


class IEMailLoginField(ILoginField):
    """ principal login field """


class INewEMailLoginField(INewLoginField):
    """ new principal login field """


class LoginAlreadyInUse(schema.ValidationError):
    __doc__ = _(u'Login name already in use.')


STATUS_CONTINUE = 1

STATUS_PROCESSED = 2


class IPortalRegistration(interface.Interface):
    """ portal membership configlet """

    actions = schema.List(
        title = _(u'Registration method'),
        description = _(u'Select portal registration method.'),
        value_type = schema.Choice(vocabulary='zojax.principal.registration'),
        default = [],
        required = False)

    public = schema.Bool(
        title = _('Public'),
        description = _('Member registration is public.'),
        default = True,
        required = False)

    invitation = schema.Bool(
        title = _('Invitation'),
        description = _('Use invitation system for member registration.'),
        default = False,
        required = False)

    authorization = schema.Bool(
        title = _('Authorization'),
        description = _('Enable email member authorization.'),
        default = False,
        required = False)

    def getActions():
        """ return action objects """

    def registerPrincipal(principal, request):
        """ register principal, return status """

    def invitePerson(principal, email, subject, message):
        """ invite person by email """

    def listAuthorizations():
        """ list authorizations """

    def authorizePrincipal(authcode):
        """ authorize principal by authcode """

    def principalAuthorization(principal):
        """ start authorization process for principal, generate auth code """

    def authcodeForPrincipal(pid):
        """ return authcode for principal """

    def principalByAuthcode(authcode):
        """ return principal id for authcode """

    def removePrincipalAuthorization(pid):
        """ remove principal authorization information """


class IMemberRegisterAction(interface.Interface):
    """ marker interface for form register action """


class IMemberRegistrationForm(interface.Interface):
    """ marker interface for member registration form """

    registeredPrincipal = interface.Attribute('Registered principal')


class IMemberRegistrationAction(interface.Interface):
    """ registration action """

    name = schema.TextLine(
        title = u'Name',
        description = u'Action name',
        required = True)

    title = schema.TextLine(
        title = u'Title',
        description = u'Action title',
        required = False)

    description = schema.TextLine(
        title = u'Description',
        description = u'Action description',
        required = False)

    def isAvailable():
        """ is this action available """


class IAfterRegistrationAction(interface.Interface):
    """ after registration action """

    def __init__(reg, principal, request):
        """ adapter factory """

    def process():
        """ process action, return True or False """


class IPrincipalRegisteredEvent(interface.Interface):
    """ principal registered event """

    principal = interface.Attribute('Registered principal')


class PrincipalRegisteredEvent(object):
    interface.implements(IPrincipalRegisteredEvent)

    def __init__(self, principal):
        self.principal = principal


class IMembershipInvitation(IInvitation):

    name = interface.Attribute('Name')
    email = interface.Attribute('Email')
    subject = interface.Attribute('Subject')
    message = interface.Attribute('Message')


class IMailAuthorizationAware(interface.Interface):
    """ marker interface for registered principal
    that supports authorization by email """


class IMailAuthorizationTemplate(interface.Interface):
    """ mail auth template """
