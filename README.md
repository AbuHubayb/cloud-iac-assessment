# Cloud IaC Analyzer

A simple Python tool that compares **Infrastructure-as-Code (IaC) resources** with **actual Cloud resources** to detect configuration drift.

The analyzer reads two JSON files:

- `cloud_resources.json` → represents the **actual infrastructure running in the cloud**
- `iac_resources.json` → represents the **desired infrastructure defined in code**

It then generates a report highlighting differences between the two states.

---

# Features

The analyzer detects the following infrastructure states:

### Match
Resource exists in both Cloud and IaC and **all properties match**.

Example:

Cloud
```
{ "id": "vm-1", "cpu": 2 }
```

IaC
```
{ "id": "vm-1", "cpu": 2 }
```

Result: `Match`

---

### Modified
Resource exists in both places but **one or more properties differ**.

Example:

Cloud
```
{ "id": "vm-2", "cpu": 4 }
```

IaC
```
{ "id": "vm-2", "cpu": 2 }
```

Result: `Modified`

The report will show exactly **which property changed**.

---

### Missing
Resource exists in **Cloud but not in IaC**.

Example:

Cloud
```
{ "id": "vm-3" }
```

IaC

```
(no matching resource)
```

Result: `Missing`

---

### Orphaned
Resource exists in **IaC but not in the Cloud**.

Example:

IaC
```
{ "id": "vm-4" }
```

Cloud

```
(no matching resource)
```

Result: `Orphaned`

---

# Key Capabilities

The analyzer supports:

- Recursive comparison of **nested dictionaries**
- Detection of **array differences with index notation**
- Detection of **properties present in IaC but missing in Cloud**
- Detection of **properties present in Cloud but missing in IaC**
- Detailed change logs with **dot notation**

Example drift:

```
tags.env
network.subnets[0].cidr
rules[1].port
```

---

# Project Structure

```
cloud-iac-analyzer
│
├── main.py
├── test_main.py
├── requirements.txt
│
├── cloud_resources.json
├── iac_resources.json
│
├── report.json
├── Dockerfile
├── init-s3.sh
│
└── README.md
```

---

# Installation

### 1. Clone repository

```
git clone <repo-url>
cd cloud-iac-analyzer
```

---

### 2. Create virtual environment

```
python -m venv venv
```

Activate:

Windows
```
venv\Scripts\activate
```

Linux / Mac
```
source venv/bin/activate
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

# Requirements

Example `requirements.txt`

```
boto3==1.34.162
pytest==8.3.5
pytest-cov==5.0.0
```

---

# Running the Analyzer

Run the analyzer:

```
python main.py
```

The script will generate:

```
report.json
```

---

# Example Output

```
[
  {
    "CloudResourceItem": {"id": "vm-1"},
    "IacResourceItem": {"id": "vm-1"},
    "State": "Match",
    "ChangeLog": []
  },
  {
    "CloudResourceItem": {"id": "vm-2"},
    "IacResourceItem": {"id": "vm-2"},
    "State": "Modified",
    "ChangeLog": [
      {
        "KeyName": "cpu",
        "CloudValue": 4,
        "IacValue": 2
      }
    ]
  }
]
```

---

# Running Tests

Run all tests:

```
pytest -v
```

Expected result:

```
collected 5 items

test_main.py::test_match PASSED
test_main.py::test_missing PASSED
test_main.py::test_modified PASSED
test_main.py::test_nested_property PASSED
test_main.py::test_array_property PASSED
```