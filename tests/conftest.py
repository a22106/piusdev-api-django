import pytest
from rest_framework.test import APIClient
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture(scope='function') # 테스트 함수마다 실행
def live_server():
    server = StaticLiveServerTestCase('run')
    server._pre_setup()
    server.setUpClass()
    yield server.live_server_url
    server.tearDownClass()
    server._post_teardown()

