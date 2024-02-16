from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import User, Comment
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
@login_required(login_url='/users')
def index(request):
    #return HttpResponse('HELLO!!!!!')
    user_list = User.objects.order_by('-id')[:5]
    user_count = User.objects.order_by('-id').count()
    context = {'user_list': user_list, 'user_count' : user_count}
    return render(request, 'users/index.html', context)

@login_required(login_url='/users')
def userlist(request):
    #return HttpResponse('HELLO!!!!!')
    user_list = User.objects.order_by('-id')[:5]
    context = {'user_list': user_list}
    return render(request, 'users/users.html', context)

@login_required(login_url='/users')
def add(request):
    return render(request, 'users/adduser.html')

@login_required(login_url='/users')
@permission_required('users.change_user', login_url='/users/login')
def processadd(request):
    user_fname = request.POST.get('user_fname')
    user_lname = request.POST.get('user_lname')
    user_position = request.POST.get('user_position')
    user_email = request.POST.get('user_email')
    user_username = request.POST.get('user_username')
    user_password = request.POST.get('user_password')
    if request.FILES.get('user_image'):
        user_image = request.FILES.get('user_image')
    else:
        user_image = 'profile_pic/image.jpg'
    try:
        n = User.objects.get(user_email=user_email)
        return render(request, 'users/adduser.html', {'error_message' : "User already exists!: " + user_email})
    except ObjectDoesNotExist:
        user = User.objects.create(user_email=user_email, user_fname=user_fname, user_lname=user_lname, user_position=user_position, user_username = user_username, user_password=user_password,user_image=user_image) 
        user.save()
    return HttpResponseRedirect('/users/userlist')

@login_required(login_url='/users')
def userdetail(request, profile_id):
    try:
        user = User.objects.get(pk=profile_id)
        comment = Comment.objects.filter(user_id=profile_id)
        comment_count = Comment.objects.filter(user_id=profile_id).count()
    except User.DoesNotExist:
        raise Http404("Profile does not exist!")
    return render(request, 'users/detail.html', {"user": user, "comment" : comment, "comment_count" : comment_count})

@login_required(login_url='/users')
def delete(request, profile_id):
    User.objects.filter(id=profile_id).delete()
    return HttpResponseRedirect('/users/userlist')

@login_required(login_url='/users')
def update(request, profile_id):
    try:
        user = User.objects.get(pk=profile_id)
    except User.DoesNotExist:
        raise Http404("Profile does not exist!")
    return render(request, 'users/update.html', {"user": user})

@login_required(login_url='/users')
def processedit(request, profile_id):
    user = get_object_or_404(User, pk=profile_id)
    profile_pic = request.FILES.get('user_image')
    try:
        user_fname = request.POST.get('user_fname')
        user_lname = request.POST.get('user_lname')
        user_position = request.POST.get('user_position')
        user_email = request.POST.get('user_email')
        user_username = request.POST.get('user_username')
        user_password = request.POST.get('user_password')

    except (KeyError, User.DoesNotExist):
        return render(request, 'users/detail.html', {'user':user, 'error_message': "Problem updating record",} )
    else:
        user_profile = User.objects.get(id=profile_id)
        user_profile.user_fname = user_fname
        user_profile.user_lname = user_lname
        user_profile.user_position = user_position
        user_profile.user_email = user_email
        user_profile.user_username = user_username
        user_profile.user_password = user_password
        if profile_pic:
            user_profile.user_image = profile_pic
        user_profile.save()
        return HttpResponseRedirect(reverse('users:userdetail', args=(profile_id,)))
    
def loginview(request):
    return render(request, 'users/login.html')

def process(request):
    username = request.POST.get('username')
    password = request.POST.get('password')


    user = authenticate(username=username, password=password)
    if user is not None:

        login(request, user)
        return HttpResponseRedirect('/users/dashboard')
    else:

        return render(request, 'users/login.html', {'error_message' : "LOGIN FAILED!!"})

def processlogout(request):
    logout(request)
    return HttpResponseRedirect('/users')