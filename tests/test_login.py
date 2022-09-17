 
def test_valid_email(client):
    email = "john@simplylift.co"
    response = client.post('/showSummary', data={"email": email})
    assert response.status_code == 200
    assert ("Welcome, " + email) in response.data.decode()


def test_invalid_email(client):
	response = client.post('/showSummary', data={"email": "test@test.com"})
	assert response.status_code == 200
	assert ("Unknown email address") in response.data.decode()

def test_empty_email(client):
    response = client.post('/showSummary', data = {"email": ""})
    assert response.status_code == 200
    assert ("Unknown email address") in response.data.decode()