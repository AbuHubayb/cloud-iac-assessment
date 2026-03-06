import json
from main import analyze_files


# ------------------------------------
# Test 1: Match state
# ------------------------------------

def test_match():

    cloud = [
        {"id": "1", "name": "server1", "region": "us-east", "size": "small"}
    ]

    iac = [
        {"id": "1", "name": "server1", "region": "us-east", "size": "small"}
    ]

    result = analyze_files(cloud, iac)

    assert result[0]["State"] == "Match"


# ------------------------------------
# Test 2: Missing state
# ------------------------------------

def test_missing():

    cloud = [
        {"id": "2", "name": "server2", "region": "us-east", "size": "medium"}
    ]

    iac = []   # nothing defined in IaC

    result = analyze_files(cloud, iac)

    assert result[0]["State"] == "Missing"


# ------------------------------------
# Test 3: Modified state
# ------------------------------------

def test_modified():

    cloud = [
        {"id": "3", "name": "server3", "region": "us-east", "size": "large"}
    ]

    iac = [
        {"id": "3", "name": "server3", "region": "eu-west", "size": "large"}
    ]

    result = analyze_files(cloud, iac)

    assert result[0]["State"] == "Modified"


# ------------------------------------
# Test 4: Nested properties
# ------------------------------------

def test_nested_property():

    cloud = [
        {
            "id": "4",
            "name": "server4",
            "config": {"cpu": 2, "memory": 4}
        }
    ]

    iac = [
        {
            "id": "4",
            "name": "server4",
            "config": {"cpu": 2, "memory": 8}
        }
    ]

    result = analyze_files(cloud, iac)

    assert result[0]["State"] == "Modified"


# ------------------------------------
# Test 5: Arrays / lists
# ------------------------------------

def test_array_property():

    cloud = [
        {
            "id": "5",
            "name": "server5",
            "tags": ["web", "production"]
        }
    ]

    iac = [
        {
            "id": "5",
            "name": "server5",
            "tags": ["web", "staging"]
        }
    ]

    result = analyze_files(cloud, iac)

    assert result[0]["State"] == "Modified"