from persistent_messages.models import Message
from persistent_messages.forms import ComposeForm
from persistent_messages.storage import get_user
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.defaultfilters import linebreaksbr
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _


def message_detail(request, message_id):
    user = get_user(request)
    if not user.is_authenticated():
        raise PermissionDenied

    message = get_object_or_404(Message, user=user, pk=message_id)
    message.read = True
    message.save()
    
    if not request.is_ajax():
      return render_to_response('persistent_messages/message/detail.html', {'message': message}, 
          context_instance=RequestContext(request))
    else:
        return HttpResponse(linebreaksbr(message.message)) # mimetype='application/javascript'
    


def message_delete(request, message_id):
    user = get_user(request)
    if not user.is_authenticated():
        raise PermissionDenied

    message = get_object_or_404(Message, user=user, pk=message_id)
    message.delete()

    if not request.is_ajax():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/')
    else:
        return HttpResponse('')


def message_delete_all(request):
    user = get_user(request)
    if not user.is_authenticated():
        raise PermissionDenied

    Message.objects.filter(user=user).delete()

    if not request.is_ajax():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/')
    else:
        return HttpResponse('')


def message_mark_read(request, message_id):
    user = get_user(request)
    if not user.is_authenticated():
        raise PermissionDenied

    message = get_object_or_404(Message, user=user, pk=message_id)
    message.read = True
    message.save()

    if not request.is_ajax():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/')
    else:
        return HttpResponse('')


def message_mark_all_read(request):
    user = get_user(request)
    if not user.is_authenticated():
        raise PermissionDenied

    Message.objects.filter(user=user).update(read=True)
    if not request.is_ajax():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/')
    else:
        return HttpResponse('')


def message_inbox(request, template_name='persistent_messages/message_inbox.html'):
    """
    Displays a list of received messages for the current user.
    Optional Arguments:
        ``template_name``: name of the template to use.
    """
    user = get_user(request)
    #if not user.is_authenticated():
    #    raise PermissionDenied
    
    message_list = Message.objects.filter(user=user)
    return render_to_response(template_name, {
        'message_list': message_list,
    }, context_instance=RequestContext(request))
message_inbox = login_required(message_inbox)
        
        
def message_compose(request, to_user=None, form_class=ComposeForm, template_name='persistent_messages/message_compose.html', success_url=None):
    """
    Displays and handles the ``form_class`` form to compose new messages.
    Required Arguments: None
    Optional Arguments:
        ``to_user``: username of a `django.contrib.auth` User, who should receive the message
                       could be separated by a '+'
        ``form_class``: the form-class to use
        ``template_name``: the template to use
        ``success_url``: where to redirect after successfull submission
    """
    if request.method == "POST":
        from_user = request.user
        form = form_class(request.POST)
        if form.is_valid():
            form.save(from_user=request.user)
            #request.user.message_set.create(                message=_(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('message_inbox')
            if request.GET.has_key('next'):
                success_url = request.GET['next']
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()
        if to_user is not None:
            to_user = get_object_or_404(User, username=to_user)
            form.fields['to_user'].initial = to_user
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))
message_compose = login_required(message_compose)

def message_reply(request, message_id, form_class=ComposeForm, template_name='persistent_messages/message_compose.html', success_url=None):
    """
    Prepares the ``form_class`` form for writing a reply to a given message
    (specified via ``message_id``). Uses the ``format_quote`` helper from
    ``messages.utils`` to pre-format the quote.
    """
    
    print message_id
    parent = get_object_or_404(Message, id=message_id)
    
    if parent.user != request.user:
        raise Http404
    
    if request.method == "POST":
        from_user = request.user
        form = form_class(request.POST)
        if form.is_valid():
            form.save(from_user=request.user, parent_msg=parent)
            # request.user.message_set.create(                message=_(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_compose')
            return HttpResponseRedirect(success_url)
    else:
        form = form_class({
            'message': _(u"%(from_user)s wrote:\n%(message)s") % {
                'from_user': parent.from_user, 
                'message': parent.message
                }, 
            'subject': _(u"Re: %(subject)s") % {'subject': parent.subject},
            'to_user': parent.from_user
            })
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))
message_reply = login_required(message_reply)        
