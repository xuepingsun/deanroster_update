from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import DeanBasic,SchoolInfo,DeanCV,Deanedu #Post,UserInput
# from .forms import DeanInfoForm

# def index(request):
#     return HttpResponse('Hello!')
#
# from django.contrib.admin.views.decorators import staff_member_required
# # from django.shortcuts import render
#
# @staff_member_required
# def admin_index(request, extra_context=None):
#     schools = SchoolInfo.objects.all()
#     total_deans = DeanBasic.objects.count()
#     context = {
#         'title': 'School Info Dashboard',
#         'schools': schools,
#         'total_deans': total_deans,
#     }
#     if extra_context is not None:
#         context.update(extra_context)
#     return render(request, 'admin/admin_index.html', context)
#

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

from django.shortcuts import render
from django.db.models import Count, Q
from .models import SchoolInfo, DeanBasic
from .reference_list import university_pilot_list
# from .models import DeanInfo


current_university_names=[uni[1] for uni in university_pilot_list]

def school_completeness_view(request):
    # Define the range of years for coverage
    start_year = 2006
    end_year = 2024
    total_years = end_year - start_year + 1
    total_fields_per_year = 2  # Number of fields to check per year


    # Query all schools and annotate completeness statistics
    schools = SchoolInfo.objects.filter(university__in=current_university_names).annotate(
        total_deans=Count("deanbasic"),
        # total_valid_names=Count("deanbasic", filter=Q(deanbasic__name_last__isnull=False) & Q(deanbasic__name_first__isnull=False)),
        # total_valid_gender=Count("deanbasic", filter=~Q(deanbasic__gender='')),
        # total_valid_birth_year=Count("deanbasic", filter=~Q(deanbasic__birth_year_mon='0000')),
        # total_valid_start_year=Count("deanbasic", filter=~Q(deanbasic__st_year_mon='0000')),
        # total_valid_end_year=Count("deanbasic", filter=~Q(deanbasic__end_year_mon='0000')),
        # total_valid_edu_url=Count("deanbasic", filter=~Q(deanbasic__edu_background_url='')),
        # total_valid_cv_url=Count("deanbasic", filter=~Q(deanbasic__CV_string_url=''))
    )

    # Prepare the completeness data for each school
    school_data = []
    for school in schools:
    # Get all deans for the school
        deans = DeanBasic.objects.filter(university_school=school)

        # Initialize total and valid counters
        valid_count = 0
        total_count = total_years * total_fields_per_year

        # Check completeness for each dean
        for dean in deans:
            try:
                # Get the start and end years for this dean's appointment
                st_year = int(dean.st_year_mon[:4]) if dean.st_year_mon and dean.st_year_mon != '0000' else None
                end_year = int(dean.end_year_mon[:4]) if dean.end_year_mon and dean.end_year_mon != '0000' else None
            except ValueError:
                continue  # Skip invalid dates

            # Only count years within the valid range
            if st_year and end_year:
                            # Determine if the dean has valid CV information
                has_valid_cv = DeanCV.objects.filter(dean_info=dean).exclude(
                        job_st_year_mon__isnull=True
                    ).exclude(
                        job_st_year_mon=''
                    ).exclude(
                        job_st_year_mon='0000'
                    ).count() > 0
                has_phd_info= Deanedu.objects.filter(dean_info=dean, edu_degree='phd').count()>0

                for year in range(max(st_year, start_year), min(end_year + 1, end_year)):
                    # Check if dean's fields are complete for this year
                    # if dean.name_first and dean.name_last and dean.st_year_mon != '0000':
                        if has_phd_info:
                            valid_count += 1
                        if has_valid_cv:
                            valid_count += 1

        # Calculate completeness score
        completeness_percentage = (valid_count / total_count) if total_count > 0 else 0

        school_data.append({
            "school_name": school.school,
            "university_name": school.university,
            "total_deans": school.total_deans,
            "completeness_percentage": round(completeness_percentage, 2),
        })

    return render(request, "school_completeness.html", {"school_data": school_data})
