from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .forms.EventForm import EventForm
from .models import Event
from .forms.CommentForm import CommentForm
from .models import Comment
from meetandeat import views
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class OwnerTestMixin(UserPassesTestMixin):
    def test_func(self):
        evtUser = Event.objects.get(pk=self.kwargs['pk']).user
        ulUser = self.request.user
        print(evtUser, ulUser)
        return evtUser == ulUser

@method_decorator(login_required, name='dispatch')
class IndexView(ListView):
    model = Event

    def get_queryset(self):
        return Event.objects.filter(visible=True)


"""
class EventJoinView(DetailView):
    model = Event
    template_name = 'meetandeat/event_details.html'
    success_url = reverse_lazy('meetandeat:index')
    def get(self, request, *args, **kwargs):
        u = self.request.user
        Group.get(event_id=self.kwargs['pk']).user_set.add(u)
"""


# TODO: implement template for EventDetailView
@method_decorator(login_required, name='dispatch')
class EventDetailView(OwnerTestMixin, DetailView):
    model = Event
    template_name = 'meetandeat/event_details.html'
    form_class = CommentForm
    success_url = reverse_lazy('meetandeat:index')

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # def post(self, request, pk):
    #     event = get_object_or_404(Event, pk=pk)
    #     form = CommentForm(request.POST)
    #     print(self.request.user)
    #     if form.is_valid():
    #         text = form.cleaned_data['text']
    #         print("valid")
    #         print(text)
    #         comment = Comment(author = request.user, datetime = timezone.now,
    #                             text = "text", event = get_object_or_404(Event, pk=pk))
    #         comment.save()

            # return HttpResponseRedirect(self.succes_url)
    # def post(self, request, pk):
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         text = form.cleaned_data['text']
    #         comment = Comment(author = settings.AUTH_USER_MODEL, datetime = timezone.now,
    #                             text = text, event = get_object_or_404(Event, pk=pk))
    #         comment.save()
    #         form = CommentForm()
    #         return HttpResponseRedirect("meetandeat/event_details.html")
    # #     return Comment.objects.filter()
    #     else:
    #             print("form not valid")
    #             print(form.errors)

@method_decorator(login_required, name='dispatch')
class EventCreate(CreateView):
    model = Event
    template_name = 'meetandeat/create-event.html'
    form_class = EventForm
    # success_url = reverse_lazy('meetandeat:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
##@login_required(redirect_field_name='meetandeat:index')
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
