# Courses App

App responsible for managing courses offered by Bioparque Macuco.

## Model: Course

| Field | Type | Description |
|---|---|---|
| `id` | BigAutoField | Primary key (auto-generated) |
| `name` | CharField(255) | Course name |
| `description` | TextField | Detailed description |
| `duration` | IntegerField | Duration (in hours) |
| `price` | DecimalField(10,2) | Price (R$) |
| `is_active` | BooleanField | Whether the course is active (default: True) |
| `created_at` | DateTimeField | Creation timestamp (auto) |
| `updated_at` | DateTimeField | Last update timestamp (auto) |
