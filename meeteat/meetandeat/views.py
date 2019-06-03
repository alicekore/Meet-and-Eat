from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .forms.EventForm import EventForm
from .models import Event


class IndexView(ListView):
    model = Event


# TODO: implement template for EventDetailView
class EventDetailView(DetailView):
    model = Event
    template_name = 'meetandeat/event_details.html'
    success_url = reverse_lazy('meetandeat:index')


class EventCreate(CreateView):
    model = Event
    template_name = 'meetandeat/create-event.html'
    form_class = EventForm
    success_url = reverse_lazy('meetandeat:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EventUpdate(UpdateView):
    model = Event
    template_name = 'meetandeat/edit-event.html'
    form_class = EventForm
    success_url = reverse_lazy('meetandeat:index')

class ProfileView(View):
    def get(self,request):
        #if logged in show profile
        #TODO: get personal Info
        context = {}
        return render(request, 'meetandeat/profile.html', context)

# TODO: EventDelete view
