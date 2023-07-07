from django.shortcuts import render, redirect
from .forms import RequestModelForm
from .models import PurchasePlanModel, PurchaseModel, RequestModel
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                auth_views.LoginView.as_view(template_name='login.html')(request)
                return redirect('purchase_app:request_list')
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
    else:
        return redirect('purchase_app:request_list')


def logout_view(request):
    auth_views.LogoutView.as_view(next_page=reverse('purchase_app:index'))(request)
    return redirect('purchase_app:index')


def index(request):
    purchase_plans = PurchasePlanModel.objects.all()
    context = {
        'purchase_plans': purchase_plans,
        'user': request.user,  # Pass the user object to the template context
    }
    return render(request, 'index.html', context)


def purchase_details(request, id):
    purchase = PurchaseModel.objects.get(externalId=id)
    context = {
        'purchase': purchase,
    }
    return render(request, 'purchase_details.html', context)


@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestModelForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.user = request.user
            request_obj.save()
            return redirect('purchase_app:request_list')
    else:
        form = RequestModelForm()
    return render(request, 'create_request.html', {'form': form})


@login_required
def request_list(request):
    requests = RequestModel.objects.filter(user=request.user)  # Filter requests by the logged-in user
    return render(request, 'request_list.html', {'requests': requests})


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('purchase_app:auth_login'))
    else:
        form = UserCreationForm()
    return render(request, 'sign_up.html', {'form': form})
