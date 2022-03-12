import re


class TestFibonacciView:

    def test_no_params(self, client):
        response = client.get('/fibonacci')
        assert response.status_code == 200, 'Status code not 200'
        assert re.search(r'<p id="response">\[0, 1, 1, 2, 3, 5\]</p>', response.data.decode('utf-8')), \
            'Actual != expected'

    def test_with_params(self, client):
        for params, correct in (
                ({'from_arg': '1', 'to_arg': '2', 'slice_type': 'pos'}, r'<p id="response">\[1, 1\]</p>'),
                ({'from_arg': '2', 'to_arg': '4', 'slice_type': 'val'}, r'<p id="response">\[2, 3\]</p>'),
        ):
            response = client.get('/fibonacci', query_string=params)
            assert response.status_code == 200, 'Status code not 200'
            assert re.search(correct, response.data.decode('utf-8')), \
                'Actual != expected'

    def test_wrong_params(self, client):
        default_response = r'<p id="response">\[0, 1, 1, 2, 3, 5\]</p>'
        for wrong_params in (
                {'from': '-3', 'to': '5', 'slice_type': 'pos'},
                {'from': '5', 'to': '-7', 'slice_type': 'val'},
                {'from': 'e', 'to': '0', 'slice_type': 'pos'},
                {'from': '1', 'to': 'e', 'slice_type': 'val'},
                {'from': 'er', 'to': 're', 'slice_type': 'pos'}
        ):
            response = client.get('/fibonacci', query_string=wrong_params)
            assert response.status_code == 200, 'Status code not 200'
            assert re.search(default_response, response.data.decode('utf-8')), \
                'Actual != expected'
