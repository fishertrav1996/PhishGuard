# PhishGuard Tracking System Architecture

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PHISHGUARD TRACKING FLOW                        │
└─────────────────────────────────────────────────────────────────────┘

1. CAMPAIGN CREATION
   ┌──────────────┐
   │ Admin/User   │
   └──────┬───────┘
          │ Creates campaign
          ▼
   ┌──────────────────────┐
   │   Campaign Model     │
   │  - name              │
   │  - organization      │
   │  - email_template    │
   │  - status: DRAFT     │
   └──────┬───────────────┘
          │ For each selected employee
          ▼
   ┌────────────────────────────┐
   │   CampaignTarget Model     │
   │  - campaign (FK)           │
   │  - employee (FK)           │
   │  - unique_tracking_token   │  ◄── UUID4 generated
   │  - status: PENDING         │
   └────────────────────────────┘


2. EMAIL SENDING
   ┌──────────────┐
   │ User clicks  │
   │ "Send        │
   │  Campaign"   │
   └──────┬───────┘
          │
          ▼
   ┌─────────────────────────────────────────────┐
   │  For each CampaignTarget:                   │
   │                                             │
   │  1. Get unique_tracking_token               │
   │     Example: a3f5e7d9-1234-5678-90ab...    │
   │                                             │
   │  2. Build tracking URL:                     │
   │     /campaigns/track/{token}/               │
   │                                             │
   │  3. Replace {{tracking_link}} in template   │
   │                                             │
   │  4. Send email via SMTP                     │
   │                                             │
   │  5. Update CampaignTarget:                  │
   │     - sent_at = now()                       │
   │     - status = SENT                         │
   └─────────────────────────────────────────────┘
          │
          ▼
   ┌──────────────────┐
   │  Email Inbox     │
   │  ┌─────────────┐ │
   │  │ Subject: ⚠️ │ │
   │  │ Password... │ │
   │  │             │ │
   │  │ [Click me]  │ │◄── Contains unique tracking link
   │  └─────────────┘ │
   └──────────────────┘


3. LINK CLICK TRACKING
   ┌──────────────┐
   │ Employee     │
   │ clicks link  │
   └──────┬───────┘
          │ HTTP GET request
          │ /campaigns/track/a3f5e7d9-1234-5678-90ab.../
          ▼
   ┌─────────────────────────────────────────────┐
   │  track_click(request, token) view           │
   │                                             │
   │  1. Look up CampaignTarget by token         │
   │     CampaignTarget.objects.get(             │
   │         unique_tracking_token=token         │
   │     )                                       │
   │                                             │
   │  2. Record click (if not already clicked):  │
   │     - link_clicked_at = now()               │
   │     - status = CLICKED                      │
   │     - save()                                │
   │                                             │
   │  3. Render educational page                 │
   └─────────────────────────────────────────────┘
          │
          ▼
   ┌──────────────────────────────┐
   │  Educational Landing Page    │
   │  ┌─────────────────────────┐ │
   │  │ ⚠️ This Was A           │ │
   │  │ Phishing Simulation     │ │
   │  │                         │ │
   │  │ Hello {employee_name}!  │ │
   │  │                         │ │
   │  │ You clicked on a link   │ │
   │  │ in: {campaign_name}     │ │
   │  │                         │ │
   │  │ [What is phishing?]     │ │
   │  │ [How to spot it]        │ │
   │  │ [What to do]            │ │
   │  └─────────────────────────┘ │
   └──────────────────────────────┘


4. ANALYTICS & REPORTING
   ┌──────────────┐
   │ User views   │
   │ campaign     │
   └──────┬───────┘
          │
          ▼
   ┌─────────────────────────────────────────────┐
   │  Campaign Detail View                       │
   │                                             │
   │  Statistics:                                │
   │  ┌────────────────────────────────────────┐ │
   │  │ Total Targets: 50                      │ │
   │  │ Emails Sent: 50                        │ │
   │  │ Links Clicked: 23                      │ │
   │  │ Click Rate: 46%                        │ │
   │  └────────────────────────────────────────┘ │
   │                                             │
   │  Per-Employee Results:                      │
   │  ┌────────────────────────────────────────┐ │
   │  │ Employee    | Status  | Clicked At    │ │
   │  │─────────────┼─────────┼───────────────│ │
   │  │ John Doe    | CLICKED | Dec 17, 14:23 │ │
   │  │ Jane Smith  | SENT    | -             │ │
   │  │ Bob Jones   | CLICKED | Dec 17, 09:15 │ │
   │  └────────────────────────────────────────┘ │
   └─────────────────────────────────────────────┘
```

## Database Schema

```
┌──────────────────────────┐
│   EmailTemplate          │
├──────────────────────────┤
│ id (PK)                  │
│ name                     │
│ subject_line             │
│ body_html                │◄── Contains {{tracking_link}}
│ sender_name              │
│ sender_email             │
│ difficulty_level         │
│ phishing_indicators      │
└──────────────────────────┘
          △
          │ FK
          │
┌─────────┴────────────────┐
│   Campaign               │
├──────────────────────────┤
│ id (PK)                  │
│ organization (FK)        │
│ name                     │
│ description              │
│ status                   │
│ email_template (FK)      │─────┐
│ created_by (FK to User)  │     │
│ created_at               │     │
│ updated_at               │     │
└──────────────────────────┘     │
          △                      │
          │ FK                   │
          │                      │
