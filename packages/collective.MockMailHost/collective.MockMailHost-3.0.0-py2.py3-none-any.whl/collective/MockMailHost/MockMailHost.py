# -*- coding: utf-8 -*-
from Products.MailHost import MailHost

import email.message
import six


META_TYPE = 'MockMailHost'


class MockMailHost(MailHost.MailHost):

    meta_type = META_TYPE

    def __init__(self, id=''):
        super(MockMailHost, self).__init__(id)
        self.reset()

    def reset(self):
        self.messages = []
        self.messages_from = []
        self.messages_to = []
        self.msg_types = []
        self._p_changed = True

    def _send(self, mfrom, mto, messageText, debug=False):
        if isinstance(messageText, email.message.Message):
            if six.PY2:
                message = messageText.as_string()
            else:
                message = email.message_from_string(messageText)
        else:
            message = messageText
        self.messages.append(message)
        self.messages_from.append(mfrom)
        self.messages_to.append(mto)
        self._p_changed = True

    def send(self,
             messageText,
             mto=None,
             mfrom=None,
             subject=None,
             encode=None,
             immediate=False,
             charset=None,
             msg_type=None,
             ):

        # messageText may be an MIMEText object, or something else.
        # We onyl want to clean it up if it is a string.
        if isinstance(messageText, (str, six.text_type)):
            messageText = '\n'.join([
                x.strip() for x in messageText.split('\n')
            ])

        self.msg_types.append(msg_type)
        super(MockMailHost, self).send(messageText, mto, mfrom,
                                       subject, encode, immediate, charset,
                                       msg_type)

    def pop(self, idx=-1):
        result = self.messages.pop(idx)
        self._p_changed = True
        return result

    def __len__(self):
        return len(self.messages)
