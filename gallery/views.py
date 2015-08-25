from django.shortcuts import render
from sevencow import Cow
# Create your views here.

cow = Cow('d5b6TAk1F2C76Xh-zfwwz7tXf0kX9YWqqPT4_r_w', 'x8flDKcJy-i_LGfjaI8ukUk0iGTepTw_hDFgDTY7')
b = cow.get_bucket('dogegeek')

def index(request):
    return render(request, 'gallery_index.html')