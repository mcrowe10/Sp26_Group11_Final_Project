from fastapi.testclient import TestClient
from ..controllers import customers as controller
from ..main import app
import pytest
from ..models import customers as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_customer(db_session, mocker):
    # Create mock payment
    payment = mocker.Mock()
    payment.id = 1

    # Create a sample customer
    customer_data = {
        "customer_name": "John Doe",
        "default_payment": payment.id,
    }

    customer_object = model.Customer(**customer_data)

    # Call the create function
    created_customer = controller.create(db_session, customer_object)

    # Assertions
    assert created_customer is not None
    assert created_customer.customer_name == "John Doe"
    assert created_customer.default_payment == payment.id