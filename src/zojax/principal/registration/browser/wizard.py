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
from zope.component import getUtility
from zojax.layoutform import Fields, PageletEditForm
from zojax.wizard import WizardWithTabs, WizardStepForm
from zojax.wizard.step import WizardStep
from zojax.wizard.interfaces import ISaveable
from zojax.principal.registration.interfaces import \
    IPortalRegistration, IInvitations

from interfaces import _, IConfigletEditWizard


class ConfigletEditWizard(WizardWithTabs):
    interface.implements(IConfigletEditWizard)

    prefix = 'configlet.'
    id = 'configlet-edit-wizard'

    @property
    def title(self):
        return self.context.__title__

    @property
    def description(self):
        return self.context.__description__


class ConfigletEditStep(WizardStepForm, PageletEditForm):

    name = 'configlet'
    title = _('Configlet')
    label = _('Modify configlet')

    @property
    def fields(self):
        return Fields(self.getContent().__schema__)


class InvitationsEditStep(WizardStep):

    name = 'invitations'
    label = title = _('Invitations')
    description = u''

    def update(self):
        super(InvitationsEditStep, self).update()

        self.configlet = getUtility(IInvitations)

    def isAvailable(self):
        return getUtility(IPortalRegistration).invitation
