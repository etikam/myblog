from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth import get_user_model
from .forms import  RegisterForm, LoginForm
from django.contrib import messages

User = get_user_model()
def registerView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Récupérer les données du formulaire
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            is_writer = form.cleaned_data.get('is_writer')
            
            
            if(password!=password2):
                messages.error(request,'les mots de passes saisis ne correspondent pas')
                pass
            else:  # Créer l'utilisateur en utilisant create_user
                user = User.objects.create_user(username=username, 
                                                email=email, 
                                                password=password,
                                                )
                user.first_name = first_name
                user.last_name = last_name
                if is_writer:
                    user.is_writer= True
                
                user.save()
                # Connecter l'utilisateur après la création
                login(request, user)
            
                return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})


def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Connecter l'utilisateur si l'authentification est réussie
                login(request, user)
                return redirect('home')  # Redirige vers la page d'accueil ou une autre page après connexion
            else:
                # Ajouter un message d'erreur si l'authentification échoue
                form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logoutView(request):
    logout(request)
    return redirect('home')