import os
import pytest


@pytest.fixture
def test_ebay_page() -> str:
    # Get the directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the test file
    file_path = os.path.join(current_directory, "test_ebay_page.html")

    with open(file_path) as f:
        return f.read()
