"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from apps.contest import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path(route='', view=views.homePage, name="homepage"),
    path(route='sign-up/', view=views.signupTeam, name="signup"),
    path(route="questions/buy/", view=views.buyQuestion, name="buyQuestion"),
    path(route="questions/solve/", view=views.solvedProblem, name="solveProblem"),
    path(route="questions/sell/", view=views.sellQuestion, name="sellQuestion"),
    path(route="questions/wrong-answer-fault/", view=views.wrongAnswerFault, name="wrongAnswerFault"),
    path(route="score-board/", view=views.scoreBoard, name="scoreBoard"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
