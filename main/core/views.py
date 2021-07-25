from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import receiver
from .models import Account
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from .models import Event_detailed, Event_simple
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import datetime
from django.http.response import HttpResponseRedirect
from django.core.mail import EmailMessage

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            acc = get_object_or_404(Account, user = self.request.user)
            context['type_acc'] = acc.status
            context['ES'] = Event_simple.objects.exclude(participants = acc)
            context['ED'] = Event_detailed.objects.exclude(participants = acc)
            return context
        except:
            pass

class SignupPageView(generic.CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

@receiver(signals.post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    try:
        acc = Account.objects.create(user = instance)
    except:
        pass

def personal_area(request):
    template = 'personal_area.html'
    context = {}
    acc = get_object_or_404(Account, user_id = request.user.id)
    context['type_acc'] = acc.status
    if context['type_acc'] == 'staff':
        context['ES'] = Event_simple.objects.filter(author = acc)
        context['ED'] = Event_detailed.objects.filter(author = acc)
    elif context['type_acc'] == 'client':
        context['ES'] = Event_simple.objects.filter(participants = acc)
        context['ED'] = Event_detailed.objects.filter(participants = acc)
    else:
        return HttpResponse('Error: account error')
    return render(request, template, context)

@login_required
def get_data_staff(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    dt_object = request.POST.get('datetime')
    
    _format = "%m/%d/%Y %I:%M %p"
    dt_object = datetime.datetime.strptime(dt_object, _format)

    return title, content, dt_object

@login_required
def add_event_s(request):
    title, content, dt_object = get_data_staff(request)
    Event_simple.objects.create(
        author = Account.objects.get(user = request.user),
        title = title,
        body = content,
        date_event = dt_object
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def add_event_d(request):
    title, content, dt_object = get_data_staff(request)
    Event_detailed.objects.create(
        author = Account.objects.get(user = request.user),
        title = title,
        body = content,
        date_event = dt_object
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

from django.conf import settings

@login_required
def participate_s(request, _id):
    es = Event_simple.objects.get(id = _id)
    acc = get_object_or_404(Account, user = request.user)
    es.participants.add(acc)
    try:
        email = EmailMessage(f'NEW simple participate ', f'{acc.user.email}', settings.EMAIL_HOST_USER , to=[es.author.user.email])
        email.send(fail_silently=False)
    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def participate_d(request):

    title = request.POST.get('title')
    content = request.POST.get('content')
    _id = request.POST.get('id')
    ed = Event_detailed.objects.get(id = _id)
    acc = get_object_or_404(Account, user = request.user)
    ed.participants.add(acc)
    ed.client_title = title
    ed.client_body = content
    ed.client_file = request.FILES['file']
    ed.save()

    try:
        email = EmailMessage(f'NEW detailed participate ', f'{acc.user.email}', settings.EMAIL_HOST_USER , to=[ed.author.user.email])
        email.send(fail_silently=False)
    except:
        pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


from django.http import JsonResponse

@login_required
def json_Participate_s(request, _id):
    context = {}
    try:
        es = Event_simple.objects.get(id = _id)
    except:
        return HttpResponse('Error: Object error')

    if request.user == es.author.user:
        context['data'] = list(es.participants.values_list('user__email', flat=True).all())
        return JsonResponse(context, safe=False)
    else:
        return HttpResponse('Error: account error')

@login_required
def json_Participate_d(request, _id):
    context = {}
    try:
        ed = Event_detailed.objects.get(id = _id)
    except:
        return HttpResponse('Error: Object error')

    if request.user == ed.author.user:
        context['data'] = list(ed.participants.values_list('user__email', flat=True).all())
        return JsonResponse(context, safe=False)
    else:
        return HttpResponse('Error: account error')
