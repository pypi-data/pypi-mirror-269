import pytest
import unittest

from promptflow.connections import CustomConnection
from promptflow_custom_tools.tools.claude import generate


@pytest.fixture
def my_custom_connection() -> CustomConnection:
    my_custom_connection = CustomConnection(
        {
            "api-key" : "my-api-key",
            "api-secret" : "my-api-secret",
            "api-url" : "my-api-url"
        }
    )
    return my_custom_connection


class TestTool:
    def test_generate(self, my_custom_connection):
        result = generate(my_custom_connection, input_text="Microsoft")
        assert result == "Hello Microsoft"


# Run the unit tests
if __name__ == "__main__":
    unittest.main()