# PhishGuard Test Scripts

This directory contains test scripts, data generation utilities, and validation tools for the PhishGuard project.

## 🧪 Test Files

### System Tests
- **[test_membership.py](test_membership.py)** - Validates the organization membership system including roles, permissions, and multi-admin functionality

### Utilities
- **[create_sample_templates.py](create_sample_templates.py)** - Generates sample phishing email templates for testing and development

## 🚀 Running Tests

### Membership System Test
```bash
cd /home/fishertrav/Projects/PhishGuard
source venv/bin/activate
python manage.py shell < tests/test_membership.py
```

### Create Sample Templates
```bash
python manage.py shell < tests/create_sample_templates.py
```

## 📝 Adding New Tests

When creating new test scripts:

1. **Naming Convention:** Use `test_*.py` for test files, `create_*.py` for data generation
2. **Documentation:** Add a docstring at the top explaining what the test validates
3. **Output:** Include clear success/failure indicators (✓/❌)
4. **Independence:** Tests should be runnable independently and not depend on specific database state
5. **Update Index:** Add new test files to this README with descriptions

## 🏗️ Test Organization

```
tests/
├── README.md                      # This file
├── test_membership.py             # Membership system validation
├── create_sample_templates.py     # Sample data generation
└── [future test files]            # Additional tests as needed
```

## ✅ Best Practices

- **Idempotent:** Tests should be runnable multiple times without side effects
- **Clear Output:** Use formatting and emoji for easy scanning of results
- **Cleanup:** Clean up test data at the end (or use transactions)
- **Documentation:** Explain what each test validates and expected outcomes

## 🔄 Django Unit Tests

For traditional Django unit tests, use the standard `tests.py` files in each app:
- `accounts/tests.py`
- `campaigns/tests.py`
- `orgs/tests.py`
- `core/tests.py`

Run Django unit tests with:
```bash
python manage.py test
```

This `/tests` directory is for standalone test scripts and utilities that don't fit the standard Django test framework.
