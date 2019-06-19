from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView, DeleteView
from .forms import *
from .models import Event, Tag, Comment
import json


class UserIsInGroupMixin(UserPassesTestMixin):
    def test_func(self):
        evt = Event.objects.get(pk=self.kwargs['pk'])
        u = self.request.user
        return u in evt.eventParticipants.all()


class OwnerTestMixin(UserPassesTestMixin):
    def test_func(self):
        evtUser = Event.objects.get(pk=self.kwargs['pk']).user
        ulUser = self.request.user
        print(evtUser, ulUser)
        return evtUser == ulUser


class UserIsStuffMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


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
    def get(self, request, pk):
        form = CommentForm
        event = get_object_or_404(Event, pk=pk)
        comments = Comment.objects.filter(event=pk)
        return render(request, 'meetandeat/event_details.html',
                      context={'comment_list': comments, 'event': event, 'form': form})

    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            print("valid")
            text = form.cleaned_data.get('text')
            author = request.user
            event = get_object_or_404(Event, pk=pk)
            c = Comment(author=author, text=text, event=event)
            c.save()
            return redirect('meetandeat:event-view', pk=pk)


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


@method_decorator(login_required, name='dispatch')
class TagView(UserIsStuffMixin, ListView):
    model = Tag


@method_decorator(login_required, name='dispatch')
class TagCreate(CreateView):
    model = Tag
    template_name = 'meetandeat/create-tag.html'
    form_class = TagForm
    success_url = reverse_lazy('meetandeat:index')


@method_decorator(login_required, name='dispatch')
class TagUpdate(UserIsStuffMixin, UpdateView):
    model = Tag
    template_name = 'meetandeat/edit-tag.html'
    form_class = TagForm
    success_url = reverse_lazy('meetandeat:index')


@method_decorator(login_required, name='dispatch')
class TagDetailView(UserIsStuffMixin, DetailView):
    model = Tag
    template_name = 'meetandeat/tag_details.html'
    success_url = reverse_lazy('meetandeat:index')


@method_decorator(login_required, name='dispatch')
class EventUpdate(OwnerTestMixin, UpdateView):
    model = Event
    template_name = 'meetandeat/edit-event.html'
    form_class = EventForm
    success_url = reverse_lazy('meetandeat:index')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)
        context = {
            'user': user,
        }
        return render(request, 'meetandeat/profile.html', context)

    def post(self, request):
        user = request.user
        if 'change-password' in request.POST:
            form = PasswordChangeForm(user=user, data=request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['new_password1'])
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, f'Password was changed')
            else:
                context = {
                    'user': user,
                    'form': form
                }
                return render(request, 'meetandeat/profile.html', context)
        elif 'update-image' in request.POST:
            form = ChangeProfilePictureForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
            else:
                context = {
                    'form': form,
                }
                return render(request, 'meetandeat/profile.html', context)

        elif 'delete-image' in request.POST:
            user.profilePicture.delete()
        context = {
            'user': user,
        }
        return render(request, 'meetandeat/profile.html', context)




@method_decorator(login_required, name='dispatch')
class modView(UserIsStuffMixin, View):

    def get(self, request):
        context = {
            'event_list': Event.objects.filter(reported=True).order_by("pk")
        }
        return render(request, "meetandeat/mod_event_list.html", context=context)


@method_decorator(login_required, name='dispatch')
class modHide(UserIsStuffMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.visible = False
        event.save()
        return redirect('meetandeat:modView')


@method_decorator(login_required, name='dispatch')
class modUnhide(UserIsStuffMixin, View):

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.visible = True
        event.save()
        return redirect('meetandeat:modView')


@method_decorator(login_required, name='dispatch')
class modUnreport(UserIsStuffMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        eventReporter = event.userReportings.all()
        for reporter in eventReporter:
            event.userReportings.remove(reporter)
        event.reported = False
        event.visible = True
        event.save()
        return redirect('meetandeat:modView')


class UserCreateView(CreateView):
    template_name = 'meetandeat/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('meetandeat:login')


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = get_user_model()
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = 'meetandeat/edit-profile.html'
    success_url = reverse_lazy('meetandeat:profile')

    def get_object(self, queryset=None):
        return self.request.user


@method_decorator(login_required, name='dispatch')
class UserDeleteAjax(View):
    def post(self, request):
        form = DeleteProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            logout(request)
            form.instance.delete()
            response = {'status': 0, 'message': "Ok", "url": reverse('meetandeat:index')}
            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            print('password invalid')
            response = {'status': 1, 'message': "Invalid password"}
            return HttpResponse(json.dumps(response), content_type='application/json')


@method_decorator(login_required, name='dispatch')
class UserDeleteView(View):
    def get(self, request):
        return render(request, 'meetandeat/delete-profile.html')

    def post(self, request):
        form = DeleteProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            print('form is valid')
            logout(request)
            form.instance.delete()
            return redirect(reverse("meetandeat:index"))
        else:
            print('form is not valid')
            context = {'form': form}
            return render(request, 'meetandeat/delete-profile.html', context)


@method_decorator(login_required, name='dispatch')
class EventLeave(View):
    def get(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs['pk'])
        user = request.user
        event.eventParticipants.remove(user)
        return redirect('meetandeat:index')


@method_decorator(login_required, name='dispatch')
class EventReport(View):
    def get(self, request, *args, **kwargs):
        event = Event.objects.get(id=self.kwargs['pk'])
        user = request.user
        event.userReportings.add(user)
        event.reported = True
        event.save()
        return redirect('meetandeat:index')


@method_decorator(login_required, name='dispatch')
class ApproveTag(UserIsStuffMixin, View):
    def get(self, request, *args, **kwargs):
        tag = Tag.objects.get(id=self.kwargs['pk'])
        tag.approved = True
        tag.save()
        return redirect('meetandeat:tag-view')


@method_decorator(login_required, name='dispatch')
class OwnEventsView(View):
    def get(self, request):
        user = self.request.user
        own_events = Event.objects.filter(visible=True, user=user)
        joined_events = user.events.all()
        joined_events = joined_events.exclude(user=user)
        form = TagFilterForm()
        return render(request, 'meetandeat/own_events_list.html',
                      context={'own_event_list': own_events, 'form': form, 'joined_event_list': joined_events})

    # Filter Events by Tags
    def post(self, request):
        user = self.request.user
        own_events = Event.objects.filter(visible=True, user=user)
        joined_events = user.events.all()
        joined_events = joined_events.exclude(user=user)
        form = TagFilterForm()
        if form.is_valid():
            tags = form.cleaned_data.get('tags')
            if tags:
                own_events = own_events.filter(tags__in=tags).distinct()
                joined_events = joined_events.filter(tags__in=tags).distinct()
            return render(request, 'meetandeat/own_events_list.html',
                          context={'own_event_list': own_events, 'form': form, 'joined_event_list': joined_events})
