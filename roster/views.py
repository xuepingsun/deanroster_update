from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Post,UserInput

# def index(request):
    # return HttpResponse('Hello World!')from django.shortcuts import render


def index(request):
    # context = {
    #     'news_list': [
    #         {
    #             "title": "图雀写作工具推出了新的版本",
    #             "content": "随随便便就能写出一篇好教程，真的很神奇",
    #         },
    #         {
    #             "title": "图雀社区正式推出快速入门系列教程",
    #             "content": "一杯茶的功夫，让你快速上手，绝无担忧",
    #         },
    #     ]
    # }

    context = { 'news_list': Post.objects.all(),
                'userinput_list':UserInput.objects.all()}
    return render(request, 'roster/index.html', context=context)
