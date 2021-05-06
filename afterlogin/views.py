from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import CfpData, AuthorData, ConferenceData, Reviews, Feedback
from datetime import datetime
from django.db.models import Q
import pickle,os
from django.views.decorators.clickjacking import xframe_options_exempt
from django.conf import settings
from django.core.files.storage import FileSystemStorage

User = get_user_model()


def Dashboard(request):
    if request.user.is_authenticated:
        return render(request,'dashboard.html')
    messages.error(request,'You need to login first')
    return redirect('home')


def cfp_suggest(request):
    pass

def CallForPaper(request):
    all_papers = CfpData.objects.filter(email=request.user.email)
    data = {'all_papers': all_papers}
    return render(request,'callforpaper.html', data)


def CreateCFP(request):
    if request.method == 'POST':
        conference_name = request.POST.get('conference_name')
        conference_acronym = request.POST.get('conference_acronym')
        conference_start_date = request.POST.get('conference_start_date')
        conference_end_date = request.POST.get('conference_end_date')
        cfp_abstract_deadlines = request.POST.get('cfp_abstract_deadlines')
        cfp_submission_deadline = request.POST.get('cfp_submission_deadline')
        webpage = request.POST.get('webpage')
        venue = request.POST.get('venue')
        city = request.POST.get('city')
        country_region = request.POST.get('country_region')
        primary_area = request.POST.get('primary_area')
        secondary_area = request.POST.get('secondary_area')
        area_notes = request.POST.get('area_notes')
        document = request.FILES['pdf']
        if area_notes:
            pass
        else:
            area_notes = ''
        topic_1 = request.POST.get('topic_1')
        topic_2 = request.POST.get('topic_2')
        if topic_2:
            pass
        else:
            topic_2 = ''
        topic_3 = request.POST.get('topic_3')
        if topic_3:
            pass
        else:
            topic_3 = ''
        topic_4 = request.POST.get('topic_4')
        if topic_4:
            pass
        else:
            topic_4 = ''
        extra_information = request.POST.get("extra_information")
        if extra_information:
            pass
        else:
            extra_information = ''

        newcfp = CfpData(email=request.user.email,conference_name=conference_name, conference_acronym=conference_acronym,
                         conference_start_date=conference_start_date, conference_end_date=conference_end_date,
                         cfp_abstract_deadlines=cfp_abstract_deadlines, cfp_submission_deadline=cfp_submission_deadline,
                         webpage=webpage, venue=venue, city=city, country_region=country_region,
                         primary_area=primary_area, secondary_area=secondary_area, area_notes=area_notes,
                         topic_1=topic_1,
                         topic_2=topic_2, topic_3=topic_3, topic_4=topic_4, extra_information=extra_information,document=document)
        CfpData.save(newcfp)
        return redirect('cfp')
    return render(request,'createcfp.html')


