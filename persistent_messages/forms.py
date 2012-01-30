import datetime
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from persistent_messages.models import Message
from persistent_messages import constants 

class ComposeForm(forms.Form):
    """
    A simple default form for private messages.
    """
    to_user = forms.CharField(label=_(u"Recipient"))
    subject = forms.CharField(label=_(u"Subject"))
    message = forms.CharField(label=_(u"Message"),
        widget=forms.Textarea(attrs={'rows': '12', 'cols':'55'}))
    
        
    def __init__(self, *args, **kwargs):
        super(ComposeForm, self).__init__(*args, **kwargs)
                
    def save(self, from_user, parent_msg=None):
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        to_user = get_object_or_404(User, username=self.cleaned_data['to_user'])
        level = constants.MESSAGE
        
        # Update the parent_msg `replied` field to true
        if parent_msg is not None:
            parent_msg.replied = True
            parent_msg.save()
        
        
        message = Message(user=to_user, level=level, message=message, subject=subject, from_user=from_user, parent_msg=parent_msg)
        return message.save()