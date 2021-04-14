from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>', views.ProjectDetailView, name='project-detail'),
    path('userprofile', views.UserProfileView, name='user-profile'),
    path('myprojects',views.ProjectOfTeamMemberListView.as_view(), name = 'my-projects'),
    path('mybugreports', views.BugreportsOfTeamMemberListView.as_view(),name = 'my-bug-reports'),
    path('bugreport/<uuid:pk>',views.bugreportdetailview,name = 'bugreport-detail'),
    path('allbugreports',views.AllBugreportsListView.as_view(),name = 'all-bug-reports'),
    path('bugreport/new', views.new_bugreport, name = 'new-bugreport'),
    path('predict_severity',views.mlseverity,name = 'predict-severity'),
    path('predict_assignee',views.mlass,name = 'predict-assignee'),
    
]