def EditCFP(request, id):
    if request.method == 'POST':
        conference_name = request.POST.get('conference_name')
        conference_acronym = request.POST.get('conference_acronym')
        conference_start_date = request.POST.get('conference_start_date')
        conference_start_date = datetime.strptime(conference_start_date, '%d/%m/%Y')
        conference_end_date = request.POST.get('conference_end_date')
        conference_end_date = datetime.strptime(conference_end_date, '%d/%m/%Y')
        cfp_abstract_deadlines = request.POST.get('cfp_abstract_deadlines')
        cfp_abstract_deadlines = datetime.strptime(cfp_abstract_deadlines, '%d/%m/%Y')
        cfp_submission_deadline = request.POST.get('cfp_submission_deadline')
        cfp_submission_deadline = datetime.strptime(cfp_submission_deadline, '%d/%m/%Y')
        webpage = request.POST.get('webpage')
        venue = request.POST.get('venue')
        city = request.POST.get('city')
        country_region = request.POST.get('country_region')
        primary_area = request.POST.get('primary_area')
        secondary_area = request.POST.get('secondary_area')
        area_notes = request.POST.get('area_notes')
        if area_notes:
            pass
        else:
            area_notes = ''
        topic_1 = request.POST.get('topic_1')
        topic_2 = request.POST.get('topic_2')
        if topic_2:
            pass
        else:
            topic_2 = ''
        topic_3 = request.POST.get('topic_3')
        if topic_3:
            pass
        else:
            topic_3 = ''
        topic_4 = request.POST.get('topic_4')
        if topic_4:
            pass
        else:
            topic_4 = ''
        extra_information = request.POST.get("extra_information")
        if extra_information:
            pass
        else:
            extra_information = ''

        CfpData.objects.filter(id=id).update(email=request.user.email, conference_name=conference_name, conference_acronym=conference_acronym,
                         conference_start_date=conference_start_date, conference_end_date=conference_end_date,
                         cfp_abstract_deadlines=cfp_abstract_deadlines, cfp_submission_deadline=cfp_submission_deadline,
                         webpage=webpage, venue=venue, city=city, country_region=country_region,
                         primary_area=primary_area, secondary_area=secondary_area, area_notes=area_notes,
                         topic_1=topic_1,
                         topic_2=topic_2, topic_3=topic_3, topic_4=topic_4, extra_information=extra_information,)
        return redirect('cfp')
    paper = CfpData.objects.get(id=id)
    start = paper.conference_start_date
    end = paper.conference_end_date
    abstract_deadlines = paper.cfp_abstract_deadlines
    submission_deadline = paper.cfp_submission_deadline
    start = start.strftime('%d/%m/%Y')
    end = end.strftime('%d/%m/%Y')
    abstract_deadlines = abstract_deadlines.strftime('%d/%m/%Y')
    submission_deadline = submission_deadline.strftime('%d/%m/%Y')
    data = {'paper': paper, 'start': start, 'end': end, 'abstract_deadlines': abstract_deadlines,
            'submission_deadline': submission_deadline}
    return render(request,'editcfp.html', data)


def ViewCFP(request, id):
    paper = CfpData.objects.get(id=id)
    data = {'paper': paper}
    return render(request,'viewcfp.html', data)

def ViewConference(request, id):
    paper = ConferenceData.objects.get(id=id)
    data = {'paper': paper, 'U':request.user.username}
    return render(request,'viewconference.html', data)


def MyConference(request):
    U = request.user.username
    papers = ConferenceData.objects.filter(email=request.user.email)
    data = {'papers':papers,'U':U}
    return render(request,'myconference.html',data)


def CreateConference(request):
    U = request.user.username

    conference_name = request.POST.get('conference_name')
    conference_acronym = request.POST.get('conference_acronym')
    conference_start_date = request.POST.get('conference_start_date')
    conference_end_date = request.POST.get('conference_end_date')
    organizer = request.POST.get('organizer')
    organizer_webpage = request.POST.get('organizer_webpage')
    webpage = request.POST.get('webpage')
    venue = request.POST.get('venue')
    city = request.POST.get('city')
    country_region = request.POST.get('country_region')
    primary_area = request.POST.get('primary_area')
    secondary_area = request.POST.get('secondary_area')
    area_notes = request.POST.get('area_notes')

    if request.method == 'POST':
        if area_notes:
            pass
        else:
            area_notes = ''
        topic_1 = request.POST.get('topic_1')
        topic_2 = request.POST.get('topic_2')
        if topic_2:
            pass
        else:
            topic_2 = ''
        topic_3 = request.POST.get('topic_3')
        if topic_3:
            pass
        else:
            topic_3 = ''
        topic_4 = request.POST.get('topic_4')
        if topic_4:
            pass
        else:
            topic_4 = ''
        extra_information = request.POST.get("extra_information")
        if extra_information:
            pass
        else:
            extra_information = ''

        conference_data = ConferenceData(email = request.user.email, conference_name = conference_name,
                                         conference_acronym = conference_acronym,
                                         conference_start_date = conference_start_date,
                                         conference_end_date =conference_end_date, organizer = organizer,
                                         organizer_webpage = organizer_webpage, webpage = webpage,
                                         venue = venue, city = city, country_region = country_region,
                                         primary_area = primary_area, secondary_area = secondary_area,
                                         area_notes = area_notes,
                                         topic_1 = topic_1, topic_2 = topic_2,
                                         topic_3 = topic_3, topic_4 = topic_4, extra_information = extra_information)
        ConferenceData.save(conference_data)
        return redirect('myconference')
    data = {'U':U}
    return render(request,'createconference.html', data)


