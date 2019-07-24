from django import template

register = template.Library()

@register.inclusion_tag('notification.html', takes_context = True)
def notification_center(context):
    context_add = {}
    user = context['user']
    groups = user.groups.all()
    notifications = list(user.notification_receiver_user.all())

    for group in groups:
        notifications += list(group.notification_receiver_group.all())

    notifications.sort(key = lambda x: x.id, reverse = True) # Sorting Notifications in descending order

    unread = sum(not notification.read for notification in notifications)

    context_add.update({
        'notifications' :   notifications[:10],
        'unread'        :   unread
        })
    return context_add