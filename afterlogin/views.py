from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import CfpData, AuthorData, ConferenceData, Reviews, Feedback
from datetime import datetime
from django.db.models import Q
import pickle, os
from django.views.decorators.clickjacking import xframe_options_exempt
from django.conf import settings
from urllib.parse import unquote
User = get_user_model()


def CallForPaper(request):
    if request.user.is_authenticated:
        all_papers = CfpData.objects.filter(email=request.user.email)
        data = {'U': request.user.username, 'all_papers': all_papers}
        return render(request, 'callforpaper.html', data)
    messages.error(request, 'You Need To login First')
    return redirect('home')


def CreateCFP(request):
    if request.user.is_authenticated:
        selected = ''
        if request.method == 'GET':
            conference_name = request.GET.get('conference_name')
            if conference_name:
                selected = ConferenceData.objects.get(conference_name=conference_name)
        try:
            if request.method == 'POST':
                conference_name = request.POST.get('conference_name')
                if conference_name == '':
                    raise Exception('Error')
                conference_acronym = request.POST.get('conference_acronym')
                conference_start_date = request.POST.get('conference_start_date')
                conference_end_date = request.POST.get('conference_end_date')
                deadline = request.POST.get('deadline')
                conference_start_date = datetime.strptime(conference_start_date, '%d/%m/%Y')
                conference_end_date = datetime.strptime(conference_end_date, '%d/%m/%Y')
                current = ConferenceData.objects.get(conference_name=conference_name)

                newcfp = CfpData(email=request.user.email, conference_name=conference_name,
                                 conference_acronym=conference_acronym,
                                 conference_start_date=conference_start_date, conference_end_date=conference_end_date,
                                 topic_1=current.topic_1, topic_2=current.topic_2, topic_3=current.topic_3,
                                 topic_4=current.topic_4, deadline=deadline)

                CfpData.save(newcfp)
                return redirect('cfp')
        except:
            messages.error(request, 'Please select All Required Field')
        all_conferences = ConferenceData.objects.all()
        try:
            start = selected.conference_start_date.strftime('%d/%m/%Y')
            end = selected.conference_end_date.strftime('%d/%m/%Y')
        except:
            start = ''
            end = ''

        data = {'U': request.user.username, 'all_conferences': all_conferences, 'selected': selected, 'start': start,
                'end': end}
        return render(request, 'createcfp.html', data)
    messages.error(request, 'You Need To login First')
    return redirect('home')


def DeleteCFP(request, id):
    if request.user.is_authenticated:
        conference_name=unquote(id)
        CfpData.objects.get(conference_name=conference_name).delete()
        return redirect('cfp')
    messages.error(request, 'You Need To login First')
    return redirect('home')


def ViewConference(request, id):
    if request.user.is_authenticated:
        try:
            paper = ConferenceData.objects.get(id=id)
        except:
            id = unquote(id)
            paper = ConferenceData.objects.get(conference_name=id)
        data = {'paper': paper, 'U':request.user.username}
        return render(request, 'viewconference.html', data)
    messages.error(request, 'You Need To login First')
    return redirect('home')


def MyConference(request):
    if request.user.is_authenticated:
        U = request.user.username
        papers = ConferenceData.objects.filter(email=request.user.email)
        data = {'papers':papers,'U':U}
        return render(request,'myconference.html',data)
    messages.error(request, 'You Need To login First')
    return redirect('home')


def CreateConference(request):
    if request.user.is_authenticated:
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
    messages.error(request, 'You Need To login First')
    return redirect('home')


def EditConference(request, id):
    if request.user.is_authenticated:
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
        try:
            papers = ConferenceData.objects.get(id=id)
        except:
            papers = ConferenceData.objects.get(conference_name=id)
        start = papers.conference_start_date
        end = papers.conference_end_date
        start = start.strftime('%d/%m/%Y')
        end = end.strftime('%d/%m/%Y')
        data = {'papers': papers, 'start': start, 'end': end,'U':U}
        return render(request,'editconference.html', data)
    messages.error(request, 'You Need To login First')
    return redirect('home')


def deleteconference(request,name):
    if request.user.is_authenticated:
        try:
            CfpData.objects.get(conference_name=name).delete()
        except:
            pass

        try:
            ConferenceData.objects.get(conference_name=name).delete()
        except:
            pass
        # try:
        #     F = AuthorData.objects.get(conference_name=name)
        #     os.remove(os.path.join(settings.MEDIA_ROOT, str(F.pdf_paper)))
        #     AuthorData.objects.get(conference_name=name).delete()
        # except Exception as E:
        #     print('***********Author')
        #     print(E)
        #     pass
        # try:
        #     Feedback.objects.filter(conference_name=name).delete()
        # except Exception as E:
        #     print('***********Feedback')
        #     print(E)
        #     pass
        # try:
        #     Reviews.objects.filter(conference_name=name).delete()
        # except:
        #     pass
        return redirect('myconference')
    messages.error(request, 'You Need To login First')
    return redirect('home')


