from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from meetandeat import views
from django.http import HttpResponseRedirect
from .forms.EventForm import EventForm
from .forms.TagForm import TagForm
from .forms.TagFilterForm import TagFilterForm
from .models import Event, Tag


class UserIsInGroupMixin(UserPassesTestMixin):
    def test_func(self):
        evt = Event.objects.get(pk=self.kwargs['pk'])
        u = self.request.user
        return (u in evt.eventParticipants.all())


class OwnerTestMixin(UserPassesTestMixin):
    def test_func(self):
        evtUser = Event.objects.get(pk=self.kwargs['pk']).user
        ulUser = self.request.user
        print(evtUser, ulUser)
        return evtUser == ulUser


@method_decorator(login_required, name='dispatch')
class IndexView(View):
    def get(self, request):
        form = TagFilterForm()
        events = Event.objects.filter(visible=True)
        return render(request, 'meetandeat/event_list.html', context={'event_list': events, 'form': form})

    # Filter Events by Tags
    def post(self, request):
        form = TagFilterForm(request.POST)
        events = Event.objects.filter(visible=True)
        if form.is_valid():
            tags = form.cleaned_data.get('tags')
            if tags:
                events = events.filter(tags__in=tags).distinct()
            return render(request, 'meetandeat/event_list.html', context={'event_list': events, 'form': form})
        else:
            return render(request, 'meetandeat/event_list.html', context={'event_list': events, 'form': form})


@method_decorator(login_required, name='dispatch')
class EventJoinView(View):
    def get(self, request, *args, **kwargs):
        e = Event.objects.get(id=self.kwargs['pk'])
        u = self.request.user
        e.eventParticipants.add(u)
        return redirect('meetandeat:event-view', pk=e.pk)


# TODO: implement template for EventDetailView
@method_decorator(login_required, name='dispatch')
class EventDetailView(UserIsInGroupMixin, DetailView):
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


class EventUpdate(UpdateView):
    model = Event
    template_name = 'meetandeat/edit-event.html'
    form_class = EventForm
    success_url = reverse_lazy('meetandeat:index')


class TagView(ListView):
    model = Tag


class TagCreate(CreateView):
    model = Tag
    template_name = 'meetandeat/create-tag.html'
    form_class = TagForm
    success_url = reverse_lazy('meetandeat:index')


class TagUpdate(UpdateView):
    model = Tag
    template_name = 'meetandeat/edit-tag.html'
    form_class = TagForm
    success_url = reverse_lazy('meetandeat:index')


class TagDetailView(DetailView):
    model = Tag
    template_name = 'meetandeat/tag_details.html'
    success_url = reverse_lazy('meetandeat:index')


@method_decorator(login_required, name='dispatch')
# @login_required(redirect_field_name='meetandeat:index')
class EventUpdate(OwnerTestMixin, UpdateView):
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
            'event_list': Event.objects.filter(reported=True)
        }
        return render(request, "meetandeat/mod_event_list.html", context=context)


@method_decorator(login_required, name='dispatch')
class modHide(View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.visible = False
        event.save()
        return HttpResponseRedirect("/mod")


@method_decorator(login_required, name='dispatch')
class modUnhide(View):

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.visible = True
        event.save()
        return HttpResponseRedirect("/mod")


@method_decorator(login_required, name='dispatch')
class modUnreport(View):

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.reported = False
        event.save()
        return HttpResponseRedirect("/mod")

# TODO: EventDelete view
