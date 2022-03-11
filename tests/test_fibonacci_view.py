import re


class TestFibonacciView:

    def test_no_params(self, client):
        response = client.get('/fibonacci')
        assert response.status_code == 200
        assert re.search(r'<p id="response">0, 1, 1, 2, 3, 5</p>', response.data.decode('utf-8'))

    def test_with_params(self, client):
        response = client.get('/fibonacci', query_string={'from': '1', 'to': '2'})
        assert response.status_code == 200
        assert re.search(r'<p id="response">1, 1</p>', response.data.decode('utf-8'))

    def test_wrong_params(self, client):
        for wrong_params in (
                {'from': '-3', 'to': '5'},
                {'from': '5', 'to': '-7'},
                {'from': 'e', 'to': '0'},
                {'from': '1', 'to': 'e'},
                {'from': 'er', 'to': 're'}
        ):
            response = client.get('/fibonacci', query_string=wrong_params)
            assert response.status_code == 200
            assert re.search(r'<p id="response">form errors</p>', response.data.decode('utf-8'))
