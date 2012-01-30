from django.conf.urls.defaults import *

urlpatterns = patterns('persistent_messages.views',
    url(r'^detail/(?P<message_id>\d+)/$', 'message_detail', name='message_detail'),
    url(r'^inbox/$', 'message_inbox', name='message_inbox'),

    # Mark read
    url(r'^mark_read/(?P<message_id>\d+)/$', 'message_mark_read', name='message_mark_read'),
    url(r'^mark_read/all/$', 'message_mark_all_read', name='message_mark_all_read'),
    
    # Delete
    url(r'^delete/message/(?P<message_id>\d+)/$', 'message_delete', name='message_delete'),
    url(r'^delete/all/$', 'message_delete_all', name='message_delete_all'),
    
    # Compose and Reply
    url(r'^compose/$', 'message_compose', name='message_compose'),
    url(r'^compose/(?P<to_user>[\+\w]+)/$', 'message_compose', name='message_compose_to'),
    url(r'^reply/(?P<message_id>[\d]+)/$', 'message_reply', name='message_reply'),
    
    
)
