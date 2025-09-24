import pytest

def pytest_configure():
    import os
    import django
    from django.conf import settings
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frameworks.webapp.webapp.settings')
    django.setup()

# Automatically apply django_db to all tests
@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
