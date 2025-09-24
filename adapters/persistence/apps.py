from django.apps import AppConfig

class PersistenceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adapters.persistence'
    label = 'persistence'  # Unique label for this app
    verbose_name = 'Task Management Persistence'
