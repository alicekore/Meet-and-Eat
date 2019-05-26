from django.shortcuts import get_object_or_404, render
from .forms.EventForm import EventForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from .models import *

# TODO: when Event is ready,replace IndexView with the IndexView below
# class IndexView(ListView):
#     model = Event


class IndexView(View):
    def get(self, request):
        # TODO: implement context
        events = Event.objects.all()[:10]
        context = {'event_list': events}
        # context = {}
        return render(request, 'meetandeat/dashboard.html', context)


class CreateEventView(View):
    def get(self, request):
        return render(request, 'meetandeat/create-event.html')

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            event = Event(user=request.user,
                          datetime=form.cleaned_data['datetime'],
                          title=form.cleaned_data['event_name'],
                          description=form.cleaned_data['description'],
                          participants=form.cleaned_data['person_number'],
                          location=form.cleaned_data['place'])
            event.save()
            return HttpResponseRedirect(reverse('meetandeat:index'))
        else:
            return render(request, 'meetandeat/create-event.html', {'form': form})


class EditEventView(View):

    def get(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        form = EventForm(initial={'event_name': event.title,
                                  'description': event.description,
                                  'datetime': event.datetime,
                                  'person_number': event.participants,
                                  'place': event.location})
        # TODO: comment it out, when Event is ready
        # form = EventForm()

        return render(request, 'meetandeat/edit-event.html', {'form': form})

    def post(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        form = EventForm(request.POST)
        if form.is_valid():
            # TODO: when a form is valid, change Event object with data from form and save it
            event.datetime = form.cleaned_data['datetime']
            event.title = form.cleaned_data['event_name']
            event.description = form.cleaned_data['description']
            event.participants = form.cleaned_data['person_number']
            event.location = form.cleaned_data['place']
            event.save()
            return HttpResponseRedirect(reverse('meetandeat:index'))
        else:
            return render(request, 'meetandeat/edit-event.html', {'form': form})



