#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


import pytest
import asyncio

from firebase import initialize_app
from tests import config
from tests.utils import rand_str


@pytest.fixture(scope='session')
def event_loop():
	loop = asyncio.get_event_loop()
	loop.close = lambda: None
	yield loop

@pytest.fixture(scope='session')
async def client_app():
	yield initialize_app(config.SIMPLE_CONFIG)

@pytest.fixture(scope='session')
async def service_app():
	yield initialize_app(config.SERVICE_CONFIG)

@pytest.fixture(scope='session')
def auth(client_app):
	return client_app.auth(config.OAUTH_CLIENT_ID, config.OAUTH_CLIENT_SECRET, config.OAUTH_CLIENT_REDIRECT_URI)

@pytest.fixture(scope='session')
def auth_admin(service_app):
	return service_app.auth(config.OAUTH_CLIENT_ID, config.OAUTH_CLIENT_SECRET, config.OAUTH_CLIENT_REDIRECT_URI)

@pytest.fixture(scope='session')
async def db(service_app):
	# To make it easier to test, we keep the test restricted to firebase_tests
	# Because of the current mutations on calls, we return it as a function.
	try:
		yield lambda: service_app.database().child('firebase_tests')
	finally:
		await service_app.database().child('firebase_tests').remove()

@pytest.fixture(scope='session')
def email():
	return f'{rand_str()}@gmail.com'

@pytest.fixture(scope='session')
def email_2():
	return f'{rand_str()}@gmail.com'

@pytest.fixture(scope='session')
def ds(client_app):
	return client_app.firestore()

@pytest.fixture(scope='session')
def ds_admin(service_app):
	return service_app.firestore()

@pytest.fixture(scope='session')
def password():
	return rand_str()

@pytest.fixture(scope='session')
def password_2():
	return rand_str()

@pytest.fixture(scope='session')
def storage(client_app):
	return client_app.storage()

@pytest.fixture(scope='session')
def storage_admin(service_app):
	return service_app.storage()
