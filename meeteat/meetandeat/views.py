from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages

from .forms.EventForm import EventForm
from .forms.UserRegistrationForm import UserRegistrationForm
from .models import Event
from meetandeat import views

from django.http import HttpResponseRedirect

from django.shortcuts import get_object_or_404

@method_decorator(login_required, name='dispatch')
class IndexView(ListView):
    model = Event


# TODO: implement template for EventDetailView
@method_decorator(login_required, name='dispatch')
class EventDetailView(DetailView):
    model = Event
    template_name = 'meetandeat/event_details.html'
    success_url = reverse_lazy('meetandeat:index')


@method_decorator(login_required, name='dispatch')
class EventCreate(CreateView):
    model = Event
    template_name = 'meetandeat/create-event.html'
    form_class = EventForm
    success_url = reverse_lazy('meetandeat:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class EventUpdate(UpdateView):
    model = Event
    template_name = 'meetandeat/edit-event.html'
    form_class = EventForm
    success_url = reverse_lazy('meetandeat:index')


@method_decorator(login_required, name='get')
class ProfileView(View):
    def get(self, request):
        # TODO: get personal Info
        context = {}
        return render(request, 'meetandeat/profile.html', context)


@method_decorator(login_required, name='dispatch')
class modView(View):

    def get(self, request):
        context = {
            'event_list' : Event.objects.filter(reported=True)
            }
        return render(request, "meetandeat/mod_event_list.html", context=context)


@method_decorator(login_required, name='dispatch')
class modHide(View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.visible=False
        event.save()
        return HttpResponseRedirect("/mod")


@method_decorator(login_required, name='dispatch')
class modUnhide(View):

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.visible=True
        event.save()
        return HttpResponseRedirect("/mod")

@method_decorator(login_required, name='dispatch')
class modUnreport(View):

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.reported=False
        event.save()
        return HttpResponseRedirect("/mod")

# TODO: EventDelete view

class UserRegistrationView(FormView):
    form_class = UserRegistrationForm
    template_name = 'meetandeat/register.html'

    def get(self, request):
        form = self.form_class(initial = self.initial)
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('/profile')
        else:
            form = UserRegistrationForm()
            context =  {'form':form}

        return render(request, self.template_name, {'form':form})
