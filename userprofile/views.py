from django.shortcuts import redirect, render
from accounts.models import CustomUser

from userprofile.models import Address, UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from accounts.forms import editprofile
from django.contrib.auth.decorators import login_required


# Create your views here.



def add_address(request):
    if request.method == "POST":
        address = Address()
        address.user=request.user
        address.first_name = request.POST.get('firstname')
        address.last_name = request.POST.get('lastname')
        address.country = request.POST.get('country')
        address.phone = request.POST.get('phone')
        address.email = request.POST.get('email')
        address.address = request.POST.get('address')
        address.pincode = request.POST.get('pincode')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.order_note = request.POST.get('ordernote')
        address.save()
        return redirect('checkout')
    
    return render(request, 'store/checkout.html')

def delete_address(request, address_id):
    
    address =Address.objects.filter(id=address_id)
    address.delete()
    return redirect('checkout')

def profile(request):
    user = request.user
    address = Address.objects.filter(user=user)
    # wallet_balance = Wallet.objects.get(user = user)
    context ={
        'address' : address,
        # 'wallet' : wallet_balance,
    }
    return render(request, 'userprofile/profile_details.html',context)

@login_required(login_url='user_login')
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = editprofile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Replace 'profile' with your actual profile page URL
    else:
        form = editprofile(instance=user)
    
    return render(request, 'userprofile/profile_details.html', {'form': form})
    
  


        
def changepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update the session to prevent the user from being logged out
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('profile')  # Replace 'home' with the appropriate URL name for your home page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        
    return render(request, 'userprofile/profile_details.html', {'form': form})


    
    

        
    





