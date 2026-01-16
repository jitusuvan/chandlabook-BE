from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        
        import api.Guest.model
        import api.GuestRecord.model
        import api.Event.model
        import api.Expense.model

        