┌─────────┴────────────────┐     │
│   CampaignTarget         │     │
├──────────────────────────┤     │
│ id (PK)                  │     │
│ campaign (FK)            │─────┘
│ employee (FK)            │
│ unique_tracking_token    │◄── UUID4 (unique, indexed)
│ sent_at                  │
│ email_opened_at          │
│ link_clicked_at          │
│ reported_at              │
│ status                   │
└──────────────────────────┘
          │ FK
          ▼
┌──────────────────────────┐
│   Employee (orgs app)    │
├──────────────────────────┤
│ id (PK)                  │
│ organization (FK)        │
│ first_name               │
│ last_name                │
│ email                    │◄── Unique (email sent here)
│ role                     │
└──────────────────────────┘
```

## Security Model

```
┌─────────────────────────────────────────────────────────┐
│                   SECURITY LAYERS                       │
└─────────────────────────────────────────────────────────┘

Layer 1: Authentication
┌────────────────────────────────────────────┐
│ @login_required decorator                  │
│ - All campaign management views            │
│ - Only authenticated users                 │
└────────────────────────────────────────────┘

Layer 2: Ownership Verification
┌────────────────────────────────────────────┐
│ if campaign.organization.owner != user:    │
│     return error                           │
│ - Users can only manage their own org's   │
│   campaigns                                │
└────────────────────────────────────────────┘

Layer 3: Unique Tokens
┌────────────────────────────────────────────┐
│ unique_tracking_token = uuid.uuid4()       │
│ - 128-bit random UUID                      │
│ - Cryptographically secure                 │
│ - 5.3 x 10^36 possible combinations        │
│ - Impossible to guess or brute force       │
└────────────────────────────────────────────┘

Layer 4: CSRF Protection
┌────────────────────────────────────────────┐
│ All form submissions: CSRF token required  │
│ Exception: track_click (from email)        │
│ - @csrf_exempt needed for email links     │
│ - Safe because token is secret & unique   │
└────────────────────────────────────────────┘

Layer 5: Database Constraints
┌────────────────────────────────────────────┐
│ unique_together = ['campaign', 'employee'] │
│ - Prevents duplicate targets               │
│ - Each employee only once per campaign     │
└────────────────────────────────────────────┘
```

## Example Tracking URLs

```
Campaign: "Q4 Security Training"
Template: "Urgent Password Reset"
Employees: 3

CampaignTarget Records Created:
┌──────────────┬───────────────┬──────────────────────────────────────┐
│ Employee     │ Status        │ Tracking Token                       │
├──────────────┼───────────────┼──────────────────────────────────────┤
│ alice@co.com │ PENDING       │ a3f5e7d9-1234-5678-90ab-cdef12345678 │
│ bob@co.com   │ PENDING       │ b1c2d3e4-5678-90ab-cdef-123456789abc │
│ carol@co.com │ PENDING       │ c7d8e9f0-90ab-cdef-1234-56789abcdef0 │
└──────────────┴───────────────┴──────────────────────────────────────┘

Tracking URLs Generated:
┌──────────────┬─────────────────────────────────────────────────────┐
│ alice@co.com │ /campaigns/track/a3f5e7d9-1234-5678-90ab-.../       │
│ bob@co.com   │ /campaigns/track/b1c2d3e4-5678-90ab-cdef-.../       │
│ carol@co.com │ /campaigns/track/c7d8e9f0-90ab-cdef-1234-.../       │
└──────────────┴─────────────────────────────────────────────────────┘

Each URL is unique and maps back to ONE employee in ONE campaign.
If Alice clicks, we know:
  - WHO: alice@co.com
  - WHEN: timestamp recorded
  - WHICH CAMPAIGN: Q4 Security Training
```

## Technology Stack

```
┌─────────────────────────────────────────────┐
│ Frontend                                    │
│ - TailwindCSS (styling)                     │
│ - DaisyUI (components)                      │
│ - HTMX (dynamic interactions)               │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│ Django (Backend)                            │
│ - Views: Campaign management                │
│ - Models: Campaign, EmailTemplate, Target   │
│ - URLs: Routing                             │
│ - Authentication: User sessions             │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│ Email (SMTP)                                │
│ - Gmail (testing): 100/day limit            │
│ - Production: SES/SendGrid/Postmark         │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│ Database (SQLite)                           │
│ - EmailTemplate table                       │
│ - Campaign table                            │
│ - CampaignTarget table (tracking)           │
│ - Employee table (from orgs app)            │
└─────────────────────────────────────────────┘
```

## Key Design Decisions

### Why UUID4 for Tracking?
✅ Cryptographically secure random
✅ No sequential patterns
✅ Impossible to guess other tokens
✅ Built-in Django field type
✅ URL-safe
❌ Longer URLs (acceptable tradeoff)

### Why CSRF Exempt for Tracking?
✅ Email links can't include CSRF tokens
✅ Token itself provides security
✅ Read-only operation (just records timestamp)
✅ No state change requiring authentication
❌ Slight increase in attack surface (mitigated by token secrecy)

### Why Separate CampaignTarget Model?
✅ Many-to-many with extra fields
✅ Tracks individual interactions
✅ Unique token per employee per campaign
✅ Allows multiple campaigns for same employee
✅ Clean separation of concerns

### Why Email Templates?
✅ Reusable across campaigns
✅ Consistent phishing scenarios
✅ Easy to test different difficulty levels
✅ Centralized management
✅ Professional quality control
