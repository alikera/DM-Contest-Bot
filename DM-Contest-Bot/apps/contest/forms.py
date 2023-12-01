from typing import Any
from django import forms
from .models import (TeamEntity, ScoresEntity, 
                     QuestionsHardnessConfigurationEntity, QuestionStatusEntity)

from .repos import (TeamRepository, QuestionStatusRepository,
                    QuestionRepository, QuestionHardnessConfigurationRepository,
                    ScoreRepository)
from random import choice
from .tasks import send_buy_question_mail_task

class signupForm(forms.ModelForm):
    class Meta:
        model = TeamEntity
        fields = ["name", "email",]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name',
                }),
            'email': forms.EmailInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Email',
                })
        }
    

    def save(self, commit: bool = ...) -> Any:
        newTeam = super().save(commit)
        ScoresEntity.objects.create(team=newTeam)
        return newTeam

class BuyQuestionForm(forms.Form):

    difficultyLevel = forms.ChoiceField(
        choices=QuestionsHardnessConfigurationEntity.ALL_LEVELS,
        required=True,
        label="Dificulty Level",
    )

    teamName = forms.ChoiceField(
        choices=TeamRepository.getAllTeamNames,
        required=True,
        label='Team Name',
    )

    @classmethod
    def execute(self, teamId: int, dificultyLevelId: int):
        if not self.is_valid:
            return
        
        cost = QuestionHardnessConfigurationRepository.getCost(dificultyLevelId)
        
        team = TeamRepository.getById(teamId)

        if team.budget < cost:
            return
        
        seenQuestionIds = QuestionStatusRepository.getTeamSeenQuestionIds(teamId=teamId)
        unSeenQuestionIds = list(QuestionRepository.getUnseenQuestionsByDifficultyLevelIds(
            seenQuestionIds=seenQuestionIds, difficultiyLevelId=dificultyLevelId))
        question = QuestionRepository.getById(choice(unSeenQuestionIds)["id"])
        
        QuestionStatusEntity.objects.create(
            team=team,
            question=question,
            status="b"
        )

        TeamEntity.objects.update(budget = (team.budget - cost))

        send_buy_question_mail_task.delay(team.email, team.name,
                                          question.file_path, question.title)
        
class SolvedProblemForm(forms.Form):

    team = forms.ChoiceField(
        choices=TeamRepository.getAllTeamNames,
        required=True,
        label='Team Name',
    )

    question = forms.ChoiceField(
        choices=QuestionRepository.getAllQuestionsTitle,
        required=True,
        label='Question Title'
    )

    @classmethod
    def execute(self, teamId: int, questionId: int):
        question = QuestionRepository.getById(questionId)
        questionConfig = question.hardness_configuration
        team = TeamRepository.getById(teamId)
        TeamEntity.objects.filter(id=teamId).update(budget=(team.budget + (2 * questionConfig.cost)))

        QuestionStatusEntity.objects.filter(question=question, team=team).update(status="s")

        score = ScoreRepository.getByTeamId(teamId=teamId)
        # ScoresEntity.objects.filter(id=score.id).update(total_score=(score.total_score + questionConfig.score))

        solverTeamIds = [ question["team"] for question in list(QuestionStatusRepository.getQuestionSolversTeamIds(questionId=questionId))]
        
        solverScores = list(ScoreRepository.getByTeamIds(solverTeamIds))
        solverCount = len(solverTeamIds)

        newScore = (float(questionConfig.score) / 2) + (float(questionConfig.score) / (2 * int(solverCount)))

        for score in solverScores:
            score.total_score = newScore

        ScoresEntity.objects.bulk_update(solverScores, ["total_score"])
    
class sellQuestionForm(forms.Form):

    team = forms.ChoiceField(
        choices=TeamRepository.getAllTeamNames,
        required=True,
        label='Team Name',
    )

    question = forms.ChoiceField(
        choices=QuestionRepository.getAllQuestionsTitle,
        required=True,
        label='Question Title'
    )

    @classmethod
    def execute(self, teamId: int, questionId: int):
        question = QuestionRepository.getById(questionId)
        questionConfig = question.hardness_configuration
        team = TeamRepository.getById(teamId)

        QuestionStatusEntity.objects.filter(question=question, team=team).update(status="r")    
        TeamEntity.objects.filter(id=teamId).update(budget=(team.budget + float(questionConfig.cost / 2)))    
class WrongQuestionFaultForm(forms.Form):

    team = forms.ChoiceField(
        choices=TeamRepository.getAllTeamNames,
        required=True,
        label='Team Name',
    )         

    @classmethod
    def execute(self, teamId: int):
        score = ScoreRepository.getByTeamId(teamId);
        ScoresEntity.objects.filter(team=teamId).update(total_score = (score.total_score - 1))
                            