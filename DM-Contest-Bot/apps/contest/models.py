from django.db import models
from core.models import Entity
from core.settings import questions_file_path
from enum import Enum

class QuestionsHardnessConfigurationEntity(Entity):

    ALL_LEVELS = (
        (0, 'EASY'),
        (1, 'MEDIUM'),
        (2, 'HARD'),
    )

    ALL_SCORES = (
        (1, 'EASY'),
        (2, 'MEDIUM'),
        (3, 'HARD'),
    )

    level = models.IntegerField(
        primary_key=True,
        choices=ALL_LEVELS,
        null=False,
        default=0
    )

    coefficient = models.FloatField(
        null=False,
        default=0.0
    )

    cost = models.FloatField(
        null=False,
        default=0
    )

    score = models.CharField(
        choices=ALL_SCORES,
        null=False,
        default=0
    )

    def __str__(self) -> str:
        if self.level == 0:
            return 'Easy'
        elif self.level == 1:
            return 'Medium'
        else:
            return 'Hard'
        

    class Meta:
        db_table = 'questions_hardness_config'
        verbose_name = 'Questions Hardness Config'
        verbose_name_plural = 'Questions Hardness Config'

class QuestionEntity(Entity):

    ALL_SUBJECTS = (
        (0, 'fuck',),
        (1, 'suck'),
    )

    title = models.CharField(
        max_length=250,
        unique=True)
    
    subject = models.IntegerField(
        choices=ALL_SUBJECTS,
        null=True
    )

    file_path = models.FilePathField(
        path=questions_file_path,
        recursive=True,
        null=True,
        match=".*\.pdf")
    
    hardness_configuration = models.ForeignKey(
        QuestionsHardnessConfigurationEntity,
        on_delete=models.RESTRICT,
        null=True
    )
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        db_table = 'contest_questions'
        verbose_name = 'Contest Questions'
        verbose_name_plural = 'Contest Questions'

class TeamEntity(Entity):

    name = models.CharField(
        max_length=250, 
        null=False, 
        unique=True,
        default='')

    email = models.EmailField(
        max_length=254, 
        null=False, 
        unique=True, 
        help_text='exampl@gmail.com')

    budget = models.FloatField(
        default=0, 
        null=False)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'contest_teams'
        verbose_name = 'Contest Teams'
        verbose_name_plural = 'Contest Teams'

class QuestionStatusEntity(Entity):

    class QUESTION_STATUSES(Enum):
        BOUGHT = "bought"
        SOLVED = "solved"
        RETURNED = "returned"
        FUCKED = "fucked"

    ALL_STATUSES = (
        ("b", "bought"),
        ("s", "solved"),
        ("r", "returned")
    )

    team = models.ForeignKey(
        TeamEntity,
        on_delete=models.CASCADE,
        blank=True,
        null=False
    )

    question = models.ForeignKey(
        QuestionEntity,
        on_delete=models.CASCADE,
        blank=True,
        null=False
    )

    status = models.CharField(
        choices=ALL_STATUSES,
        max_length=50,
        null=False,
        blank=False,
        default="b"
    )

    def __str__(self):
        return "question " + self.question.title + " for team " + self.team.name
                                                            
    class Meta:
        db_table = 'contest_questions_status'
        verbose_name = 'Contest Questions Status'
        verbose_name_plural = 'Contest Questions Status'
        unique_together = [
            ["team", "question",]
        ]

class ScoresEntity(Entity):

    total_score = models.IntegerField(
        default=0,
        null=False
    )
    
    team = models.OneToOneField(
        TeamEntity,
        on_delete=models.CASCADE) 
    
    class Meta:
        db_table = 'scores'
        verbose_name = 'Scores'
        verbose_name_plural = 'Scores'
        ordering = ["-total_score",]
    
    def __str__(self) -> str:
        return 'score of team ' + str(self.team.name)
