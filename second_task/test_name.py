import pytest
from scanner_handler import CheckQr
from unittest.mock import patch


# Фікстура для створення екземпляра класу CheckQr
@pytest.fixture
def qr_checker():
    return CheckQr()

@pytest.mark.parametrize("qr, expected_color", [
    ('123', 'Red'),
    ('12345', 'Green'),
    ('1234567', 'Fuzzy Wuzzy'),
])
def test_color_success(qr: str, expected_color: str, qr_checker: CheckQr) -> None:
    """
    Перевіряє, що при скануванні QR-кодів з допустимою довжиною:
    - змінна color набуває правильного значення
    - викликається метод can_add_device з очікуваним аргументом
    """
    with patch.object(qr_checker, 'check_in_db', return_value=True):
        with patch.object(qr_checker, 'can_add_device') as mock_success:
            qr_checker.check_scanned_device(qr)

            # color має правильне значення
            assert qr_checker.color == expected_color

            # can_add_device викликається з правильним параметром
            mock_success.assert_called_with(f'hallelujah {qr}')


@pytest.mark.parametrize("qr", [
    '12',        # 2 символи — колір відсутній
    '1234',      # 4 символи — колір відсутній
    '12345678',  # 8 символів — колір відсутній
])
def test_check_len_color_fail(qr: str, qr_checker: CheckQr) -> None:
    """
    Перевіряє поведінку для QR-кодів з довжиною, яка не відповідає жодному кольору:
    - має бути викликано send_error з повідомленням про неправильну довжину
    """
    with patch.object(qr_checker, 'check_in_db', return_value=True):
        with patch.object(qr_checker, 'send_error') as mock_error:
            qr_checker.check_scanned_device(qr)

            # Перевірка, що метод send_error викликається з правильним повідомленням
            mock_error.assert_called_with(f"Error: Wrong qr length {len(qr)}")


@pytest.mark.parametrize("qr", [
    '12345',      # довжина правильна, але немає в DB
    '123',        # довжина правильна, але немає в DB
    '1234567',    # довжина правильна, але немає в DB
])
def test_qr_not_in_db(qr: str, qr_checker: CheckQr) -> None:
    """
    Перевіряє поведінку, коли QR-код має правильну довжину, але не знайдений у БД:
    - має бути викликано send_error з повідомленням "Not in DB"
    """
    with patch.object(qr_checker, 'check_in_db', return_value=None), \
         patch.object(qr_checker, 'send_error') as mock_send_error:
        qr_checker.check_scanned_device(qr)

        # Перевірка, що метод send_error викликається з повідомленням "Not in DB"
        mock_send_error.assert_called_with("Not in DB")


def test_successful_scan(qr_checker: CheckQr) -> None:
    """
    Перевіряє повністю успішний сценарій:
    - QR-код має допустиму довжину
    - QR знайдено у DB
    - очікується виклик can_add_device з правильним аргументом
    """
    qr = '12345'  # 5 символів: Green
    with patch.object(qr_checker, 'check_in_db', return_value=True), \
         patch.object(qr_checker, 'can_add_device') as mock_can_add_device:
        qr_checker.check_scanned_device(qr)

        # Перевірка, що color має значення Green
        assert qr_checker.color == "Green"

        # Перевірка, що метод can_add_device викликається з правильним параметром
        mock_can_add_device.assert_called_with(f"hallelujah {qr}")
