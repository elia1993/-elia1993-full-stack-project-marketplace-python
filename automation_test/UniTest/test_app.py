import logging
import pytest
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def extract_user_name(html):
    soup = BeautifulSoup(html, 'html.parser')
    user_greeting = soup.find('h2', text=lambda t: t and "Hi" in t)
    if user_greeting:
        return user_greeting.get_text(strip=True).replace('Hi ', '').replace('!', '')
    return None

def test_root(client):
    response = client.get('/')
    logger.info("Testing root endpoint: %s", response.status_code)
    assert response.status_code == 200

def test_register(client):
    response = client.get('/register')
    logger.info("Testing register endpoint: %s", response.status_code)
    assert response.status_code == 200

def test_login(client):
    response = client.post('/login', data={
        'email': 'rotana12@gmail.com',
        'password': '12345678'
    })

    response_data = response.data.decode('utf-8')
    logger.info("Login response status: %s", response.status_code)
    assert response.status_code == 200
    assert "logout" in response_data

    user_name = extract_user_name(response_data)
    if user_name:
        logger.info("Logged in user: %s", user_name)
    else:
        logger.info("User name not found in login response")

def test_add_item(client):
    with client.session_transaction() as sess:
        sess['user_email'] = 'rotana12@gmail.com'

    response = client.get('/add_new_item', query_string={
        'itemName': 'pancake',
        'Price': '35',
        'itemUrl': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSt0mgUpErWuTtuy6NG09B1tklYdMoElu5ELA&s',
        'comment': 'This is a test item to add pancake'
    })
    logger.info("Add item response status: %s", response.status_code)
    assert response.status_code == 204

def test_edit_item(client):
    with client.session_transaction() as sess:
        sess['user_email'] = 'rotana12@gmail.com'

    response = client.post('/edit/pancake', data={
        'img_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSt0mgUpErWuTtuy6NG09B1tklYdMoElu5ELA&s',
        'name': 'pancake updated',
        'price': '25',
        'info': 'Updated info',
        'sale': 'yes',
        'sale_description': '50% off'
    })
    logger.info("Edit item response status: %s", response.status_code)
    assert response.status_code == 302

def test_about_page(client):
    with client.session_transaction() as sess:
        sess['user_email'] = 'rotana12@gmail.com'

    response = client.get('/about', query_string={
        'em': 'hunger@gmail.com'
    })
    logger.info("About page response status: %s", response.status_code)
    assert response.status_code == 200

def test_compare_page(client):
    with client.session_transaction() as sess:
        sess['user_email'] = 'rotana12@gmail.com'

    response = client.get('/compare', query_string={
        'left': 'hunger@gmail.com',
        'right': 'burger_king@gmail.com'
    })

    logger.info("Compare page response status: %s", response.status_code)
    assert response.status_code == 200
    assert b'hunger@gmail.com' in response.data
    assert b'burger_king@gmail.com' in response.data

def test_search_owner(client):
    with client.session_transaction() as sess:
        sess['user_email'] = 'rotana12@gmail.com'

    response = client.post('/search', data={'search': 'ruben', 'selected_search': 'name'})
    logger.info("Search owner response status: %s", response.status_code)
    assert response.status_code == 200

def test_logout(client):
    with client.session_transaction() as sess:
        sess['user_email'] = 'rotana12@gmail.com'

    response = client.get('/logout')
    logger.info("Logout response status: %s", response.status_code)
    assert response.status_code == 302
    assert response.headers["Location"] == "/"
