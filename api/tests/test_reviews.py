from fastapi.testclient import TestClient
from ..controllers import reviews as controller
from ..main import app
import pytest
from ..models import reviews as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_reviews(db_session, mocker):
    # Create mock customer
    customer = mocker.Mock()
    customer.id = 1

    # Create a sample review
    review_data = {
        "customer_id": customer.id,
        "review_text": "Test review",
        "score": 5.0
    }

    review_object = model.Review(**review_data)

    # Call the create function
    created_review = controller.create(db_session, review_object)

    # Assertions
    assert created_review is not None
    assert created_review.customer_id == customer.id
    assert created_review.review_text == "Test review"
    assert created_review.score == 5.0
