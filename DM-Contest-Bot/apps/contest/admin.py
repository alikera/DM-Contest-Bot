from django.contrib import admin
from .models import (TeamEntity, QuestionEntity, 
                     ScoresEntity, QuestionStatusEntity, 
                     QuestionsHardnessConfigurationEntity)

# Register your models here.
admin.site.register(TeamEntity)
admin.site.register(QuestionEntity)
admin.site.register(ScoresEntity)
admin.site.register(QuestionStatusEntity)
admin.site.register(QuestionsHardnessConfigurationEntity)