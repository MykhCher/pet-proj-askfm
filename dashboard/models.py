from core.models import Answer

class Dashboard(Answer):
    class Meta:
        proxy = True
