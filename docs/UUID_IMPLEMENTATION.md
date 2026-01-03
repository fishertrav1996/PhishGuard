# UUID Implementation - Security Enhancement

## What Changed

Successfully migrated from integer IDs to UUIDs for Organization and Campaign models to prevent enumeration attacks and enhance security.

## Changes Made

### 1. Models
- **Organization**: Added `uuid` field (UUIDField, unique, indexed)
- **Campaign**: Added `uuid` field (UUIDField, unique, indexed)

### 2. Migrations
Created 4-step migration process:
1. Add nullable UUID field
2. Populate existing records with UUIDs
3. Make UUID non-nullable and unique
4. Applied successfully to database

### 3. URL Patterns

**Before:**
```python
/orgs/<int:org_id>/employees/
/campaigns/<int:campaign_id>/
```

**After:**
```python
/orgs/<uuid:org_uuid>/employees/
/campaigns/<uuid:campaign_uuid>/
```

### 4. Views Updated

**orgs/views.py:**
- `add_employee_view(org_uuid)`
- `upload_employees_csv_view(org_uuid)`
- `list_employees_view(org_uuid)`
- `delete_employee_view(org_uuid, employee_id)`

**campaigns/views.py:**
- `campaign_detail(campaign_uuid)`
- `send_campaign(campaign_uuid)`

### 5. Templates Updated

All URL references changed from `.id` to `.uuid`:
- `campaigns/campaign_list.html`
- `campaigns/create_campaign.html`
- `campaigns/campaign_detail.html`
- `campaigns/send_campaign.html`
- `orgs/add_employee.html`
- `orgs/list_employees.html`
- `orgs/upload_employees_csv.html`

## Security Benefits

✅ **Prevents Enumeration**: Can't guess other organization/campaign IDs  
✅ **Information Disclosure**: Attackers can't determine total count of orgs/campaigns  
✅ **Unpredictable**: 5.3 × 10³⁶ possible combinations per record  
✅ **Authorization Still Required**: UUID alone doesn't grant access - must still pass ownership checks

## Example URLs

**Before:**
```
/orgs/1/employees/
/orgs/2/employees/
/campaigns/5/
```

**After:**
```
/orgs/a3f5e7d9-1234-5678-90ab-cdef12345678/employees/
/orgs/b1c2d3e4-5678-90ab-cdef-123456789abc/employees/
/campaigns/c7d8e9f0-90ab-cdef-1234-56789abcdef0/
```

## Breaking Changes

⚠️ **All existing URLs are now invalid**  
- Any bookmarked URLs will need to be updated
- Old integer-based URLs will return 404
- This is acceptable since the app is in development

## Testing

✅ Django system check passed with no issues  
✅ All migrations applied successfully  
✅ Database constraints in place (unique, indexed)

## Next Steps

1. Test all org/campaign functionality with new UUIDs
2. Verify HTMX delete still works correctly
3. Check campaign creation flow
4. Test employee management with UUID-based URLs

## Important Notes

- UUIDs are **not secrets** - they're identifiers
- Security still comes from `@login_required` and ownership checks
- Never use UUID alone for authorization
- UUIDs are exposed in URLs, logs, browser history - this is normal and acceptable
