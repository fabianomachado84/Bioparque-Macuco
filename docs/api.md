# API — Macuco Web App

REST API construída com **Django REST Framework**. Toda a API vive sob
o prefixo `/api/`. Os apps `courses`, `accounts`, `enrollments` e
`content` registram seus próprios routers e são incluídos em
`core/urls.py`:

```python
path('api/', include('courses.urls')),
path('api/', include('accounts.urls')),
path('api/', include('enrollments.urls')),
path('api/', include('content.urls')),
```

## Autenticação

A configuração global em `core/settings.py` define:

- **Esquema**: `TokenAuthentication` (token DRF, no header
  `Authorization: Token <chave>`).
- **Permissão padrão**: `IsAuthenticated` — qualquer endpoint que **não
  sobrescreva** a permissão exige token, inclusive para `GET`.

Endpoints que sobrescrevem a permissão para `IsAuthenticatedOrReadOnly`
(leitura aberta, escrita restrita):

- `/api/courses/`
- `/api/lessons/`
- `/api/banners/`

Endpoints que **mantêm** o default `IsAuthenticated` (precisam de
token até para listar):

- `/api/enrollments/`
- `/api/payments/`
- `/api/students/`
- `/api/employees/`
- `/api/instructors/`

### Como obter o token

Hoje **não existe um endpoint público de login**. O token é gerado via:

1. Django Admin (`/admin/authtoken/tokenproxy/` → "Add Token") para um
   `User` existente.
2. Comando de management: `python manage.py drf_create_token <username>`.
3. Shell:
   ```python
   from rest_framework.authtoken.models import Token
   from django.contrib.auth.models import User
   token, _ = Token.objects.get_or_create(user=User.objects.get(username='x'))
   print(token.key)
   ```

Para usar nas requisições:

```bash
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
     http://localhost:8000/api/students/
```

## Convenções

- **Formato**: JSON em entrada e saída.
- **Trailing slash**: obrigatório (`/api/courses/` em vez de `/api/courses`).
- **Paginação**: não há paginação configurada globalmente — listas
  retornam o array bruto. Para suportar tanto array quanto formato
  paginado (`{count, next, previous, results}`), os clientes JS do
  projeto fazem fallback (vide `static/js/courses.js`).
- **Status codes** padrão do DRF:
  - `200 OK` — leitura/atualização bem-sucedida.
  - `201 Created` — criação bem-sucedida.
  - `204 No Content` — deleção bem-sucedida.
  - `400 Bad Request` — payload inválido (corpo da resposta lista os
    erros de cada campo).
  - `401 Unauthorized` — falta o header `Authorization` ou token
    inválido.
  - `403 Forbidden` — autenticado, mas sem permissão (não é o caso
    nesse projeto hoje).
  - `404 Not Found`.
  - `405 Method Not Allowed` — verbo não suportado naquele endpoint
    (ex.: `POST /api/courses/`, hoje read-only).

## Recursos

### `Course` — `/api/courses/`

Catálogo público de cursos. **Read-only** via API (escrita pelo Django
Admin).

| Verbo | URL | Permissão |
|---|---|---|
| `GET` | `/api/courses/` | Pública |
| `GET` | `/api/courses/<id>/` | Pública |

#### Query params (lista)

- `?status=active|inactive` — Por padrão retorna apenas `active`.
  Passe `?status=inactive` ou `?status=` para ver inativos.
- `?ordering=<campo>` — Aceita `name`, `price`, `duration_hours`,
  `created_at`. Prefixe com `-` para ordem decrescente
  (ex.: `?ordering=-price`).
- Sem `ordering` explícito, a lista é ordenada pela data da próxima
  turma pública (cursos sem turma futura aparecem por último).

#### Schema de saída

```json
{
  "id": 1,
  "name": "Manejo de aves silvestres",
  "description": "Curso prático de manejo...",
  "syllabus": "## Programa\n- Anatomia\n- ...",
  "duration_hours": 8,
  "price": "120.00",
  "status": "active",
  "image": "http://localhost:8000/media/courses/aves.jpg",
  "min_age": 16,
  "has_certificate": true,
  "donation_kg_required": "2.00",
  "instructors": [
    { "id": 3, "name": "João Silva", "specialty": "Ornitologia" }
  ],
  "next_lesson": {
    "id": 7,
    "start_date": "2026-05-18",
    "start_time": "08:00:00",
    "end_time": "12:00:00",
    "capacity": 15
  }
}
```

