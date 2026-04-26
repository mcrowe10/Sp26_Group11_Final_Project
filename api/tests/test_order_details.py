from fastapi.testclient import TestClient
from ..controllers import order_details as controller
from ..main import app
import pytest
from ..models import order_details as model
from ..models import orders as order_model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_order_detail(db_session):
    # Create a sample order
    order_data = {
        "customer_name": "John Doe",
        "order_date": "2021-04-01",
        "description": "Test order",
        "tracking_number": "1A2B3C",
        "order_status": "Test",
    }

    order_object = order_model.Order(**order_data)

    # Call the create function
    created_order = controller.create(db_session, order_object)

    # Assertions
    assert created_order is not None
    assert created_order.customer_name == "John Doe"
    assert created_order.description == "Test order"
