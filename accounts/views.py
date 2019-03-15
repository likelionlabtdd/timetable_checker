from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from .models import Profile
# Create your views here.

def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password_check']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
                profile = Profile(user=user)
                profile.timetable_url = request.POST['timetable_url']
                profile.save()
                auth.login(request, user)
                messages.add_message(request, messages.SUCCESS, '환영합니다!')
                return redirect('home')
            except:
                messages.add_message(request, messages.ERROR, '이미 존재하는 id입니다.')
                return redirect('signup')
        messages.add_message(request, messages.ERROR, '비밀번호가 일치하지 않습니다.')
        return redirect('signup')

    return render(request, 'signup.html')

def update(request):
    if request.method == 'POST':
        try:
            user = request.user
            Profile.objects.filter(user=user).update(
                timetable_url=request.POST['timetable_url']
            )
            messages.add_message(request, messages.SUCCESS, '정보가 수정되었습니다.')
            return render(request, 'home.html')
        except:
            print('exception')
            return redirect('update')

    return render(request, 'update.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            # 로그인 성공
            print('로그인 성공')
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS, '환영합니다!')
            return redirect('home')
        else:
            # 로그인 실패
            messages.add_message(request, messages.ERROR, '로그인에 실패하였습니다. 아이디 또는 비밀번호를 확인해주세요.')
            return render(request, 'login.html')

    else:
        return render(request, 'login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.add_message(request, messages.SUCCESS, '성공적으로 로그아웃 되었습니다.')
        return redirect('home')
    return render(request, 'signup.html')