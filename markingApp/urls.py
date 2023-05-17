"""django_Marking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from .views import *
from . import views

urlpatterns = [
    path('', views.home, name ='marking-home'),
    path('create/', assignmentCreateView.as_view(), name ='marking-create'),
    path('view/', submissionCreateView.as_view(), name ='marking-view'),
    path('mark/', markListView.as_view(), name ='marking-mark'),
    path('mark/createFeedback/<int:pk>', views.feedbackCreateView , name ='feedback-create'),
    path('assignments/', views.assignments, name ='assignment-view'),
    path('<int:pk>/edit/', assignmentEditView.as_view(), name ='marking-edit'),
    path('<int:pk>/delete/', assignmentDeleteView.as_view(), name ='marking-delete'),
    path('createCriteria/<int:pk>', criteriaCreateView.as_view(), name ='criteria-create'),
    path('view/<int:pk>', submissionDetailView.as_view(), name ='submission-detail'),
    path('view-pdf/<int:pk>', views.view_pdf, name='view-pdf'),
    path('createCriteriaLevel/<int:pk>', criteriaLevelCreateView.as_view(), name='level-create'),
    path('calculateMark/', views.calculateMark, name ='calculate-mark'),



]
