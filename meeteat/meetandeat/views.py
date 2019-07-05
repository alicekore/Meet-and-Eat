import json

from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash, logout
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import EmailMessage
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from meetandeat.tokens import account_activation_token

from .forms import *
from .models import Event, Tag, Comment
from .helpers import *
from meetandeat.tokens import account_activation_token
from django.template.loader import render_to_string
from datetime import date
import json
from .helpers import *
from .models import *

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
    def get(self, request, *args, **kwargs):
        form = TagFilterForm()
        ids = Report.objects.filter(reporter=request.user).values_list(
            'event', flat=True).distinct()
        reportedEvents = Event.objects.filter(id__in=ids)

        events = Event.objects.filter(visible=True).difference(
            reportedEvents).order_by('pk')
        return render(request, 'meetandeat/event_list.html',
                      context={'event_list': events, 'form': form, 'reportedEvents': reportedEvents})

    # Filter Events by Tags
    def post(self, request):
        form = TagFilterForm(request.POST)
        events = Event.objects.filter(visible=True)
        for event in events:
            event.set_matching(101)
        if form.is_valid():
            tags = form.cleaned_data.get('tags')
            idate = form.cleaned_data.get('date')
            time = form.cleaned_data.get('time')
            if tags:
                events = events.filter(tags__in=tags).distinct()
                for event in events:
                        if tags.count() <= event.tags.count():
                            match = 100
                        else:
                            match = event.tags.count() / tags.count() * 100
                        event.set_matching(match)

            if idate:
                events = events.filter(date=idate)
            if time:
                if idate is None:
                    # filter by todays date
                    today = date.today()
                    events = events.filter(date=today)
                 # filter by times greater than input time
                events = events.filter(time__gte=time)

            return render(request, 'meetandeat/event_list.html', context={'event_list': events, 'form': form})
        else:
            return render(request, 'meetandeat/event_list.html', context={'event_list': events, 'form': form})

@method_decorator(login_required, name='dispatch')
class EventJoinView(View):
    def get(self, request, *args, **kwargs):
        e = Event.objects.get(id=self.kwargs['pk'])
        u = self.request.user

        # Check if event is already full
        if not e.is_full():
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
    success_url = reverse_lazy('meetandeat:NotificationView')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class TagUpdate(UserIsStuffMixin, UpdateView):
    model = Tag
    template_name = 'meetandeat/edit-tag.html'
    form_class = TagDisapprovalForm
    success_url = reverse_lazy('meetandeat:tag-view')

    def form_valid(self, form):
        form.instance.approved = False
        form.instance.pending = False
        form.instance.save()
        return HttpResponseRedirect(self.get_success_url())

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
            form = ChangeProfilePictureForm(
                request.POST, request.FILES, instance=user)
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
class ModView(UserIsStuffMixin, ListView):
    model = Event
    template_name = 'meetandeat/mod_event_list.html'

    def get_queryset(self):
        events = Event.objects.annotate(num_reports=Count('reports', filter=Q(reports__valid=None))).filter(
            num_reports=1)[:5]
        return events


