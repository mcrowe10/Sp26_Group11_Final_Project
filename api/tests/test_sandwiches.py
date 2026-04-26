from fastapi.testclient import TestClient
from ..controllers import order_details as controller
from ..main import app
import pytest
from ..models import sandwiches as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_order_detail(db_session):
    # Create a sample sandwich
    sandwich_data = {
        "sandwich_name": "Veggie",
        "price": 5.99,
        "calories": 350,
        "food_category": "Vegetarian"
    }

    sandwich_object = model.Sandwich(**sandwich_data)

    # Call the create function
    created_sandwich = controller.create(db_session, sandwich_object)

    # Assertions
    assert created_sandwich is not None
    assert created_sandwich.sandwich_name == "Veggie"
    assert created_sandwich.price == 5.99
    assert created_sandwich.calories == 350
    assert created_sandwich.food_category == "Vegetarian"
