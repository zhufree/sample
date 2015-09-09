from django.shortcuts import render
from django.http import HttpResponseRedirect
import json
from account import Account as Account_
from models import Account, Bar, Sign_status
# Create your views here.


def index(request):
    accounts = request.user.user_has_accounts.all()
    for account in accounts:
        account_ = Account_(account.uid, account.pwd)
        account_.get_bars()
        tieba_infos = account_.fetch_tieba_info()
        for tieba_info in tieba_infos:
            # print tieba_info['name']
            cur_bar, dummy = Bar.objects.get_or_create(
                name=tieba_info['name'],
                link=tieba_info['link']
            )
            new_sign_status, dummy = Sign_status.objects.get_or_create(
                account = account,
                bar = cur_bar,
            )
            new_sign_status.signed = tieba_info['sign_status']
            new_sign_status.save()
            cur_bar.bar_sign_status.add(new_sign_status)
            account.account_sign_status.add(new_sign_status)
            cur_bar.save()
            account.save()
            # print new_sign_status
    return render(request, 'tieba_index.html', {
        'accounts': accounts,
    })


def bind(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        pwd = request.POST.get('pwd')
        new_acc = Account.objects.create(
            uid=uid,
            pwd=pwd,
            user=request.user
        )
        bars = Account_(uid, pwd).get_bars()
        for bar in bars:
            new_bar, dummy = Bar.objects.get_or_create(
                name=bar['name'],
                link=bar['link']
            )
            new_bar.save()
            new_acc.bars.add(new_bar)
        new_acc.save()
        return HttpResponseRedirect("/tieba/")

def sign(request):
    pass