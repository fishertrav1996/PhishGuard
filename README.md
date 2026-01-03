# PhishGuard – Healthcare Phishing Simulation & Security Training Platform

PhishGuard is a web-based platform designed to help healthcare organizations strengthen their security posture against phishing attacks—the leading cause of ransomware incidents in the healthcare industry.

This project aims to provide:

- **Phishing simulation tools**
- **Security awareness training modules**
- **Employee performance tracking**
- **Organization-level reporting dashboards**

This is the early MVP version and will evolve as development continues.

## 📂 Project Structure

```
PhishGuard/
├── docs/                      # All documentation and implementation guides
├── tests/                     # Test scripts and utilities
├── accounts/                  # User authentication app
├── campaigns/                 # Phishing campaign management
├── core/                      # Core app (home, about, FAQ)
├── orgs/                      # Organizations and employees
├── PhishGuard/               # Django project settings
├── manage.py                 # Django management script
└── requirements.txt          # Python dependencies
```

## 📚 Documentation

All technical documentation is organized in the [`/docs`](docs/) directory:

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md)
- [Membership System](docs/MEMBERSHIP_IMPLEMENTATION.md)
- [Campaign Setup Guide](docs/CAMPAIGN_SETUP.md)

See [`docs/README.md`](docs/README.md) for the complete documentation index.

## 🧪 Testing

Test scripts and utilities are in the [`/tests`](tests/) directory. See [`tests/README.md`](tests/README.md) for details on running tests.