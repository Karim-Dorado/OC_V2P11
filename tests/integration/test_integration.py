def test_login_and_success_booking_places(client):
    club = "She Lifts"
    email = "kate@shelifts.co.uk"
    competition = "Fall Classic"
    login = client.post('/showSummary',  data={"email": email, "name": club}, follow_redirects=True)
    assert login.status_code == 200
    assert ("Welcome, " + email) in login.data.decode()
    response = client.post(
        '/purchasePlaces',
        data={
            'club': club,
            'competition': competition,
            'places': 1
            }
    )
    assert response.status_code == 200
    assert ("Great-booking complete!") in response.data.decode()


def test_login_and_to_much_booking_places(client):
    club = "Iron Temple"
    email = "admin@irontemple.com"
    competition = "Fall Classic"
    login = client.post('/showSummary',  data={"email": email, "name": club}, follow_redirects=True)
    assert login.status_code == 200
    assert ("Welcome, " + email) in login.data.decode()
    response = client.post(
        '/purchasePlaces',
        data={
            'club': club,
            'competition': competition,
            'places': 6
            }
    )
    assert response.status_code == 200
    assert ("Not enough points to require this number of places!") in response.data.decode()


def test_login_and_fail_negative_booking_places(client):
    club = "Simply Lift"
    email = "john@simplylift.co"
    competition = "Fall Classic"
    login = client.post('/showSummary',  data={"email": email, "name": club}, follow_redirects=True)
    assert login.status_code == 200
    assert ("Welcome, " + email) in login.data.decode()
    response = client.post(
        '/purchasePlaces',
        data={
            'club': club,
            'competition': competition,
            'places': -1
            }
    )
    assert response.status_code == 200
    assert ("Please, enter a positive number!") in response.data.decode()


def test_login_and_purchase_more_than_12_places(client):
    club = "Simply Lift"
    email = "john@simplylift.co"
    competition = "Fall Classic"
    login = client.post('/showSummary',  data={"email": email, "name": club}, follow_redirects=True)
    assert login.status_code == 200
    assert ("Welcome, " + email) in login.data.decode()
    response = client.post(
        '/purchasePlaces',
        data={
            'club': club,
            'competition': competition,
            'places': 13
            }
    )
    assert response.status_code == 200
    assert ("You cannot require more than 12 places per competition") in response.data.decode()


def test_login_and_book(client):
    club = "Simply Lift"
    email = "john@simplylift.co"
    competition = "Fall Classic"
    login = client.post('/showSummary',  data={"email": email, "name": club}, follow_redirects=True)
    assert login.status_code == 200
    assert ("Welcome, " + email) in login.data.decode()
    response = client.get(f"/book/{competition}/{club}")
    assert response.status_code == 200
