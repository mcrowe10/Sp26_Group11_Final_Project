from fastapi.testclient import TestClient
from ..controllers import order_details as controller
from ..main import app
import pytest
from ..models import resources as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_order_detail(db_session):
    # Create a sample sandwich
    resource_data = {
        "item": "Bread",
        "amount": 10
    }

    resource_object = model.Resource(**resource_data)

    # Call the create function
    created_resource = controller.create(db_session, resource_object)

    # Assertions
    assert created_resource is not None
    assert created_resource.item == "Bread"
    assert created_resource.amount == 10
