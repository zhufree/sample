from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from account import Account as Account_
from models import Account, Bar, SignStatus
# Create your views here.


@login_required
def index(request):
    accounts = request.user.user_has_accounts.all()
    for account in accounts:
        if account.uid in request.session:
            pass
        else:
            account_ = Account_(account.uid, account.pwd)
            account_.get_bars()
            request.session[account.uid] = account_.fetch_tieba_info()
            print request.session[account.uid]
    return render(request, 'tieba_index.html', {
        'accounts': accounts,
    })


@csrf_exempt
def get_sign_status(request):
    if request.method == 'POST':
        cur_bar = Bar.objects.get(id=request.POST.get('bar_id'))
        cur_account = Account.objects.get(id=request.POST.get('account_id'))
        cur_sign_status = SignStatus.objects.get(
                 account = cur_account,
                 bar = cur_bar,
             )
        for tieba_info in request.session[cur_account.uid]:
            if tieba_info['name'] == cur_bar.name:
                cur_sign_status.signed = tieba_info['sign_status']
                if tieba_info['sign_status'] != True:
                    print tieba_info['name']
        cur_sign_status.save()
        data = {'sign_status': cur_sign_status.signed}
        return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_protect
def bind(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        pwd = request.POST.get('pwd')
        new_acc = Account.objects.create(
            uid=uid,
            pwd=pwd,
            user=request.user
        )
        new_acc.auto_get_bars()
        new_acc.save()
        return HttpResponseRedirect("/tieba/")

def sign(request):
    pass