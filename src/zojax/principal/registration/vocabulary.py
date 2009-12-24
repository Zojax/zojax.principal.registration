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
from zope.component import getUtilitiesFor
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from interfaces import IMemberRegistrationAction


class Vocabulary(SimpleVocabulary):

    def getTerm(self, value):
        try:
            return self.by_value[value]
        except KeyError:
            return self.by_value[self.by_value.keys()[0]]


class MemberRegistrations(object):
    """
    >>> from zope import interface, component
    >>> from zojax.principal.registration.interfaces import IMemberRegistrationAction

    >>> class Action(object):
    ...     interface.implements(IMemberRegistrationAction)
    ...     def __init__(self, name, title, avialable):
    ...         self.name = name
    ...         self.title = title
    ...         self.avialable = avialable
    ...     def isAvailable(self):
    ...         return self.avialable

    >>> component.provideUtility(Action('a1', 'Action 1', True), name='a1')
    >>> component.provideUtility(Action('a2', 'Action 2', False), name='a2')

    >>> from zojax.principal.registration.vocabulary import MemberRegistrations
    >>> factory = MemberRegistrations()
    >>> voc = factory(None)

    >>> for term in voc:
    ...     print term.value, term.title
    a1 Action 1

    >>> voc.getTerm('a1').title
    'Action 1'

    >>> voc.getTerm('unknown').title
    'Action 1'

    """
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        result = []
        for name, action in getUtilitiesFor(IMemberRegistrationAction):
            if action.isAvailable():
                result.append((action.title, name, action))

        result.sort()
        return Vocabulary([SimpleTerm(name, name, title)
                           for title, name, r in result])
