# Database Schema

This folder contains the database modeling for the Macuco Web App, written in [DBML](https://dbml.dbdiagram.io/docs/) (Database Markup Language).

## How to visualize

**Option A: In the browser**

Copy the contents of [`macuco.dbml`](macuco.dbml) and paste it into [dbdiagram.io](https://dbdiagram.io) to generate an interactive ERD (Entity-Relationship Diagram).

**Option B: In the IDE (VSCode / Cursor)**

Install the [DBML Live Preview](https://marketplace.visualstudio.com/items?itemName=bocovo.dbml-erd-visualizer) extension, then open the `.dbml` file and use the preview command to visualize the diagram directly in the editor.

## Entities overview

### Team (internal access)

| Table | Description |
|---|---|
| **User** | Django's native `auth_user` table. Exclusive to staff members. |
| **Employee** | Extends User with role and hire date (1:1 relationship). |
| **Instructor** | Professional profile for instructors. Personal data (name, email) come from Employee → User. |

### Courses

| Table | Description |
|---|---|
| **Course** | Available courses with name, description, full syllabus (Markdown), duration, price, status, optional cover image (uploaded via admin into `MEDIA_ROOT/courses/`), minimum age, certificate flag and required food-donation amount. Has a many-to-many relationship with **Instructor** (a course is taught by 1+ instructors). |
| **CourseInstructor** | Join table for the Course ↔ Instructor M2M. Each course must have at least 1 instructor (validated at the model level). |
| **Lesson** | Specific lesson sessions for a course, with date, time, capacity and assigned instructor (1 instructor teaches each session). Supports an optional `label` (custom name, e.g. closed school groups) and `is_private` flag (hidden from public listing, admin-only enrollment). |

### Students, Enrollments & Payments

| Table | Description |
|---|---|
| **Student** | Visitors/quick-purchase students. No panel access. Identified by CPF and email. Stores `birth_date` (age is derived, used for course age restrictions and minor identification). |
| **Enrollment** | Links a student to a lesson, with status tracking (pending/approved/rejected/expired). Pending enrollments have an `expires_at` deadline; if not paid by then, status auto-changes to `expired` and the slot is released. |
| **Payment** | Payment details for an enrollment. Supports multiple methods including donations (kg). When the method is `donation_item` or `hybrid`, the `donation_type` (dog/cat/bird food) is required for record-keeping. |

## Enums

| Enum | Values |
|---|---|
| `enrollment_status` | pending, approved, rejected, expired |
| `payment_status` | pending, confirmed |
| `payment_origin` | online, in_person |
| `payment_method` | credit_card, pix, cash, donation_item, hybrid, scholarship |
| `course_status` | active, inactive |
| `donation_type` | dog_food, cat_food, bird_food |
