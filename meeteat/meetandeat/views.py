from django.shortcuts import get_object_or_404, render
from .forms.EventForm import EventForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

# TODO: when Event is ready,replace IndexView with the IndexView below
# class IndexView(ListView):
#     model = Event


class IndexView(View):
    def get(self, request):
        # TODO: implement context
        # events = Event.objects.all()[:5]
        # context = {'event_list': events}
        context = {}
        return render(request, 'meetandeat/dashboard.html', context)


class CreateEventView(View):
    def get(self, request):
        return render(request, 'meetandeat/create-event.html')

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            # TODO: when a form is valid, create new Event object with data from form and save it
            # event = Event(datetime = form.cleaned_data['datetime'],...)
            # event.save()
            return HttpResponseRedirect(reverse('meetandeat:index'))
        else:
            return render(request, 'meetandeat/create-event.html', {'form': form})


class EditEventView(View):

    def get(self, request, event_id):
        # event = get_object_or_404(Event, pk=event_id)
        # form = EventForm(initial={'event_name': event.name,
        #                           'description': event.description,
        #                           'datetime': event.datetime,
        #                           'person_number': event.person_number,
        #                           'place': event.place})
        # TODO: comment it out, when Event is ready
        form = EventForm()

        return render(request, 'meetandeat/edit-event.html', {'form': form})

    def post(self, request, event_id):
        # event = get_object_or_404(Event, pk=event_id)
        form = EventForm(request.POST)
        if form.is_valid():
            # TODO: when a form is valid, change Event object with data from form and save it
            # save data from form
            # event.datetime = form.cleaned_data['datetime']
            # task.save()
            return HttpResponseRedirect(reverse('meetandeat:index'))
        else:
            return render(request, 'meetandeat/edit-event.html', {'form': form})

class ProfileView(View):
    def get(self,request):
        #if logged in show profile
        #TODO: get personal Info
        context = {}
        return render(request, 'meetandeat/profile.html', context)
