import pytest
from unittest.mock import patch, Mock
import requests
from src.utils import get_currency_rates

test_currencies = ['USD', 'EUR']

mock_response_data = {
    'USD': {'result': 90.5678},
    'EUR': {'result': 100.1234}
}


def mock_requests_get(*args, **kwargs):
    mock_response = Mock()
    currency = args[0].split('from=')[1].split('&')[0]

    if currency in mock_response_data:
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'result': mock_response_data[currency]['result']
        }
    else:
        mock_response.status_code = 404
        mock_response.json.return_value = {'error': 'Currency not found'}

    return mock_response


@patch('requests.get', side_effect=mock_requests_get)
def test_get_currency_rates(mock_get):
    result = get_currency_rates(test_currencies)
    assert len(result) == 2
    usd_rate = result[0]
    assert usd_rate['currency'] == 'USD'
    assert usd_rate['rate'] == 90.57
    eur_rate = result[1]
    assert eur_rate['currency'] == 'EUR'
    assert eur_rate['rate'] == 100.12


@patch('requests.get')
def test_get_currency_rates_error(mock_get):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {'error': 'Internal Server Error'}
    mock_get.return_value = mock_response

    result = get_currency_rates(test_currencies)
    assert len(result) == 0


@patch('requests.get')
def test_get_currency_rates_invalid_currency(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {'error': 'Currency not found'}
    mock_get.return_value = mock_response

    result = get_currency_rates(['XYZ'])
    assert len(result) == 0


@patch('requests.get')
def test_get_currency_rates_empty_list(mock_get):
    result = get_currency_rates([])
    assert len(result) == 0


@patch('requests.get')
def test_get_currency_rates_single_currency(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'result': 90.5678}
    mock_get.return_value = mock_response

    result = get_currency_rates(['USD'])
    assert len(result) == 1
    assert result[0]['currency'] == 'USD'
    assert result[0]['rate'] == 90.57