@method_decorator(login_required, name='dispatch')
class ModHide(UserIsStuffMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.reports.update(valid=True)
        return redirect('meetandeat:modView')


@method_decorator(login_required, name='dispatch')
class ModUnReport(UserIsStuffMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.reports.update(valid=False)
        event.visible = True
        event.save()
        return redirect('meetandeat:modView')


class UserCreateView(View):
    template_name = 'meetandeat/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("meetandeat:profile")
        return render(request, self.template_name)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("meetandeat:profile")
        form = UserRegistrationForm(request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.new_activation_attempt()
            user.save()
            sent_emails = send_activation_email(request, user)
            if sent_emails == 0:
                messages.error(request, "Something went wrong, try again")
                user.delete()
                return redirect(reverse('meetandeat:register'), {'form': form})

            messages.success(request, "You have successfully signed up, we have sent you an activation email",
                             fail_silently=True)
            return redirect(reverse('meetandeat:login'))
        else:
            return render(request, self.template_name, {'form': form})


class UserActivateAccountView(View):
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.confirm_email()
            user.save()
            messages.success(
                request, "You have activated your account. You can now sign in")
            return redirect('meetandeat:profile')
        else:
            messages.error(request, "Activation link is invalid")
            return redirect('meetandeat:profile')


class RequestActivateAccountView(View):
    def get(self, request):
        return render(request, 'meetandeat/request-activation.html')

    def post(self, request):
        form = RequestActivationLinkForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data['username'])
            if user.is_email_confirmed:
                messages.error(request, "Your account is already activated",
                               fail_silently=True)
                return redirect(reverse('meetandeat:login'))
            user.new_activation_attempt()
            user.save()
            sent_emails = send_activation_email(request, user)
            if sent_emails == 0:
                messages.error(request, "Something went wrong, try again")
                user.activation_attempt_failed()
                user.save()
                return redirect(reverse('meetandeat:login'))

            messages.success(request, "We have sent you a new activation link. Check your emails.",
                             fail_silently=True)
            return redirect(reverse('meetandeat:login'))
        else:
            return render(request, 'meetandeat/request-activation.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class RequestEmailConfirmView(View):
    def get(self, request):
        user = request.user
        if user.activation_attempts_number >= 3:
            messages.error(
                request, "You have requested too many activation emails")
            return redirect(reverse('meetandeat:profile'))
        if user.last_activation_attempt + timedelta(hours=1) > timezone.now():
            messages.error(
                request, "You have requested an activation email recently")
            return redirect(reverse('meetandeat:profile'))

        if user.is_email_confirmed:
            messages.error(request, "Your account is already activated",
                           fail_silently=True)
            return redirect(reverse('meetandeat:profile'))
        user.new_activation_attempt()
        user.save()
        sent_emails = send_activation_email(request, user)
        if sent_emails == 0:
            messages.error(request, "Something went wrong, try again")
            user.activation_attempt_failed()
            user.save()
            return redirect(reverse('meetandeat:profile'))

        messages.success(request, "We have sent you a new activation link. Check your emails.",
                         fail_silently=True)
        return redirect(reverse('meetandeat:profile'))


class RequestPasswordResetView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(request, reverse('meetandeat:index'))
        return render(request, 'meetandeat/password_reset.html')

    def post(self, request):
        if request.user.is_authenticated:
            return redirect(request, reverse('meetandeat:index'))
        form = RequestPasswordResetLinkForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data['username'])
            if not user.is_active:
                messages.error(request, "Your account is not activated",
                               fail_silently=True)
                return redirect(reverse('meetandeat:login'))
            sent_emails = send_password_reset_email(request, user)
            if sent_emails == 0:
                messages.error(request, "Something went wrong, try again")
                return redirect(reverse('meetandeat:login'))

            messages.success(request, "We have sent you a password reset link. Check your emails.",
                             fail_silently=True)
            return redirect(reverse('meetandeat:login'))
        else:
            return render(request, 'meetandeat/password_reset.html', {'form': form})


class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            return render(request, 'meetandeat/password_reset_confirm.html')
        else:
            messages.error(request, "Password reset link is invalid")
            return redirect('meetandeat:profile')

    def post(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            form = SetPasswordForm(user, request.POST)
            print('token is valid')
            if form.is_valid():
                print('form is valid')
                form.save()
                messages.success(
                    request, "You have successfully changed your password")
                return redirect('meetandeat:login')
            else:
                print('form is invalid')

                return render(request, 'meetandeat/password_reset_confirm.html', {'form': form})
        else:
            print('form is invalid')
            messages.error(request, "Password reset link is invalid")
            return redirect('meetandeat:profile')


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = get_user_model()
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = 'meetandeat/edit-profile.html'
    success_url = reverse_lazy('meetandeat:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        if 'email' in form.changed_data:
            form.instance.new_email()
            user = form.save(commit=False)
            request = self.request
            user.new_activation_attempt()
            user.save()
            sent_emails = send_activation_email(request, user)
            if sent_emails == 0:
                messages.error(
                    request, "Something went wrong, request an activation link")
                user.set_old_email()
                user.save()
                return redirect(reverse('meetandeat:profile'), {'form': form})

            messages.success(request, "We have sent you an activation link. Check your emails.",
                             fail_silently=True)
            return redirect(reverse('meetandeat:profile'))
        super().form_valid(form)
        return redirect(reverse('meetandeat:profile'))


@method_decorator(login_required, name='dispatch')
class UserDeleteAjax(View):
    def post(self, request):
        form = DeleteProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            logout(request)
            form.instance.delete()
            response = {'status': 0, 'message': "Ok",
                        "url": reverse('meetandeat:index')}
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

        """ if event owner leaves his own event,
        pick a random participant and make him the new owner
        if there are no participants left, the event will be deleted.
        """

        if user == event.user:
            rand_participant = event.eventParticipants.all().first()
            if rand_participant:
                event.user = rand_participant
                event.save()
            else:
                event.delete()

        return redirect('meetandeat:index')


@method_decorator(login_required, name='dispatch')
class EventReport(View):
    def post(self, request, *args, **kwargs):
        event = Event.objects.get(id=self.kwargs['pk'])
        user = request.user
        Report.objects.create(reporter=user, event=event)
        event.leave(user=user)
        event.hide_by_enough_reports()
        """
        totalNumberOfReports = event.reports.filter(valid=None).count()
        if totalNumberOfReports >= 5:
            event.visible = False
            event.save()
        """
        # leave event if user is part of event

        return redirect('meetandeat:index')


@method_decorator(login_required, name='dispatch')
class ApproveTag(UserIsStuffMixin, View):
    def get(self, request, *args, **kwargs):
        tag = Tag.objects.get(id=self.kwargs['pk'])
        tag.approved = True
        tag.pending = False
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

class NotificationView(View):
    def get(self, request):
        User = self.request.user
        tags = Tag.objects.filter(user=User).order_by("pk")
        return render(request, 'meetandeat/notification_list.html', context={'tags': tags})

def comments_changed(request):
    """ 
    This view is used for dynamical loading of comments inside events.
    returns a JsonResponse with event comment-list, rendered as html
    """
    event_id = request.GET.get('event_id', None)
    event_comments = Comment.objects.filter(event=event_id)

    comments_count_get = int(request.GET.get('comments_amount', None))

    difference = abs(event_comments.count() - comments_count_get)
    comments_changed = difference > 0

    data = {
        'comments_changed': comments_changed
    }

    """
    return data only if changed or on first load
    """
    if data['comments_changed']:
        data['comment_count'] = event_comments.count()
        data['html'] = render_to_string('meetandeat/comment-list.html', context={'request': request,'comment_list': event_comments})

    return JsonResponse(data, safe=False)
