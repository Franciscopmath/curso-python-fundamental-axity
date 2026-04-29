"""
Tests usando mocking con unittest.mock.

Demuestra cómo mockear dependencias externas.
"""

import pytest
from decimal import Decimal
from unittest.mock import Mock, patch, MagicMock, call
from src.inventory import Inventory, Product
from src.notification_service import NotificationService, InventoryNotifier


class TestNotificationServiceMocking:
    """Tests de servicio de notificaciones usando mocking."""

    def test_send_notification_called(self, mocker):
        """Test: Verifica que se llame a send_notification."""
        # Mock del servicio
        mock_service = mocker.Mock(spec=NotificationService)

        notifier = InventoryNotifier(mock_service)
        notifier.notify_low_stock("P001", "Mouse", 2)

        # Verificar que se llamó al método
        mock_service.send_notification.assert_called_once()

    def test_send_notification_with_correct_message(self, mocker):
        """Test: Verifica el mensaje correcto en notificación."""
        mock_service = mocker.Mock(spec=NotificationService)

        notifier = InventoryNotifier(mock_service)
        notifier.notify_low_stock("P001", "Keyboard", 3)

        # Verificar el mensaje
        args = mock_service.send_notification.call_args[0]
        assert "Keyboard" in args[0]
        assert "3" in args[0]

    @patch("src.notification_service.EmailService")
    def test_email_service_integration(self, mock_email_class):
        """Test: Mock de clase EmailService completa."""
        # Configurar mock
        mock_instance = mock_email_class.return_value
        mock_instance.send_email.return_value = True

        notifier = InventoryNotifier(mock_instance)
        result = notifier.notify_restock("P001", "Monitor", 100)

        assert result is True
        mock_instance.send_email.assert_called_once()

    def test_multiple_notifications(self, mocker):
        """Test: Múltiples llamadas a notificaciones."""
        mock_service = mocker.Mock()

        notifier = InventoryNotifier(mock_service)
        notifier.notify_low_stock("P001", "Item1", 1)
        notifier.notify_low_stock("P002", "Item2", 2)
        notifier.notify_low_stock("P003", "Item3", 3)

        # Verificar que se llamó 3 veces
        assert mock_service.send_notification.call_count == 3

    def test_notification_raises_exception(self, mocker):
        """Test: Manejo de excepciones en notificaciones."""
        mock_service = mocker.Mock()
        mock_service.send_notification.side_effect = ConnectionError("Network error")

        notifier = InventoryNotifier(mock_service)

        with pytest.raises(ConnectionError):
            notifier.notify_low_stock("P001", "Item", 1)


class TestInventoryWithMocking:
    """Tests de inventario usando mocking para dependencias."""

    @patch("src.inventory.Database")
    def test_save_product_to_database(self, mock_db_class):
        """Test: Mock de guardado en base de datos."""
        # Configurar mock
        mock_db = mock_db_class.return_value
        mock_db.save.return_value = True

        inventory = Inventory()
        product = Product("P001", "Item", Decimal("10"), 5)
        inventory.add_product(product)

        # Simular guardado (normalmente sería inventory.save_to_db())
        result = mock_db.save(product)

        assert result is True
        mock_db.save.assert_called_with(product)

    def test_mock_external_api_call(self, mocker):
        """Test: Mock de llamada a API externa."""
        # Mock de requests.get
        mock_get = mocker.patch("requests.get")
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "P001",
            "name": "External Product",
            "price": "99.99",
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Código que usaría la API (simulado)
        import requests

        response = requests.get("https://api.example.com/products/P001")

        assert response.status_code == 200
        assert response.json()["name"] == "External Product"
        mock_get.assert_called_once_with("https://api.example.com/products/P001")
