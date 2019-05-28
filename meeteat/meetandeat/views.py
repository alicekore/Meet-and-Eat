from django.shortcuts import get_object_or_404, render
from .forms.EventForm import EventForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from .models import Event

# TODO: when Event is ready,replace IndexView with the IndexView below
# class IndexView(ListView):
#     model = Event


class IndexView(ListView):
    model = Event


class CreateEventView(View):
    def get(self, request):
        return render(request, 'meetandeat/create-event.html')

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            print('valid')
            # TODO: Check if this works
            event = Event(
                user=request.user,
                title=form.cleaned_data['event_name'],
                description=form.cleaned_data['description'],
                participants=form.cleaned_data['person_number'],
                location=form.cleaned_data['place'],
                datetime=form.cleaned_data['datetime'],
            )
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

        return render(request, 'meetandeat/edit-event.html', {'form': form})

    def post(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        form = EventForm(request.POST)
        if form.is_valid():
            # TODO: when a form is valid, change Event object with data from form and save it
            # save data from form
            event.title = form.cleaned_data['event_name']
            event.description = form.cleaned_data['description']
            event.location = form.cleaned_data['place']
            event.participants = form.cleaned_data['person_number']
            event.datetime = form.cleaned_data['datetime']

            event.save()
            return HttpResponseRedirect(reverse('meetandeat:index'))
        else:
            return render(request, 'meetandeat/edit-event.html', {'form': form})

class ProfileView(View):
    def get(self,request):
        #if logged in show profile
        #TODO: get personal Info
        context = {}
        return render(request, 'meetandeat/profile.html', context)
