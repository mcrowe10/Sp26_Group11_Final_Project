from fastapi.testclient import TestClient
from ..controllers import payments as controller
from ..main import app
import pytest
from ..models import payments as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_payment(db_session):
    # Create a sample payment
    payment_data = {
        "card_info": "1234 8765 2468 3579",
        "status": "Test",
        "payment_type": "Credit"
    }

    payment_object = model.Payment(**payment_data)

    # Call the create function
    created_payment = controller.create(db_session, payment_object)

    # Assertions
    assert created_payment is not None
    assert created_payment.card_info == "1234 8765 2468 3579"
    assert created_payment.status == "Test"
    assert created_payment.payment_type == "Credit"