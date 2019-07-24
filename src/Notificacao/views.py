from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from . import models
from django.contrib import messages

# Create your views here.

# MiddlewareViews
def readNotification(request, *args, **kwargs):
    notification = models.Notification.objects.get(id = kwargs.pop('id'))
    notification.read = True
    notification.save()

    if notification.related_url != None:
        redirect_url = notification.related_url
    else:
        redirect_url = request.META.get('HTTP_REFERER')
        messages.info(request, 'A notificação não possui URL de referência.')

    return redirect(redirect_url, permanet = True)

def createNotification(request, *args, **kwargs):

    # Getting URL parametes and normalizing
    variables = {
        'creator'       : kwargs.get('creator') if not kwargs.get('creator') == 0 else None,
        'receiver_group': kwargs.get('receiver_group') if not kwargs.get('receiver_group') == 0 else None,
        'receiver_user' : kwargs.get('receiver_user') if not kwargs.get('receiver_user') == 0 else None,
        'related_url'   : kwargs.get('related_url') if not kwargs.get('related_url') == '0' else None,
        'title'         : kwargs.get('title') if not kwargs.get('title') == '0' else None,
        'message'       : kwargs.get('message') if not kwargs.get('message') == '0' else None,
        'next_url'      : kwargs.get('next_url') if not kwargs.get('next_url') == '0' else request.META.get('HTTP_REFERER', '/')
    }

    # Adjusting text variables
    from urllib.parse import unquote
    variables['title'] = unquote(variables['title']).replace('+', ' ')
    variables['message'] = unquote(variables['message']).replace('+', ' ')
    
    # Testing for Creator
    if variables['creator'] is None and variables['creator'] is None:
        messages.error(request, 'Informe o recipiente da notificação')
        return redirect(request.META.get('HTTP_REFERER'), permanent = True)
    
    # Testing for Receiver
    if variables['receiver_group'] is None and variables['receiver_user'] is None:
        messages.error(request, 'Informe o recipiente da notificação')
        return redirect(request.META.get('HTTP_REFERER'), permanent = True)

    # Keeping only receiver_group if was given
    variables['receiver_user'] = None if variables['receiver_group'] else variables['receiver_user']

    # Getting Auth Objects from Parametes
    variables['creator'] = User.objects.get(id = variables['creator'])

    try:
        variables['receiver_group'] = Group.objects.get(id = variables['receiver_group'])
    except:
        variables['receiver_user'] = User.objects.get(id = variables['receiver_user'])

    # Creating Notification Object
    notification = models.Notification.objects.create(
        creator = variables['creator'], receiver_group = variables['receiver_group'], receiver_user = variables['receiver_user'],
        related_url = variables['related_url'], title = variables['title'], message = variables['message']
        )
    
    # Asserting Notification was Created 
    if notification:
        messages.success(request, 'Notificacao gerada com sucesso !')
    else:
        messages.error(request, 'Erro ao gerar notificacao.')

    return redirect(variables['next_url'], permanent = True)

def notify(creator, receiver_group, receiver_user, related_url, title, message, next_url):
    from django.utils.http import urlencode

    url = urlencode({
        'creator' : str(creator),
        'receiver_group' : str(receiver_group),
        'receiver_user' : str(receiver_user),
        'related_url' : str(related_url),
        'title' : str(title),
        'message' : str(message),
        'next_url' : str(next_url)
        })

    return ('notification/create/{}'.format(url))
