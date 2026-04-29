"""
Servicio de notificaciones para inventario.

Usado para demostrar mocking en tests.
"""


class NotificationService:
    """Servicio base de notificaciones."""

    def send_notification(self, message: str) -> bool:
        """Envía una notificación (implementación simulada)."""
        print(f"Notification: {message}")
        return True


class EmailService(NotificationService):
    """Servicio de notificaciones por email."""

    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Envía un email (simulado)."""
        print(f"Email to {to}: {subject}")
        return True


class InventoryNotifier:
    """Notificador de eventos de inventario."""

    def __init__(self, service: NotificationService):
        self.service = service

    def notify_low_stock(self, product_id: str, product_name: str, stock: int) -> bool:
        """Notifica stock bajo."""
        message = f"LOW STOCK ALERT: {product_name} (ID: {product_id}) - Only {stock} units left"
        return self.service.send_notification(message)

    def notify_restock(self, product_id: str, product_name: str, quantity: int) -> bool:
        """Notifica reabastecimiento."""
        message = f"RESTOCK: {product_name} (ID: {product_id}) - Added {quantity} units"
        if hasattr(self.service, "send_email"):
            return self.service.send_email(
                "admin@example.com", "Restock Alert", message
            )
        return self.service.send_notification(message)
