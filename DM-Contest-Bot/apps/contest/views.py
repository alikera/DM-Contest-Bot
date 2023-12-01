from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from http import HTTPStatus
from django.http import HttpResponse
from .forms import (signupForm, BuyQuestionForm,
                    SolvedProblemForm, sellQuestionForm,
                    WrongQuestionFaultForm)
from .repos import ScoreRepository

@require_http_methods(["GET"])
def homePage(request) -> HttpResponse:
    return render(
        request=request,
        template_name='index.html',
        status=HTTPStatus.OK)

@require_http_methods(["GET", "POST"])
def signupTeam(request):
    form = signupForm()
    if request.method == "GET":
        return render(
            request=request,
            template_name="signup.html",
            context={
                "form" : form,
            },
            status=HTTPStatus.OK
        )
    
    if request.method == "POST":
        form = signupForm(request.POST)

        if form.is_valid:
            form.save()

            return redirect("homepage")
        
        return render(
            request=request,
            template_name="signup.html",
            context={
                "form" : form,
            }
        )

@require_http_methods(["GET", "POST"])
def buyQuestion(request):
    form = BuyQuestionForm()
    if request.method == "GET":
        return render(
            request=request,
            template_name="buy_question.html",
            context={
                "form" : form,
            },
            status=HTTPStatus.OK
        )
    
    if request.method == "POST":
        form = BuyQuestionForm(request.POST)

        if form.is_valid:
            form.execute(form["teamName"].value(), form["difficultyLevel"].value())

            return render(
                request=request,
                template_name="buy_question.html",
                context={
                    "form" : form,
                    "isBuyed" : True,
                },
                status=HTTPStatus.OK
            )

@require_http_methods(["GET", "POST"])
def solvedProblem(request):
    form = SolvedProblemForm()

    if request.method == "GET":
        return render(
            request=request,
            template_name='solved_question.html',
            context = {"form" : form,},
            status=HTTPStatus.OK
        )
    
    if request.method == "POST":
        form = SolvedProblemForm(request.POST)

        if form.is_valid:
            form.execute(form["team"].value(), form["question"].value())

            return render(
                request=request,
                template_name="solved_question.html",
                context={
                    "form" : form,
                    "is_finished_process": True,
                },
                status=HTTPStatus.OK
            )

@require_http_methods(["GET", "POST"])
def sellQuestion(request):
    form = sellQuestionForm()

    if request.method == "GET":
        return render(
            request=request,
            template_name='sell_question.html',
            context= {"form" : form,},
            status=HTTPStatus.OK
        )
    
    if request.method == "POST":
        form = sellQuestionForm(request.POST)

        if form.is_valid:
            form.execute(form["team"].value(), form["question"].value())

            return render(
                request=request,
                template_name="sell_question.html",
                context={
                    "form" : form,
                    "is_finished_process": True,
                },
                status=HTTPStatus.OK
            )

@require_http_methods(["GET"])
def scoreBoard(request):
    scores = ScoreRepository.getAll()

    return render(
        request=request,
        template_name="score_board.html",
        context={"scores": scores,},
        status=HTTPStatus.OK,
    )

@require_http_methods(["GET", "POST"])
def wrongAnswerFault(request):
    form = WrongQuestionFaultForm()

    if request.method == "GET":
        return render(
            request=request,
            template_name='wrong_question_fault.html',
            context= {"form" : form,},
            status=HTTPStatus.OK
        )
    
    if request.method == "POST":
        form = WrongQuestionFaultForm(request.POST)

        if form.is_valid:
            form.execute(form["team"].value())

            return render(
                request=request,
                template_name="wrong_question_fault.html",
                context={
                    "form" : form,
                    "is_finished_process": True,
                },
                status=HTTPStatus.OK
            )   