def EngineCFP(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            query= request.GET.get('q')
            if query is not None:
                lookups = Q(conference_name__icontains=query) | Q(conference_acronym__icontains=query) |Q(topic_1__icontains=query)| Q(topic_2__icontains=query) | Q(topic_3__icontains=query) | Q(topic_4__icontains=query)
                papers = CfpData.objects.filter(lookups).distinct()
                data = {'papers': papers, 'U':request.user.username}
                return render(request,'enginecfp.html',data)
        papers = CfpData.objects.all()
        data = {'papers': papers, 'U': request.user.username}
        return render(request,'enginecfp.html',data)
    messages.error(request, 'You Need To login First')
    return redirect('home')


def SearchConferece(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            query= request.GET.get('q')
            if query is not None:
                lookups = Q(conference_name__icontains=query) | Q(conference_acronym__icontains=query) | Q(city__icontains=query) | Q(topic_1__icontains=query)| Q(topic_2__icontains=query) | Q(topic_3__icontains=query) | Q(topic_4__icontains=query)
                papers = ConferenceData.objects.filter(lookups).distinct()
                data = {'papers': papers}
                return render(request,'conferencesearch.html', data)
        papers = ConferenceData.objects.all()
        data = {'papers': papers}
        return render(request, 'conferencesearch.html', data)
    messages.error(request, 'You Need To login First')
    return redirect('home')


def reviewer_assignment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('primary_area')
            AuthorData.objects.filter(paper_name=name).update(paper_assigned=True)
            messages.error(request, f'{name} Assigned')
        papers = AuthorData.objects.filter(paper_assigned=False)
        data = {'papers':papers, 'U':request.user.username}
        return render(request, 'reviewer_assignment.html', data)
    messages.error(request, 'You Need To login First')
    return redirect('home')


selected = ''
def conference(request):
    if request.user.is_authenticated:
        global selected
        if request.method == 'POST':
            conference_name = request.GET.get('conference_name')
            print(conference_name)
            if conference_name:
                selected = ConferenceData.objects.get(conference_name=conference_name)
        return redirect('submit-paper')
    messages.error(request, 'You Need To login First')
    return redirect('home')


def SubmitPaper(request):
    if request.user.is_authenticated:
        selected = ''
        U = request.user.username
        all_conferences = []
        call_for_paper_conferences =CfpData.objects.all()
        for i in call_for_paper_conferences:
            all_conferences.append(ConferenceData.objects.get(conference_name=i.conference_name))

        if request.method == 'GET':
            conference_name = request.GET.get('conference_name')
            print(conference_name)
            if conference_name:
                selected = ConferenceData.objects.get(conference_name=conference_name)
                deadline = CfpData.objects.get(conference_name=conference_name)
                deadline = deadline.deadline
        try:
            if request.method == 'POST':
                conference_name = request.POST.get('conference_name')
                author = request.POST.get('author')
                paper_name = request.POST.get('paper_name')
                if conference_name == '':
                    raise Exception('Error')
                co_author_receive = request.POST.get('co_author')
                co_author = pickle.dumps(co_author_receive.split(';'))
                abstract = request.POST.get('abstract')
                deadline = CfpData.objects.get(conference_name=conference_name)
                topics = request.POST.get('topics')
                keyword_receive = request.POST.get('keywords')
                keywords = pickle.dumps(keyword_receive.split(','))
                pdf_paper = request.FILES['pdf']
                email = request.user.email

                data = AuthorData(email=email, conference_name=conference_name, author=author,paper_name=paper_name,
                                  topics=topics,co_author=co_author, abstract=abstract, keywords=keywords, pdf_paper=pdf_paper,
                                  deadline=deadline.deadline)
                AuthorData.save(data)
                return redirect('view-paper')
        except Exception as E:
            messages.error(request,E)

        data = {'U': U, 'all_conferences': all_conferences, 'selected': selected,'deadline':deadline}
        return render(request, 'submitpaper.html', data)
    messages.error(request, 'You Need To login First')
    return redirect('home')


def ViewPaper(request):
    if request.user.is_authenticated:
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
    messages.error(request, 'You Need To login First')
    return redirect('home')


@xframe_options_exempt
def DocumentViewer(request,id):
    if request.user.is_authenticated:
        papers = AuthorData.objects.get(id=id)
        data = {"papers":papers,'U':request.user.username}
        return render(request,'documentviewer.html', data)
    messages.error(request, 'You Need To login First')
    return redirect('home')


def DocumentDelete(request,id):
    if request.user.is_authenticated:
        F = AuthorData.objects.get(id=id)
        os.remove(os.path.join(settings.MEDIA_ROOT, str(F.pdf_paper)))
        AuthorData.objects.get(id=id).delete()
        return redirect('view-paper')
    messages.error(request, 'You Need To login First')
    return redirect('home')


def PaperAssignment(request):
    if request.user.is_authenticated:
        pap = AuthorData.objects.filter(paper_assigned=True, reviewed=False)
        papers = []
        for i in pap:
            Reviewed = Reviews.objects.filter(email=request.user.email, conference_name=i.conference_name)
            if Reviewed:
                pass
            else:
                papers.append(i)
        data = {'papers': papers, 'U':request.user.username}
        return render(request,'paperassignment.html', data)
    messages.error(request, 'You Need To login First')
    return redirect('home')


def review_paper(request,id):
    if request.user.is_authenticated:
        id = unquote(id)
        papers = AuthorData.objects.get(paper_name=id)
        if request.method == 'POST':
            review = request.POST.get('review')
            suggest = request.POST.get('usertype')

            reviewed = Reviews(email=request.user.email, conference_name=papers.conference_name, review=review,
                               paper_name=papers.paper_name, Suggest=suggest)
            Reviews.save(reviewed)
            return redirect('paper-assignment')
        data = {'papers': papers,'U':request.user.username}
        return render(request, 'review_paper.html', data)
    messages.error(request, 'You Need To login First')
    return redirect('home')


def paperReviewed(request):
    if request.user.is_authenticated:
        all_papers_reviewed = AuthorData.objects.filter(reviewed=True)
        # papers = []
        # for i in all_papers_reviewed:
        #     papers.append(CfpData.objects.get(conference_name=i.conference_name))
        data = {'papers': all_papers_reviewed,'U':request.user.username}
        return render(request,'paper_reviewd.html', data)
    messages.error(request, 'You Need To login First')
    return redirect('home')


def ViewReviewed(request, id):
    if request.user.is_authenticated:
        id = unquote(id)
        review = Reviews.objects.get(email=request.user.email, paper_name=id)
        data = {'review':review,'U':request.user.username}
        return render(request, 'view_review.html',data)
    messages.error(request, 'You Need To login First')
    return redirect('home')


def EditReviewed(request, id):
    if request.user.is_authenticated:
        id = unquote(id)
        review = Reviews.objects.get(email=request.user.email, paper_name=id)
        paper = AuthorData.objects.get(paper_name=id)
        if request.method == 'POST':
            re = request.POST.get('review')
            Reviews.objects.filter(email=request.user.email, paper_name=id).update(review=re)
            return redirect('paper-reviewed')
        data = {'review':review,'U':request.user.username, 'paper': paper}
        return render(request, 'edit_review.html',data)
    messages.error(request, 'You Need To login First')
    return redirect('home')


# this is author part
def paperreviewes(request):
    if request.user.is_authenticated:
        all_papers_reviewed = AuthorData.objects.filter(email=request.user.email, reviewed=True)
        data = {'papers': all_papers_reviewed,'U':request.user.username}
        return render(request,'All_reviewd_paper_author_part.html', data)
    messages.error(request, 'You Need To login First')
    return redirect('home')


def FeedBackPost(request, id):
    if request.user.is_authenticated:
        paper = AuthorData.objects.get(paper_name=id)
        try:
            feed = Feedback.objects.get(paper_name=id, email=request.user.email)
            author_feedback = feed.Feedback
        except:
            author_feedback = False
        if request.method == 'POST':
            feedback = request.POST.get('feedback')
            F = Feedback(email=request.user.email, paper_name=paper.paper_name, Feedback=feedback,
                         conference_name=paper.conference_name)
            Feedback.save(F)
            AuthorData.objects.filter(paper_name=id).update(feedback=True)
            return redirect('review-viewer')
        if paper:
            all_papers_reviewed = Reviews.objects.filter(paper_name=paper.paper_name)
            data = {'paper': paper, 'reviews':all_papers_reviewed,'U':request.user.username,
                    'author_feedback':author_feedback}
            return render(request, 'author_feedback.html', data)
    messages.error(request, 'You Need To login First')
    return redirect('home')


# this is for reviewer Author Feedback Part
def Review_Feedback(request):
    if request.user.is_authenticated:
        F = AuthorData.objects.filter(feedback=True)
        data = {'papers': F, 'U':request.user.username}
        return render(request, 'Reviewer_author_feedbck_part.html', data)
    messages.error(request, 'You Need To login First')
    return redirect('home')


def Review_Feedback_Detail(request, id):
    if request.user.is_authenticated:
        id = unquote(id)
        P = AuthorData.objects.get(paper_name=id)
        R = Reviews.objects.filter(paper_name=P.paper_name)
        F = Feedback.objects.filter(paper_name=P.paper_name)
        data = {'paper': P, 'reviews': R, 'feedback': F, 'U':request.user.username}
        return render(request,'view_feedbacl_review.html',data)
    messages.error(request, 'You Need To login First')
    return redirect('home')
