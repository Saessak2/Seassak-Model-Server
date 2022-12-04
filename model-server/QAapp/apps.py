from django.apps import AppConfig
import os

class QaappConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'QAapp'

    def ready(self):
        if not os.environ.get('APP'):
            os.environ['APP'] = 'True'
            # print('1')
        # print(f'app = {os.getpid()}')



        # app/__init__.py
# default_app_config = 'app.broker.MyAppConfig' 