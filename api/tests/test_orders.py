from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model
from ..schemas.orders import OrderUpdate

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_order(db_session):
    # Create a sample order
    order_data = {
        "customer_name": "John Doe",
        "order_date": "2021-04-01",
        "description": "Test order",
        "tracking_number": "1A2B3C",
        "order_status": "Test",
    }

    order_object = model.Order(**order_data)

    # Call the create function
    created_order = controller.create(db_session, order_object)

    # Assertions
    assert created_order is not None
    assert created_order.customer_id is None
    assert created_order.customer_name == "John Doe"
    assert created_order.order_date == "2021-04-01"
    assert created_order.description == "Test order"
    assert created_order.tracking_number == "1A2B3C"
    assert created_order.order_status == "Test"
    assert created_order.price == 0.0
