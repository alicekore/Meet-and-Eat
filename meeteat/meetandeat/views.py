from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .forms.EventForm import EventForm
from .models import Event


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

# TODO: EventDelete view
