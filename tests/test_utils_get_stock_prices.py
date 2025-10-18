import pytest
from unittest.mock import patch, Mock
from src.utils import get_stock_prices

test_stocks = ['AAPL', 'GOOGL']

mock_response_data = {
    'AAPL': {'price': 232.8},
    'GOOGL': {'price': 3200.5}
}


def mock_requests_get(*args, **kwargs):
    mock_response = Mock()
    stock = args[0].split('symbol=')[1].split('&')[0]

    if stock in mock_response_data:
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'symbol': stock,
                'price': mock_response_data[stock]['price']
            }
        ]
    else:
        mock_response.status_code = 404
        mock_response.json.return_value = {'error': 'Stock not found'}

    return mock_response


@patch('requests.get', side_effect=mock_requests_get)
def test_get_stock_prices_success(mock_get):
    result = get_stock_prices(test_stocks)
    assert len(result) == 2
    aapl_price = result[0]
    assert aapl_price['stock'] == 'AAPL'
    assert aapl_price['price'] == 232.80
    googl_price = result[1]
    assert googl_price['stock'] == 'GOOGL'
    assert googl_price['price'] == 3200.50


@patch('requests.get')
def test_get_stock_prices_error(mock_get):
    # Создаем мок ответа сервера
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {'error': 'Internal Server Error'}
    mock_get.return_value = mock_response

    # Вызываем тестируемую функцию
    result = get_stock_prices(test_stocks)

    # Проверяем, что результат пустой
    assert len(result) == 0, "Результат должен быть пустым при ошибке сервера"

    # Дополнительно можно проверить:
    # 1. Статус код ответа
    assert mock_get.called, "Запрос должен был быть сделан"
    assert mock_get.call_count == len(test_stocks), "Количество запросов должно соответствовать количеству тикеров"

    # 2. Содержимое ответа
    for call in mock_get.call_args_list:
        args, _ = call
        url = args[0]
        assert "symbol=" in url, "URL должен содержать параметр symbol"
        assert "apikey=" in url, "URL должен содержать API ключ"

    # 3. Тип возвращаемого значения
    assert isinstance(result, list), "Результат должен быть списком"


@patch('requests.get')
def test_get_stock_prices_single_stock(mock_get):
    # Симулируем ответ для одной акции
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            'symbol': 'AAPL',
            'price': 232.8
        }
    ]
    mock_get.return_value = mock_response

    result = get_stock_prices(['AAPL'])
    assert len(result) == 1
    assert result[0]['stock'] == 'AAPL'
    assert result[0]['price'] == 232.80