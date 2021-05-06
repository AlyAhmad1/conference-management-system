from django.urls import path
from . import views

urlpatterns = [
    # cfp manager
    path('chair-dashboard/',views.Dashboard, name='dashboard'),
    path('call-for-paper/',views.CallForPaper, name='cfp'),
    path('create-cfp/',views.CreateCFP, name='createcfp'),
    path('edit-cfp/<int:id>',views.EditCFP, name='editcfp'),
    path('view-cfp/<int:id>',views.ViewCFP, name='viewcfp'),
    path('view-conference/<int:id>', views.ViewConference,name='viewconference'),
    path('my-conference/', views.MyConference,name='myconference'),
    path('create-conference/', views.CreateConference,name='createconference'),
    path('edit-conference/<int:id>', views.EditConference, name='editconference'),
    path('engine-cfp', views.EngineCFP, name='enginecfp'),
    path('Search-conference/', views.SearchConferece, name='searchconferece'),
    path('reviewer-assignment/', views.reviewer_assignment, name='reviewerassigment'),

    #author
    path('dashboard-author/', views.AuthorDashboard,name='dashboard-author'),
    path('submit-paper/', views.SubmitPaper,name='submit-paper'),
    path('view-paper/', views.ViewPaper,name='view-paper'),
    path('document-viewer/<id>', views.DocumentViewer,name='document-viewer'),
    path('delete-document/<id>', views.DocumentDelete,name='delete-document'),
    path('review-viewer/', views.paperreviewes,name='review-viewer'),
    path('author-feedback/<int:id>', views.FeedBackPost, name='author-feedback'),

    # reviewer
    path('reviewer-dashboard/',views.ReviewerDashboard,name='reviewer-dashboard'),
    path('paper-assignment/',views.PaperAssignment,name='paper-assignment'),
    path('review-paper/<int:id>', views.review_paper, name='review-paper'),
    path('paper-reviewed/',views.paperReviewed,name='paper-reviewed'),
    path('view-review/<int:id>',views.ViewReviewed,name='view-review'),
    path('edit-review/<int:id>',views.EditReviewed,name='edit-review'),
    path('edit-review/', views.EditReviewed,name='edit-review'),
    path('Review-Feedback/', views.Review_Feedback,name='Review_Feedback'),
    path('Detailed-Review-Feedback/<int:id>', views.Review_Feedback_Detail, name='Detailed_Review_Feedback'),

    # get selected conference
    path('conf/', views.conference, name='conf')
]

