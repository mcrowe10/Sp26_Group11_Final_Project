from fastapi.testclient import TestClient
from ..controllers import recipes as controller
from ..main import app
import pytest
from ..models import recipes as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_recipe(db_session, mocker):
    # Create mock sandwich
    sandwich = mocker.Mock()
    sandwich.id = 1

    # Create mock resource
    resource = mocker.Mock()
    resource.id = 2

    # Create a sample recipe
    recipe_data = {
        "sandwich_id": sandwich.id,
        "resource_id": resource.id,
        "amount": 1
    }

    recipe_object = model.Recipe(**recipe_data)

    # Call the create function
    created_recipe = controller.create(db_session, recipe_object)

    # Assertions
    assert created_recipe is not None
    assert created_recipe.sandwich_id == sandwich.id
    assert created_recipe.resource_id == resource.id
    assert created_recipe.amount == 1
