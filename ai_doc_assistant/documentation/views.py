from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import RegisterForm, CodeFileForm
from .models import CodeFile
from .utils import generate_documentation

def home(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = CodeFileForm(request.POST, request.FILES)
        if form.is_valid():
            code_file = form.save(commit=False)
            code_file.user = request.user
            code_file.save()
            return redirect('file_list')
    else:
        form = CodeFileForm()
    return render(request, 'upload.html', {'form': form})

@login_required
def file_list(request):
    files = CodeFile.objects.filter(user=request.user)
    return render(request, 'file_list.html', {'files': files})

@login_required
def delete_file(request, file_id):
    file = get_object_or_404(CodeFile, id=file_id, user=request.user)
    file.delete()
    return redirect('file_list')

@login_required
def generate_docs(request, file_id):
    code_file = get_object_or_404(CodeFile, pk=file_id)
    with open(code_file.file.path, 'r') as file:
        code_content = file.read()
    documentation = generate_documentation(code_content)
    return render(request, 'documentation.html', {'code_file': code_file, 'documentation': documentation})