def EditConference(request, id):
    U = request.user.username
    if request.method == 'POST':
        conference_name = request.POST.get('conference_name')
        conference_acronym = request.POST.get('conference_acronym')
        conference_start_date = request.POST.get('conference_start_date')
        conference_start_date = datetime.strptime(conference_start_date, '%d/%m/%Y')
        conference_end_date = request.POST.get('conference_end_date')
        conference_end_date = datetime.strptime(conference_end_date, '%d/%m/%Y')
        organizer = request.POST.get('organizer')
        organizer_webpage = request.POST.get('organizer_webpage')
        webpage = request.POST.get('webpage')
        venue = request.POST.get('venue')
        city = request.POST.get('city')
        country_region = request.POST.get('country_region')
        primary_area = request.POST.get('primary_area')
        secondary_area = request.POST.get('secondary_area')
        area_notes = request.POST.get('area_notes')
        if area_notes:
            pass
        else:
            area_notes = ''
        topic_1 = request.POST.get('topic_1')
        topic_2 = request.POST.get('topic_2')
        if topic_2:
            pass
        else:
            topic_2 = ''
        topic_3 = request.POST.get('topic_3')
        if topic_3:
            pass
        else:
            topic_3 = ''
        topic_4 = request.POST.get('topic_4')
        if topic_4:
            pass
        else:
            topic_4 = ''
        extra_information = request.POST.get("extra_information")
        if extra_information:
            pass
        else:
            extra_information = ''
        ConferenceData.objects.filter(id=id).update(email = request.user.email, conference_name = conference_name,
                                         conference_acronym = conference_acronym,
                                         conference_start_date = conference_start_date,
                                         conference_end_date =conference_end_date, organizer = organizer,
                                         organizer_webpage = organizer_webpage, webpage = webpage,
                                         venue = venue, city = city, country_region = country_region,
                                         primary_area = primary_area, secondary_area = secondary_area,
                                         area_notes = area_notes,
                                         topic_1 = topic_1, topic_2 = topic_2,
                                         topic_3 = topic_3, topic_4 = topic_4,
                                         extra_information = extra_information)
        return redirect('myconference')
    papers = ConferenceData.objects.get(id=id)
    start = papers.conference_start_date
    end = papers.conference_end_date
    start = start.strftime('%d/%m/%Y')
    end = end.strftime('%d/%m/%Y')
    data = {'papers': papers, 'start': start, 'end': end,'U':U}
    return render(request,'editconference.html', data)


def EngineCFP(request):
    if request.method == 'GET':
        query= request.GET.get('q')
        if query is not None:
            lookups = Q(conference_name__icontains=query) | Q(conference_acronym__icontains=query) | Q(city__icontains=query) | Q(topic_1__icontains=query)| Q(topic_2__icontains=query) | Q(topic_3__icontains=query) | Q(topic_4__icontains=query)
            papers = CfpData.objects.filter(lookups).distinct()
            data = {'papers': papers}
            return render(request,'enginecfp.html',data)
    papers = CfpData.objects.all()
    data = {'papers':papers}
    return render(request,'enginecfp.html',data)

