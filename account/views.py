from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.views.generic import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str , force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from social.models import Post
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
# Create your views here.

def log_out(request):
    logout(request)
    return redirect('account:login')

class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('account:login') 

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('social:profile')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        cd = form.cleaned_data
        user = form.save(commit=False)
        user.set_password(cd['password2'])
        user.save()
        messages.success(self.request, 'your register is successful')
        return super().form_valid(form)

class EditUserView(LoginRequiredMixin,FormView):
    template_name = 'registration/edit_user.html'
    form_class = EditUserForm
    success_url = reverse_lazy('social:profile')
    login_url = 'account:login'
    
    def form_valid(self, form):
        user = User.objects.get(pk=self.request.user.pk)
        cd = form.cleaned_data
        user_image = self.request.FILES.get('photo')
        user.first_name = cd['first_name']
        user.last_name = cd['last_name']
        user.bio = cd['bio']
        user.date_of_birth = cd['date_of_birth']
        user.photo = user_image
        user.save()
        return super().form_valid(form)

class ForgetPasswordView(FormView):
    template_name = 'registration/forget_password.html'
    form_class = ForgetPasswordForm
    success_url = reverse_lazy('account:send_mail_done')

    def form_valid(self, form):
        if form.is_valid():
            user_email = form.cleaned_data['email']
        user = get_object_or_404(User, email=user_email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = reverse_lazy('account:password_reset_confirm', kwargs = {'uidb64':uid, 'token':token})
        cuurent_site = get_current_site(self.request)
        domain = cuurent_site.domain
        reset_url = f"http://{domain}/{reset_url}"
        send_mail("reset-password", f"use the link for reset password :\n {reset_url}", 'mohamadbigdeli24@gmail.com', [user_email], fail_silently=False)
        return super().form_valid(form)

def send_mail_done(request):
    return render(request, 'registration/send_mail_done.html')

class PasswordResetConfirmView(FormView):
    template_name = 'registration/password_reset.html'
    form_class = PasswordResetConfirmForm
    success_url = reverse_lazy('account:login')

    def form_valid(self, form):
        cd = form.cleaned_data
        uidb64 = self.kwargs['uidb64']
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user.set_password(cd['password2'])
        user.save()
        messages.success(self.request ,'your password change done')
        return super().form_valid(form)

def user_list(request):
    users = User.objects.filter(is_active=True)
    context = {
        'users':users
    }
    return render(request, 'user/user_list.html', context)

def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    posts = Post.objects.filter(author=user).all()
    context = {
        'user':user,
        'posts':posts
    }
    return render(request, 'user/user_detail.html', context)


@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            if request.user in user.followers.all():
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
                follow=False
            else:
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                follow=True
            following_count = user.following.count
            followers_count = user.followers.count
            return JsonResponse({'follow':follow, 'followers_count':followers_count, 'following_count':following_count})
        except User.DoesNotExist: 
            return JsonResponse({'error':"user dose not exist"})
    return JsonResponse({'error':"InvalidRequest"})
