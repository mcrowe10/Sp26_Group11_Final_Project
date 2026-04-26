from fastapi.testclient import TestClient
from ..controllers import order_details as controller
from ..main import app
import pytest
from ..models import recipes as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_order_detail(db_session):
    # Create a sample order
    recipe_data = {
        "id": 1,
        "sandwich_id": 1,
        "resource_id": 1,
    }

    recipe_object = model.Recipe(**recipe_data)

    # Call the create function
    created_recipe = controller.create(db_session, recipe_object)

    # Assertions
    assert created_recipe is not None
    assert created_recipe.customer_name == "John Doe"
    assert created_recipe.description == "Test order"
