from django.shortcuts import render,reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from wallet.models import Wallet,Transaction
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum,Count
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
import datetime
from itertools import chain

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current = Wallet(user = request.user, balance = 0)
            current.save()
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required   
def dashboard(request):
    user = Wallet.objects.get(user=request.user)
    return render(request,'wallet/profile.html',{"user1":user})
   
    
def addmoney(request):
    if request.method == "POST":
        amount = request.POST["amount"]
        User1 = User.objects.get(username=request.user.username)
        money =Wallet.objects.get(user=User1)
        money1=money.balance
        money.balance= money1+int(amount)
        money.save()
        wallet_money =Transaction(sender=request.user,receiver=request.user,amount=amount,timestamp=datetime.datetime.now())
        wallet_money.save()
        return redirect('dashboard')
       
    user = Wallet.objects.get(user=request.user)
    return render(request,'wallet/addmoney.html',{"balance":user.balance})
  

def trasfermoney(request):
    msg=""
    if request.method == "POST":
        try:
            username = request.POST["username"]
            amount = request.POST["amount"]
            senderUser = User.objects.get(username=request.user.username)
            receiverUser =  User.objects.get(username=username)
            sender = Wallet.objects.get(user = senderUser)
            left=sender.balance
            if left < int(amount):
                messages.error(request,'Insufficient funds')
                
                return HttpResponseRedirect(reverse("trasfer"))
              
            receiver = Wallet.objects.get(user = receiverUser)
            sender.balance = sender.balance - int(amount)
            receiver.balance = receiver.balance + int(amount)
            sender.save()
            receiver.save()
            add =Transaction(sender=senderUser,receiver=receiverUser,amount=amount,timestamp=datetime.datetime.now())
            add.save()
            msg = "Transaction Success"
        except Exception as e:
            print(e)
            msg = "Transaction Failure, Please try again"
   
    user = Wallet.objects.get(user=request.user)
    return render(request,'wallet/transfer.html',{"balance":user.balance,"msg":msg})

def passbook(request):
   
    send_money = Transaction.objects.filter(sender=request.user).order_by('-timestamp')
    receive_money = Transaction.objects.filter(receiver=request.user).order_by('-timestamp')
    wallet_money  =Transaction.objects.filter(sender=request.user,receiver=request.user).order_by('-timestamp')
    context ={'send_money':send_money ,'receive_money':receive_money, 'wallet_money':wallet_money}
#     posts = list(
#             sorted(
#                 chain(kk,un),
#                 key=lambda objects: objects.created,
#                 reverse=True  # Optional
#             ))
#     print(posts)        
#     for post in posts:
#         print(post)

#    # print(posts.object_list)
#     paginator = Paginator(posts,5)# 3 posts at single page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         objects = paginator.page(paginator.num_pages)
 #   return render(request,'wallet/tran1.html',{'page':page,'posts':posts})
    return render(request,'wallet/passbook.html',context)
    
  #  return render(request,'tran.html',{"kk":kk})


def addition(request):
   
    current_month=datetime.datetime.now()
    previous_month=current_month-timedelta(days=30)
  
    wallet_add = Transaction.objects.filter(sender=request.user,receiver=request.user,timestamp__gte=previous_month,timestamp__lte=current_month)\
           .annotate(date=TruncMonth('timestamp'))\
           .values('date').annotate(total_sum=Sum('amount'))
    # for re in wallet_add:
    #     p1=re['total_sum'] 
    #     print(p1)
    wallet_receive = Transaction.objects.filter(receiver=request.user,timestamp__gte=previous_month,timestamp__lte=current_month).exclude(sender=request.user)\
            .annotate(date=TruncMonth('timestamp'))\
            .values('date').annotate(total_sum=Sum('amount'))
    # for rec in wallet_receive:
    #     p=rec['total_sum'] 
     
    #wallet_total = p1+p
    wallet_transfer=Transaction.objects.filter(sender=request.user,timestamp__gte=previous_month,timestamp__lte=current_month).exclude(receiver=request.user)\
            .annotate(date=TruncMonth('timestamp'))\
            .values('date').annotate(transfer_sum=Sum('amount'))
   
    return render(request,'wallet/sum.html',{'wallet_add':wallet_add , 'wallet_transfer':wallet_transfer,'wallet_receive': wallet_receive})
   