### `Lesson` — `/api/lessons/`

Catálogo público de turmas. **Read-only**.

| Verbo | URL | Permissão |
|---|---|---|
| `GET` | `/api/lessons/` | Pública |
| `GET` | `/api/lessons/<id>/` | Pública |

#### Query params

- `?course=<id>` — filtra turmas de um curso específico.
- `?ordering=start_date|-start_date|start_time|-start_time`
  (default: `start_date,start_time`).

#### Regra automática

- Usuários **anônimos** nunca veem turmas com `is_private=True`.

#### Schema de saída

```json
{
  "id": 7,
  "course": 1,
  "start_date": "2026-05-18",
  "start_time": "08:00:00",
  "end_time": "12:00:00",
  "capacity": 15,
  "instructor": 3,
  "label": "Turma Escola Eusébio Farias",
  "is_private": false
}
```

### `Banner` — `/api/banners/`

Banners promocionais agendados, exibidos no carrossel da home.
**Read-only**.

| Verbo | URL | Permissão |
|---|---|---|
| `GET` | `/api/banners/` | Pública |
| `GET` | `/api/banners/<id>/` | Pública |

#### Regra automática

- A queryset usa `Banner.objects.visible_today()` — retorna apenas
  banners com `status='active'` e dentro da janela `start_date` /
  `end_date`. Banners fora do prazo nunca chegam ao front.

#### Schema de saída

```json
{
  "id": 4,
  "image": "http://localhost:8000/media/banners/feriado.jpg",
  "title": "Feriado prolongado no parque",
  "subtitle": "Programe sua visita com a família",
  "link_url": "https://example.com/agendar",
  "link_label": "AGENDAR",
  "display_order": 0
}
```

> O campo interno `name` (identificação no admin) é deliberadamente
> omitido — o serializer só expõe o que o front precisa.

### `Enrollment` — `/api/enrollments/`

CRUD de inscrições. **Exige token** (autenticado em todas as
operações, inclusive listagem).

| Verbo | URL |
|---|---|
| `GET`    | `/api/enrollments/` |
| `POST`   | `/api/enrollments/` |
| `GET`    | `/api/enrollments/<id>/` |
| `PUT`    | `/api/enrollments/<id>/` |
| `PATCH`  | `/api/enrollments/<id>/` |
| `DELETE` | `/api/enrollments/<id>/` |

#### Schema de entrada / saída

```json
{
  "id": 12,
  "student": 5,
  "lesson": 7,
  "enrollment_date": "2026-05-04T18:42:11Z",
  "status": "pending",
  "is_overbooked": false,
  "expires_at": "2026-05-05T18:42:11Z"
}
```

#### Regras de domínio (executadas pelo `model.clean()`)

- Inscrição em turma cheia é bloqueada com `400 Bad Request` (mensagem
  *"Turma lotada. Inscrição online não permitida."*) a menos que
  `is_overbooked=True`.
- `expires_at` é preenchido automaticamente para 24h após a criação
  (ver `default_enrollment_expiration`).
- `UniqueConstraint` no banco impede o mesmo aluno ter duas
  inscrições ativas (não-rejeitadas / não-expiradas) na mesma turma.

> ⚠️ Não há endpoint público de criação anônima de inscrição ainda
> (Fatia 1 parte 2 da roadmap). Hoje o `POST` aqui exige token.

### `Payment` — `/api/payments/`

CRUD de pagamentos. **Exige token**.

| Verbo | URL |
|---|---|
| `GET`    | `/api/payments/` |
| `POST`   | `/api/payments/` |
| `GET`    | `/api/payments/<id>/` |
| `PUT`    | `/api/payments/<id>/` |
| `PATCH`  | `/api/payments/<id>/` |
| `DELETE` | `/api/payments/<id>/` |

#### Schema

```json
{
  "id": 33,
  "enrollment": 12,
  "payment_date": "2026-05-04T18:45:09Z",
  "payment_method": "pix",
  "payment_origin": "online",
  "status": "pending",
  "money_amount": "120.00",
  "item_quantity_kg": null,
  "donation_type": "",
  "approved_by": null
}
```

#### Choices

- `payment_method`: `credit_card`, `pix`, `cash`, `donation_item`,
  `hybrid`, `scholarship`.