def SearchConferece(request):
    if request.method == 'GET':
        query= request.GET.get('q')
        if query is not None:
            lookups = Q(conference_name__icontains=query) | Q(conference_acronym__icontains=query) | Q(city__icontains=query) | Q(topic_1__icontains=query)| Q(topic_2__icontains=query) | Q(topic_3__icontains=query) | Q(topic_4__icontains=query)
            papers = ConferenceData.objects.filter(lookups).distinct()
            data = {'papers': papers}
            return render(request,'conferencesearch.html',data)
    papers = ConferenceData.objects.all()
    data = {'papers':papers}
    return render(request,'conferencesearch.html',data)


def reviewer_assignment(request):
    if request.method == 'POST':
        name = request.POST.get('primary_area')
        CfpData.objects.filter(conference_name=name).update(paper_assigned=True)
        messages.error(request, f'{name} Assigned')
    papers = CfpData.objects.filter(email=request.user.email,paper_assigned=False)
    data = {'papers':papers}
    return render(request, 'reviewer_assignment.html', data)


def AuthorDashboard(request):
    return render(request,'dashboard_author.html')


selected = ''


def conference(request):
    global selected
    if request.method == 'POST':
        conference_name = request.GET.get('conference_name')
        print(conference_name)
        if conference_name:
            selected = ConferenceData.objects.get(conference_name=conference_name)
    return redirect('submit-paper')


def SubmitPaper(request):
    selected = ''
    U = request.user.username
    all_conferences = ConferenceData.objects.all()
    if request.method == 'GET':
        conference_name = request.GET.get('conference_name')
        print(conference_name)
        if conference_name:
            selected = ConferenceData.objects.get(conference_name=conference_name)
    if request.method == 'POST':
        conference_name = request.POST.get('conference_name')
        author = request.POST.get('author')
        paper_name = request.POST.get('paper_name')
        co_author_receive = request.POST.get('co_author')
        co_author = pickle.dumps(co_author_receive.split(';'))
        abstract = request.POST.get('abstract')
        topics = request.POST.get('topics')
        keyword_receive = request.POST.get('keywords')
        keywords = pickle.dumps(keyword_receive.split(','))
        pdf_paper = request.FILES['pdf']
        email = request.user.email
        data = AuthorData(email=email, conference_name=conference_name, author=author,paper_name=paper_name,
                          topics=topics,co_author=co_author, abstract=abstract, keywords=keywords, pdf_paper=pdf_paper)
        AuthorData.save(data)
        return redirect('view-paper')
    data = {'U': U, 'all_conferences': all_conferences, 'selected': selected}
    return render(request, 'submitpaper.html', data)


