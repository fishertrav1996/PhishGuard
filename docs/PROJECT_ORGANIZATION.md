# Project Organization Guidelines

This document defines how files should be organized in the PhishGuard project.

## 📁 Directory Structure

### `/docs` - Documentation
**Purpose:** All technical documentation, architecture decisions, and implementation guides

**What goes here:**
- Architecture diagrams and system design docs
- Implementation summaries for major features
- Setup and configuration guides
- API documentation
- Design decisions and rationale

**Naming conventions:**
- `ARCHITECTURE*.md` - Architecture and system design
- `*_IMPLEMENTATION.md` - Feature implementation guides
- `*_SETUP.md` or `*_GUIDE.md` - User/developer guides
- `README.md` - Documentation index (always keep updated)

**Examples:**
- `docs/ARCHITECTURE.md`
- `docs/MEMBERSHIP_IMPLEMENTATION.md`
- `docs/CAMPAIGN_SETUP.md`

---

### `/tests` - Test Scripts & Utilities
**Purpose:** Standalone test scripts, data generation utilities, and validation tools

**What goes here:**
- System validation scripts
- Integration test scripts
- Data generation utilities
- Test fixtures and sample data creators
- Performance/load testing scripts

**Naming conventions:**
- `test_*.py` - Test and validation scripts
- `create_*.py` - Data generation utilities
- `load_*.py` - Data loading scripts
- `README.md` - Test index with run instructions

**Examples:**
- `tests/test_membership.py`
- `tests/create_sample_templates.py`

**Note:** Traditional Django unit tests remain in each app's `tests.py` file:
- `accounts/tests.py`
- `campaigns/tests.py`
- `orgs/tests.py`

---

### App-Specific Documentation
**Purpose:** Documentation specific to a single app

**Location:** `<app_name>/README.md` or `<app_name>/docs/`

**Examples:**
- `campaigns/README.md` - Campaign-specific documentation
- `orgs/EMPLOYEE_MANAGEMENT.md` - Org-specific feature docs

---

## 🗂️ File Organization Rules

### Root Level - Clean & Minimal
Only these files should be at root level:
- `manage.py` - Django management
- `requirements.txt` - Python dependencies
- `package.json` - Node dependencies (if needed)
- `README.md` - Project overview with links to `/docs`
- `.gitignore`, `.env`, etc. - Config files
- `db.sqlite3` - Database (dev only)

### What NOT to Put at Root
- ❌ Implementation docs (→ `/docs`)
- ❌ Test scripts (→ `/tests`)
- ❌ Sample data generators (→ `/tests`)
- ❌ Utility scripts (→ `/tests` or app-specific)

---

## 📝 When Creating New Content

### New Feature Implementation?
1. Document in `/docs/<FEATURE>_IMPLEMENTATION.md`
2. Update `/docs/README.md` index
3. Create tests in `/tests/test_<feature>.py`
4. Update `/tests/README.md` with run instructions

### New Test Script?
1. Create in `/tests/test_<name>.py`
2. Add docstring explaining what it tests
3. Update `/tests/README.md` index
4. Make it runnable: `python manage.py shell < tests/test_<name>.py`

### New Architecture Decision?
1. Document in `/docs/ARCHITECTURE_<topic>.md`
2. Update main `/docs/ARCHITECTURE.md` if needed
3. Update `/docs/README.md` index

---

## 🔍 Quick Reference

| Content Type | Location | Example |
|--------------|----------|---------|
| Feature implementation docs | `/docs/` | `MEMBERSHIP_IMPLEMENTATION.md` |
| Architecture & design | `/docs/` | `ARCHITECTURE.md` |
| Setup guides | `/docs/` | `CAMPAIGN_SETUP.md` |
| Test scripts | `/tests/` | `test_membership.py` |
| Sample data generators | `/tests/` | `create_sample_templates.py` |
| Django unit tests | `<app>/tests.py` | `campaigns/tests.py` |
| App-specific docs | `<app>/README.md` | `campaigns/README.md` |

---

## ✅ Benefits of This Structure

1. **Clean Root** - Easy to see main project structure
2. **Easy Discovery** - Docs and tests in predictable locations
3. **Scalable** - Can add many docs/tests without cluttering root
4. **Conventional** - Follows common open-source practices
5. **IDE-Friendly** - Standard structure works well with tools

---

## 🔄 Maintenance

- Keep `/docs/README.md` updated with all documentation files
- Keep `/tests/README.md` updated with all test scripts
- Review root directory monthly - move any misplaced files
- When archiving old docs, create `/docs/archive/` subdirectory
