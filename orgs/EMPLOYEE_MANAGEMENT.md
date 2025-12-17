# Employee Management Feature

## Overview
Organization owners can now add employees to their organizations through two methods:
1. **Single Employee Form** - Add one employee at a time
2. **CSV Bulk Upload** - Upload multiple employees at once

## URLs

### For organization with ID = 1:
- **List Employees**: `/orgs/1/employees/`
- **Add Single Employee**: `/orgs/1/employees/add/`
- **Upload CSV**: `/orgs/1/employees/upload/`

## CSV Upload Format

### Required Columns:
- `first_name` - Employee's first name (required)
- `last_name` - Employee's last name (required)
- `email` - Unique email address (required)

### Optional Columns:
- `role` - Must be one of: ADMIN, STAFF, OTHER (default: STAFF)
- `position` - Job title or position

### Example CSV:
```csv
first_name,last_name,email,role,position
John,Doe,john.doe@hospital.com,STAFF,Registered Nurse
Jane,Smith,jane.smith@hospital.com,ADMIN,IT Manager
Bob,Johnson,bob.j@hospital.com,STAFF,Pharmacist
```

### CSV Template
A template CSV file is available at `orgs/employee_template.csv`

## Security Features

1. **Ownership Verification**: Only organization owners can add employees to their organizations
2. **Email Uniqueness**: Each email must be unique across all employees
3. **File Validation**: CSV files are validated for:
   - File extension (.csv)
   - File size (max 5MB)
   - Required fields
   - Valid role values

## Error Handling

- Missing required fields are reported by row number
- Invalid roles are rejected with clear error messages
- Duplicate emails are handled gracefully with warnings
- All errors are displayed to the user before any data is saved

## Usage Example

### Single Employee
1. Navigate to `/orgs/{org_id}/employees/`
2. Click "Add Employee"
3. Fill out the form
4. Submit

### Bulk Upload
1. Prepare CSV file with proper format
2. Navigate to `/orgs/{org_id}/employees/`
3. Click "Upload CSV"
4. Select your CSV file
5. Upload - system will validate and import all employees

## Future Enhancements
- Employee edit/delete functionality
- Employee dashboard for self-service
- Export employees to CSV
- Advanced filtering and search
- Email verification for new employees
