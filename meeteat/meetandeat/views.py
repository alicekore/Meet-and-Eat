from django.shortcuts import get_object_or_404, render
from .forms.EventForm import EventForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from .models import Event


class IndexView(ListView):
    model = Event


class CreateEventView(View):
    def get(self, request):
        return render(request, 'meetandeat/create-event.html')

    def post(self, request):
        event = Event(user=request.user)
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            # print('valid')
            form.save()
            return HttpResponseRedirect(reverse('meetandeat:index'))
        else:
            return render(request, 'meetandeat/create-event.html', {'form': form})


class EditEventView(View):

    def get(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        form = EventForm(instance=event)
        return render(request, 'meetandeat/edit-event.html', {'form': form})

    def post(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            # save data from form
            form.save()

            return HttpResponseRedirect(reverse('meetandeat:index'))
        else:
            return render(request, 'meetandeat/edit-event.html', {'form': form})