def ViewPaper(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query is not None:
            lookups = Q(topics__icontains=query) | Q(conference_name__icontains=query) | Q(paper_name__icontains=query) | Q(author__icontains=query)
            papers = AuthorData.objects.filter(lookups,email=request.user.email).distinct()
            data = {'papers': papers}
            return render(request, 'viewpaper.html', data)
    papers = AuthorData.objects.filter(email=request.user.email)
    data = {'papers': papers,'U':request.user.username}
    return render(request,'viewpaper.html', data)


@xframe_options_exempt
def DocumentViewer(request,id):
    papers = AuthorData.objects.get(id=id)
    data = {"papers":papers,'U':request.user.username}
    return render(request,'documentviewer.html', data)

def DocumentDelete(request,id):
    F = AuthorData.objects.get(id=id)
    os.remove(os.path.join(settings.MEDIA_ROOT, str(F.pdf_paper)))
    AuthorData.objects.get(id=id).delete()
    return redirect('view-paper')

def ReviewerDashboard(request):
    return render(request,'dashboard_reviewer.html')


def PaperAssignment(request):
    pap = CfpData.objects.filter(paper_assigned=True)
    papers = []
    for i in pap:
        Reviewed = Reviews.objects.filter(email=request.user.email, conference_name=i.conference_name)
        if Reviewed:
            pass
        else:
            papers.append(i)
    data = {'papers': papers}
    return render(request,'paperassignment.html', data)


def review_paper(request,id):
    papers = CfpData.objects.get(id=id)
    if request.method == 'POST':
        review = request.POST.get('review')
        suggest = request.POST.get('usertype')

        reviewed = Reviews(email=request.user.email, conference_acronym=papers.conference_acronym, review=review,
                           conference_name=papers.conference_name, Suggest=suggest)
        Reviews.save(reviewed)
        return redirect('paper-assignment')
    data = {'papers': papers}
    return render(request, 'review_paper.html', data)


def paperReviewed(request):
    all_papers_reviewed = Reviews.objects.filter(email=request.user.email)
    papers = []
    for i in all_papers_reviewed:
        papers.append(CfpData.objects.get(conference_name=i.conference_name))
    data = {'papers': papers}
    return render(request,'paper_reviewd.html', data)


def ViewReviewed(request, id):
    paper = CfpData.objects.get(id=id)
    review = Reviews.objects.get(email=request.user.email,conference_name=paper.conference_name)
    data = {'review':review}
    return render(request, 'view_review.html',data)


def EditReviewed(request, id):
    paper = CfpData.objects.get(id=id)
    review = Reviews.objects.get(email=request.user.email,conference_name=paper.conference_name)
    if request.method == 'POST':
        re = request.POST.get('review')
        Reviews.objects.filter(email=request.user.email,conference_name=paper.conference_name).update(review=re)
        return redirect('paper-reviewed')
    data = {'review':review,'paper':paper}
    return render(request, 'edit_review.html',data)


# this is author part
def paperreviewes(request):
    all_papers_reviewed = Reviews.objects.filter(email=request.user.email)
    papers = []
    for i in all_papers_reviewed:
        Paper = CfpData.objects.get(conference_name=i.conference_name)
        Check = Feedback.objects.filter(conference_name=Paper.conference_name)
        if Check:
            pass
        else:
            papers.append(Paper)
    # if request.method == 'GET':
    #     query= request.GET.get('q')
    #     if query is not None:
    #         lookups = Q(conference_name__icontains=query) | Q(conference_acronym__icontains=query) | Q(city__icontains=query)
    #         pap = []
    #         for i in papers:
    #             paper = i.(lookups).distinct()
    #             pap.append(paper)
    #         data = {'papers': pap}
    #         return render(request, 'All_reviewd_paper_author_part.html', data)

    data = {'papers': papers}
    return render(request,'All_reviewd_paper_author_part.html', data)


def FeedBackPost(request, id):
    paper = CfpData.objects.get(id=id)
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        F = Feedback(email=request.user.email, conference_acronym=paper.conference_acronym, Feedback=feedback,
                conference_name=paper.conference_name)
        Feedback.save(F)
        return redirect('review-viewer')
    if paper:
        all_papers_reviewed = Reviews.objects.filter(conference_name=paper.conference_name)
        data = {'paper': paper, 'reviews':all_papers_reviewed}
        return render(request, 'author_feedback.html', data)
    return render(request, 'author_feedback.html')


# this is for reviewer Author Feedback Part
def Review_Feedback(request):
    F = CfpData.objects.all()
    papers = []
    for i in F:
        j = Feedback.objects.filter(conference_name=i.conference_name)
        if j:
            papers.append(i)
    data = {'papers': papers}
    return render(request, 'Reviewer_author_feedbck_part.html', data)


def Review_Feedback_Detail(request, id):
    P = CfpData.objects.get(id=id)
    R = Reviews.objects.filter(conference_name=P.conference_name)
    F = Feedback.objects.filter(conference_name=P.conference_name)
    data = {'paper': P, 'reviews': R, 'feedback': F}
    return render(request,'view_feedbacl_review.html',data)

