from django.shortcuts import render
from django.http import HttpResponseRedirect
import json
from account import Account as Account_
from models import Account,Bar
# Create your views here.


def index(request):
    accounts = request.user.user_has_accounts.all()
    '''
    for account in accounts:
        account_ = Account_(account.uid, account.pwd)
        tieba_infos = account_.fetch_tieba_info(account_.get_bars())
        for tieba_info in tieba_infos:
            cur_bar = Bar.objects.get(name=tieba_info['name'])
            #cur_bar.fid = tieba_info['fid']
            #cur_bar.tbs = tieba_info['tbs']
            cur_bar.signed = bool(tieba_info['sign_status'])
            print cur_bar.signed
            cur_bar.save()
            '''
    return render(request, 'tieba_index.html', {'accounts': accounts})


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