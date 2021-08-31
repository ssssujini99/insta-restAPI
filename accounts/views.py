from django.contrib.auth import authenticate, login # authenticate:인증관련
from django.shortcuts import redirect, render
from django.contrib.auth import logout as django_logout
from .forms import SignupForm, LoginForm # 회원가입폼, 로그인폼

# Create your views here.

def signup(request): # 회원가입
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect('accounts:login') # accounts의 login으로 redirect하기
    else: # get 요청일때
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_check(request): # 로그인
    if request.method == "POST":
        form = LoginForm(request.POST)
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        
        user = authenticate(username=name, password=pwd)
        
        if user is not None: # user가 데이터베이스에 있다면
            login(request, user) # 장고가 제공하는 기능 login
            return redirect("/")
        else:
            return render(request, 'accounts/login_fail_info.html')
    else: ## request.method != "GET"
        form = LoginForm() # 다시 로그인 시도
        return render(request, 'accounts/login.html', {"form": form})
    
    
def logout(request): # 로그아웃
    django_logout(request) # 장고에서 제공
    return redirect("/")
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    