- `payment_origin`: `online`, `in_person`.
- `status`: `pending`, `confirmed`.
- `donation_type` (quando `payment_method` ∈ `{donation_item, hybrid}`):
  `dog_food`, `cat_food`, `bird_food`.

#### Regras de domínio (`model.clean()`)

- `payment_method == 'donation_item'` exige `item_quantity_kg`.
- Métodos `donation_item` e `hybrid` exigem `donation_type` informado.
- `payment_origin == 'in_person'` exige `approved_by` (id do
  funcionário que validou).

### `Student` — `/api/students/`

CRUD de alunos. **Exige token**.

| Verbo | URL |
|---|---|
| `GET`    | `/api/students/` |
| `POST`   | `/api/students/` |
| `GET`    | `/api/students/<id>/` |
| `PUT`    | `/api/students/<id>/` |
| `PATCH`  | `/api/students/<id>/` |
| `DELETE` | `/api/students/<id>/` |

#### Schema

```json
{
  "id": 5,
  "name": "Maria de Souza",
  "email": "maria@exemplo.com",
  "cpf": "123.456.789-00",
  "phone": "(45) 99999-1234",
  "emergency_contact": "(45) 99999-5678",
  "birth_date": "2010-03-21",
  "age": 16,
  "is_minor": true
}
```

- `age` e `is_minor` são **derivados** de `birth_date` (read-only).
- `cpf` e `email` têm `unique=True`.

### `Employee` — `/api/employees/`

CRUD de funcionários. **Exige token**.

| Verbo | URL |
|---|---|
| `GET`    | `/api/employees/` |
| `POST`   | `/api/employees/` |
| `GET`    | `/api/employees/<id>/` |
| `PUT`    | `/api/employees/<id>/` |
| `PATCH`  | `/api/employees/<id>/` |
| `DELETE` | `/api/employees/<id>/` |

#### Schema

```json
{
  "id": 2,
  "user": 4,
  "role": "Atendente",
  "hire_date": "2025-09-01"
}
```

### `Instructor` — `/api/instructors/`

CRUD de instrutores. **Exige token**.

| Verbo | URL |
|---|---|
| `GET`    | `/api/instructors/` |
| `POST`   | `/api/instructors/` |
| `GET`    | `/api/instructors/<id>/` |
| `PUT`    | `/api/instructors/<id>/` |
| `PATCH`  | `/api/instructors/<id>/` |
| `DELETE` | `/api/instructors/<id>/` |

#### Schema (interno)

```json
{
  "id": 3,
  "employee": 2,
  "bio": "Bióloga formada pela UFPR...",
  "specialty": "Ornitologia"
}
```

> O endpoint público `/api/courses/` aninha instrutores via
> `InstructorPublicSerializer` (apenas `id`, `name`, `specialty`),
> sem expor `bio` e `employee`.

## Pontos a observar (limitações conhecidas)

1. **Sem rota de login da API**: o token tem que ser gerado fora do
   fluxo HTTP (admin/shell/comando). Para a Fatia 1 parte 2 da
   roadmap, vale considerar adicionar
   `rest_framework.authtoken.views.obtain_auth_token` em
   `/api/token/`.
2. **`enrollments`, `payments`, `students`, `employees`, `instructors`
   estão hoje atrás de `IsAuthenticated`** sem distinção entre
   staff e usuário comum. Qualquer `User` cadastrado com token pode
   listar e mexer em tudo. Apertar isso (ex.: `IsAdminUser` para
   escrita) está na Should Have da roadmap.
3. **Sem paginação configurada**: clientes do projeto já lidam com
   array bruto e com paginado, mas a API ainda não usa
   `PageNumberPagination`. Vale ativar antes de produção.
4. **Sem documentação automática (Swagger/OpenAPI)**: a roadmap
   menciona `drf-spectacular` como melhoria futura. Quando entrar,
   este documento pode ser substituído por `/api/schema/swagger-ui/`.
5. **`enrollments/views.py` e `accounts/views.py` ainda estão como
   `ModelViewSet` cru**, sem regras de negócio expostas. As regras
   moram no `model.clean()` e são executadas via `full_clean()` no
   `save()`, então o DRF retorna 400 apropriadamente quando a regra é
   violada — mas o endpoint POST público de inscrição
   anônima ainda não existe.
