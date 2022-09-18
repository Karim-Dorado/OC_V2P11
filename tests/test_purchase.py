def test_success_booking_places(client):
    club = "Simply Lift"
    competition = "Fall Classic"
    response = client.post(
        '/purchasePlaces',
        data={
            'club':club,
            'competition':competition,
            'places':10
            }
    )
    assert response.status_code == 200
    assert ("Great-booking complete!") in response.data.decode()


def test_booking_without_enough_points(client):
    club = "Simply Lift"
    competition = "Fall Classic"
    response = client.post(
        '/purchasePlaces',
        data={
            'club':club,
            'competition':competition,
            'places':14
            }
    )
    assert response.status_code == 200
    assert ("Not enough points to require this number of places!") in response.data.decode()


def test_booking_more_than_12_places(client):
    club = "Simply Lift"
    competition = "Spring Festival"
    response = client.post(
        '/purchasePlaces',
        data={
            'club':club,
            'competition':competition,
            'places':13
            }
    )
    assert response.status_code == 200
    assert ("You cannot require more than 12 places per competition") in response.data.decode()
