from fastapi.testclient import TestClient
from ..controllers import order_details as controller
from ..main import app
import pytest
from ..models import order_details as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_order_detail(db_session, mocker):
    order = mocker.Mock()
    order.id = 1
    order.price = 0.0

    db_session.query.return_value.filter.return_value.first.return_value = order

    resource = mocker.Mock()
    resource.amount = 10

    recipe = mocker.Mock()
    recipe.resource = resource
    recipe.amount = 1

    sandwich = mocker.Mock()
    sandwich.id = 2
    sandwich.price = 5.99
    sandwich.recipes = [recipe]

    db_session.query.return_value.options.return_value.filter.return_value.first.return_value = sandwich

    order_detail_data = {
        "order_id": order.id,
        "sandwich_id": sandwich.id,
        "amount": 2
    }

    order_detail_object = model.OrderDetail(**order_detail_data)

    # Call the create function
    created_order_detail = controller.create(db_session, order_detail_object)

    # Assertions
    assert created_order_detail is not None
    assert created_order_detail.order_id == order.id
    assert created_order_detail.sandwich_id == sandwich.id
    assert resource.amount == 8
    assert order.price == 11.98
