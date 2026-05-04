# Courses App

App responsible for managing the courses offered by Bioparque Macuco and the
specific class sessions (lessons / "turmas") in which each course is
delivered. Provides the data, admin and public read-only API used by the site
to list and detail courses to visitors.

## Models

### `Course`

A course represents a recurring offering of the park (e.g. "Manejo de aves").
It is enrollment-agnostic: students do not enroll in a `Course` directly,
they enroll in a `Lesson` (see below).

| Field | Type | Description |
|---|---|---|
| `id` | BigAutoField | Primary key (auto-generated). |
| `name` | CharField(255) | Course name, displayed on cards and the detail page. |
| `description` | TextField | Short description (1–2 paragraphs), shown on cards and at the top of the detail page. |
| `syllabus` | TextField (blank) | Detailed program / outline. Accepts Markdown (rendered on the front via `marked`). |
| `duration_hours` | IntegerField | Total course duration, in hours. |
| `price` | DecimalField(10,2) | Price in BRL. |
| `status` | CharField(10) | `'active'` or `'inactive'`. Public API hides inactive courses by default. |
| `image` | ImageField (optional) | Cover image (uploaded to `media/courses/`). Used on cards and the detail page; falls back to a placeholder if absent. |
| `min_age` | PositiveIntegerField (optional) | Minimum age required to enroll. Empty means no restriction. |
| `has_certificate` | BooleanField (default `True`) | Whether the course issues a certificate. |
| `donation_kg_required` | DecimalField(6,2) (optional) | Kilograms of pet food required as part of the payment. Empty means no donation required. |
| `instructors` | ManyToMany → `accounts.Instructor` | Instructors who teach this course. At least one is required (validated in the admin form). |
| `created_at` | DateTimeField | Creation timestamp (auto). |
| `updated_at` | DateTimeField | Last update timestamp (auto). |

### `Lesson`

A `Lesson` is a concrete dated session of a `Course` that students can
enroll in. The model is named `Lesson` internally but is exposed in the UI
as "Turma".

| Field | Type | Description |
|---|---|---|
| `id` | BigAutoField | Primary key. |
| `course` | ForeignKey → `Course` (PROTECT) | The course this lesson belongs to. |
| `start_date` | DateField | Date the lesson takes place. |
| `start_time` | TimeField | Start time. |
| `end_time` | TimeField | End time. |
| `capacity` | IntegerField | Maximum number of students allowed. |
| `instructor` | ForeignKey → `accounts.Instructor` (PROTECT) | Instructor in charge of this specific lesson. |
| `label` | CharField(100, blank) | Optional friendly name for the class (e.g. "Turma Escola X"). |
| `is_private` | BooleanField (default `False`) | When `True`, the lesson is hidden from the public listing and only an admin can enroll students into it. |

## Public API

The app exposes a read-friendly REST API (Django REST Framework) under
`/api/`. Anonymous users can list and retrieve; only authenticated users can
write (in practice, content management is done through the Django admin).

| Method | Endpoint | Notes |
|---|---|---|
| `GET` | `/api/courses/` | List of courses. By default returns only `status='active'`; pass `?status=inactive` to override. Ordered by the date of the next upcoming public lesson (courses with no upcoming lesson appear last). Accepts `?ordering=name`, `?ordering=price`, `?ordering=duration_hours`, `?ordering=created_at` (use `-` prefix for descending). |
| `GET` | `/api/courses/<id>/` | Detail of a single course, including its instructors and the next upcoming public lesson (`next_lesson`). |
| `GET` | `/api/lessons/` | List of lessons. Hides `is_private=True` from anonymous callers. Supports `?course=<id>` to filter by course. |
| `GET` | `/api/lessons/<id>/` | Detail of a single lesson. |

The `CourseSerializer` exposes the cover `image` URL, the instructors
(through `accounts.serializers.InstructorPublicSerializer`) and a
computed `next_lesson` field built from a prefetched queryset, so the
listing page can render a card with the next available date without
issuing N+1 queries.

## Front-end consumption

The public site consumes this API from two places:

- **Home page** — `static/js/courses.js` populates `#featured-courses-grid`
  with up to 3 cards (via `data-limit="3"`).
- **Courses page** (`/cursos/`) — same script, full list, no limit.
- **Course detail page** (`/cursos/<id>/`) — `static/js/course-detail.js`
  fetches `/api/courses/<id>/` and renders the syllabus (Markdown), the
  next lesson card and the CTA pointing to the enrollment flow.

## Admin

`CourseAdmin` and `LessonAdmin` are configured with grouped `fieldsets`,
search and filtering. The course form enforces the "at least one
instructor" rule at form-clean time, since Django saves M2M relations
after the model's `clean()` runs.
