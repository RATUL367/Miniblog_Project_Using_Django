from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm, LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group
# Home
def home(request):
    posts = Post.objects.all()
    return render(request,'miniblog/home.html',{'posts':posts})

# About
def about(request):
    return render(request, 'miniblog/about.html')

# About
def contact(request):
    return render(request, 'miniblog/contact.html')

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        grup = user.groups.all()
        return render(request, 'miniblog/dashboard.html',{'posts':posts,'full_name':full_name,'groups':grup})
    else:
        return HttpResponseRedirect('/login/')

# Signup
def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! You have become an Author')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, 'miniblog/signup.html',{'form':form})

# Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username = uname, password = upass)
                if user is not None:
                    login(request,user)
                    messages.success(request, 'Logged in Successfully!!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'miniblog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
# Add New Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title_v = form.cleaned_data['title']
                desc_v = form.cleaned_data['desc']
                pst = Post(title=title_v, desc=desc_v)
                pst.save()
                messages.success(request, 'Post Added Successfully!!')
                form=PostForm()
        else:
            form = PostForm()
        return  render(request,'miniblog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

# Update Post
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                messages.success(request, 'Post Updated Successfully!!!')
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request,'miniblog/updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')

# Delete Post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method =='POST':
            pi = Post.objects.get(pk = id)
            pi.delete()
            messages.warning(request, 'Post Deleted Successfully!!')
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

# Post Details Page
def post_details(request, id):
    val = Post.objects.get(pk=id)
    data = {
        'post': val,
    }
    return render(request, 'miniblog/postdetails.html', data)

