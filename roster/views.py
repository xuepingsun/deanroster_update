from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import DeanBasic,SchoolInfo #Post,UserInput
# from .forms import DeanInfoForm

# def index(request):
#     return HttpResponse('Hello!')

from django.contrib.admin.views.decorators import staff_member_required
# from django.shortcuts import render

@staff_member_required
def admin_index(request, extra_context=None):
    schools = SchoolInfo.objects.all()
    total_deans = DeanBasic.objects.count()
    context = {
        'title': 'School Info Dashboard',
        'schools': schools,
        'total_deans': total_deans,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, 'admin/admin_index.html', context)


#from django.shortcuts import render


# def index(request):
#     # context = {
#     #     'news_list': [
#     #         {
#     #             "title": "图雀写作工具推出了新的版本",
#     #             "content": "随随便便就能写出一篇好教程，真的很神奇",
#     #         },
#     #         {
#     #             "title": "图雀社区正式推出快速入门系列教程",
#     #             "content": "一杯茶的功夫，让你快速上手，绝无担忧",
#     #         },
#     #     ]
#     # }
#
#     # context = { 'dean_list': DeanInfo.objects.all()
#     #             # 'news_list': Post.objects.all(),
#     #             # 'userinput_list':UserInput.objects.all()
#     #             }
#     form = DeanInfoForm()
#     # return render(request, 'roster/index.html', context=context)
#     return render(request, 'roster/deaninfo.html', {'form': form})

# def index(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = DeanInfoForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # # ...
#             # article_title = request.POST.get("article_title", "");
#             # article_prief = request.POST.get("article_prief", "");
#             # article_content = request.POST.get("article_content", "");
#             # dean = DeanInfo(article_title=article_title, article_prief_content=article_prief,
#             #                       article_content=article_content);
#             form.save();
#             # redirect to a new URL:
#             # return HttpResponseRedirect('roster/index.html')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = DeanInfoForm()
#
#     return render(request, 'roster/deaninfo.html', {'form': form})
