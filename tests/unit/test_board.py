def test_display_board(client):
    response = client.get('/board')
    assert response.status_code == 200
    assert ('Simply Lift Points: 40') in response.data.decode()
    assert ('Iron Temple Points: 4') in response.data.decode()
    assert ('She Lifts Points:') in response.data.decode()
