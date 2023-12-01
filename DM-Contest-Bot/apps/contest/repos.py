from .models import (TeamEntity, QuestionStatusEntity, 
                     QuestionEntity, QuestionsHardnessConfigurationEntity,
                     ScoresEntity)
from core.models import Entity
from abc import ABC, abstractmethod

class AEntityRepository(ABC):

    @abstractmethod
    def getEntityclass(self) -> Entity:
        pass

    @classmethod
    def getByIds(self, ids):
        return list(self.getEntityclass().objects.filter(id__in=ids))
    
    @classmethod
    def getById(self, id: int):
        return list(self.getEntityclass().objects.filter(id=id))[0]

    @classmethod
    def getAll(self):
        return list(self.getEntityclass().objects.all())

class  TeamRepository(AEntityRepository):

    @classmethod
    def getEntityclass(self):
        return TeamEntity

    @classmethod
    def getAllTeamNames(self):
        return [(team['id'], team['name']) for team in self.getEntityclass().objects.values('id', 'name').iterator()]
    
class QuestionStatusRepository(AEntityRepository):

    @classmethod
    def getEntityclass(self) -> Entity:
        return QuestionStatusEntity

    @classmethod
    def getTeamSeenQuestionIds(self, teamId: int):
        return self.getEntityclass().objects.filter(team=teamId).values('question_id')
    
    @classmethod
    def getCountSolvedOfQuestion(self, questionId: int) -> int:
        return self.getEntityclass().objects.filter(question=questionId).filter(status="s").count()
    
    @classmethod
    def getQuestionSolversTeamIds(self, questionId: int):
        return self.getEntityclass().objects.filter(question=questionId).filter(status="s").values("team")


class QuestionRepository(AEntityRepository):

    @classmethod
    def getEntityclass(self) -> Entity:
        return QuestionEntity
    
    @classmethod
    def getUnseenQuestionsByDifficultyLevelIds(self, seenQuestionIds, difficultiyLevelId: int):
        return (self.getEntityclass()
                .objects
                .filter(hardness_configuration=difficultiyLevelId)
                .exclude(id__in=seenQuestionIds)
                .values('id'))

    @classmethod
    def getAllQuestionsTitle(self):
        return [(question['id'], question['title']) for question in self.getEntityclass().objects.values('id', 'title').iterator()]

class QuestionHardnessConfigurationRepository(AEntityRepository):

    @classmethod
    def getEntityclass(self) -> Entity:
        return QuestionsHardnessConfigurationEntity
    
    @classmethod
    def getById(self, id: int):
        return list(self.getEntityclass().objects.filter(level=id))[0]

    @classmethod
    def getCost(self, difficultyLevelId: int) -> float:
        return self.getById(difficultyLevelId).cost
    
class ScoreRepository(AEntityRepository):

    @classmethod
    def getEntityclass(self) -> Entity:
        return ScoresEntity
    
    @classmethod
    def getByTeamId(self, teamId: int) -> ScoresEntity:
        return list(self.getEntityclass().objects.filter(team=teamId))[0]
    
    @classmethod
    def getByTeamIds(self, teamIds):
        return list((self.getEntityclass().objects.filter(team__in=teamIds)))
    