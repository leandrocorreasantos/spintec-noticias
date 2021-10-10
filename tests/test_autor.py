from api.app import application
from api.config import TestingConfig
from http.client import OK


application.config.from_object(TestingConfig)
app = application.test_client()

def test_get_all_autors_should_return_ok():
    response = app.get('/v1/autor')
    assert response.status_code == OK.value
