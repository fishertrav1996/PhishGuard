# PhishGuard Documentation

This directory contains all technical documentation, architecture decisions, and implementation guides for the PhishGuard project.

## 📚 Documentation Index

### Project Planning
- **[REVENUE_FEATURES_ROADMAP.md](REVENUE_FEATURES_ROADMAP.md)** - Complete roadmap for building revenue-ready features (Phases 1-3)
- **[SMTP_STRATEGY.md](SMTP_STRATEGY.md)** - ⭐ **NEW** SMTP provider strategy for phishing simulation email delivery (Amazon SES recommended)

### Project Organization
- **[PROJECT_ORGANIZATION.md](PROJECT_ORGANIZATION.md)** - Guidelines for organizing files, docs, and tests in this project

### Architecture & Design
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Complete system architecture with tracking flow diagrams, database schema, and component interactions
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Overview of core features, models, views, and workflows

### Feature Implementation Guides
- **[MEMBERSHIP_IMPLEMENTATION.md](MEMBERSHIP_IMPLEMENTATION.md)** - Organization membership system with role-based access control (OWNER, ADMIN, MEMBER, BILLING)
- **[CAMPAIGN_SETUP.md](CAMPAIGN_SETUP.md)** - Guide for setting up and running phishing simulation campaigns
- **[UUID_IMPLEMENTATION.md](UUID_IMPLEMENTATION.md)** - UUID-based tracking system for campaigns and organizations

### Testing & Quick Reference
- **[QUICK_TEST.md](QUICK_TEST.md)** - Quick testing procedures and verification steps

## 🗂️ Organization

All implementation documentation generated during development should be placed in this directory. This keeps the root project directory clean and makes documentation easy to find.

### Naming Convention
- Use descriptive UPPERCASE names with underscores: `FEATURE_NAME_IMPLEMENTATION.md`
- Include dates for major milestones if needed: `FEATURE_NAME_LAUNCH_2026_01.md`
- Architecture docs: `ARCHITECTURE_*.md`
- Feature guides: `*_IMPLEMENTATION.md`
- User guides: `*_GUIDE.md` or `*_SETUP.md`

## 🔄 Maintenance

Keep this README updated when adding new documentation files. List them in the appropriate category above with a brief description.
