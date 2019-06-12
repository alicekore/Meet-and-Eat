from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
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
from .forms.CommentForm import CommentForm
from .models import Comment
from meetandeat import views


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
class EventUpdate(UpdateView):
    model = Event
    template_name = 'meetandeat/edit-event.html'
    form_class = EventForm
    success_url = reverse_lazy('meetandeat:index')


@method_decorator(login_required, name='dispatch')
class TagView(ListView):
    model = Tag


@method_decorator(login_required, name='dispatch')
class TagCreate(CreateView):
    model = Tag
    template_name = 'meetandeat/create-tag.html'
    form_class = TagForm
    success_url = reverse_lazy('meetandeat:index')


@method_decorator(login_required, name='dispatch')
class TagUpdate(UpdateView):
    model = Tag
    template_name = 'meetandeat/edit-tag.html'
    form_class = TagForm
    success_url = reverse_lazy('meetandeat:index')


@method_decorator(login_required, name='dispatch')
class TagDetailView(DetailView):
    model = Tag
    template_name = 'meetandeat/tag_details.html'
    success_url = reverse_lazy('meetandeat:index')


@method_decorator(login_required, name='dispatch')
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
        return render(request, 'meetandeat:profile', context)


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
