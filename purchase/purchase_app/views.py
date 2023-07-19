from django.shortcuts import get_object_or_404, render, redirect
from .forms import RequestModelForm, StateRequestModelForm
from .models import PurchasePlanModel, PurchaseModel, RequestModel, StateRequestModel
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.admin.models import LogEntry


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                auth_views.LoginView.as_view(template_name='login.html')(request)
                return redirect('purchase_app:request_list')
        else:
            form = AuthenticationForm()
        return render(request, 'auth/login.html', {'form': form})
    else:
        return redirect('purchase_app:request_list')


def logout_view(request):
    auth_views.LogoutView.as_view(next_page=reverse('purchase_app:purchase_plans'))(request)
    return redirect('purchase_app:purchase_plans')


def purchase_plans(request):
    purchase_plans = PurchasePlanModel.objects.all()
    context = {
        'purchase_plans': purchase_plans,
        'user': request.user, 
    }
    return render(request, 'purchases/purchase_plans.html', context)


def purchase_details(request, id):
    purchase = PurchaseModel.objects.get(externalId=id)
    context = {
        'purchase': purchase,
    }
    return render(request, 'purchases/purchase_details.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('purchase_app:auth_login'))
    else:
        form = UserCreationForm()
    return render(request, 'auth/sign_up.html', {'form': form})


@login_required
def create_request(request):
    form = RequestModelForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            state_request = StateRequestModel.objects.create(name=StateRequestModel.STATE_CHOICES[0][0])
            request_obj = form.save(commit=False)
            request_obj.user = request.user
            request_obj.state = state_request
            request_obj.save()

            return redirect('purchase_app:request_list')
    
    context = {'form': form}
    return render(request, 'requests/create_request.html', context)



@login_required
def request_list(request):
    requests = RequestModel.objects.filter(user=request.user)
    form = RequestModelForm()
    edit_state_form = StateRequestModelForm()
    context = {'requests': requests, 'form': form, 'edit_state_form': edit_state_form,}
    return render(request, 'requests/request_list.html', context)


@login_required
def edit_request(request, id):
    request_obj = get_object_or_404(RequestModel, id=id, user=request.user)

    if request.method == 'POST':
        form = RequestModelForm(request.POST, instance=request_obj)
        if form.is_valid():
            form.save()
            return redirect('purchase_app:request_list')
    else:
        form = RequestModelForm(instance=request_obj)

    context = {
        'request': request_obj,
        'form': form,
    }
    return render(request, 'requests/edit_request.html', context)


def request_details(request, id):
    request_model = RequestModel.objects.get(id=id)
    log_entries = LogEntry.objects.filter(object_id=id, content_type__model='requestmodel')
    context = {
        'request_model': request_model,
        'log_entries': log_entries,
    }
    return render(request, 'requests/details.html', context)


@login_required
def change_state(request, id):
    request_obj = get_object_or_404(StateRequestModel, id=id,)

    if request.method == 'POST':
        edit_state_form = StateRequestModelForm(request.POST, instance=request_obj)
        if edit_state_form.is_valid():
            edit_state_form.save()
            return redirect('purchase_app:request_list')
    else:
        edit_state_form = StateRequestModelForm(instance=request_obj)

    context = {
        'request': request_obj,
        'edit_state_form': edit_state_form,
    }
    return render(request, 'requests/change_state.html', context)
