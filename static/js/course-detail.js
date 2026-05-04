/**
 * Course detail page — fetches a single course (with its instructors and
 * next upcoming lesson) and renders it. Uses the global `marked` library
 * (loaded via CDN in the template) to render the syllabus Markdown.
 */
(function () {
  const PLACEHOLDER_IMAGE = '/static/images/curso-placeholder.svg';

  function escapeHtml(value) {
    if (value == null) return '';
    return String(value)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

  function renderSyllabus(syllabus) {
    if (!syllabus || !syllabus.trim()) {
      return '<p class="course-detail__empty">Roteiro não disponível.</p>';
    }
    if (typeof window.marked === 'undefined') {
      // Fallback: show as preformatted text if the markdown lib didn't load.
      return `<pre class="course-detail__syllabus-fallback">${escapeHtml(syllabus)}</pre>`;
    }
    return window.marked.parse(syllabus);
  }

  function renderInstructors(instructors) {
    if (!instructors || instructors.length === 0) return '';
    const heading = instructors.length === 1 ? 'Instrutor' : 'Instrutores';
    const items = instructors
      .map((i) => `<span class="course-detail__instructor">${escapeHtml(i.name || 'Instrutor')}</span>`)
      .join('');
    return `
      <h3 class="course-detail__instructors-title">${heading}</h3>
      <div class="course-detail__instructors-list">${items}</div>
    `;
  }

  function formatPrice(course) {
    const parts = [];
    if (course.price && Number(course.price) > 0) {
      parts.push(`R$ ${Number(course.price).toFixed(2).replace('.', ',')}`);
    }
    if (course.donation_kg_required && Number(course.donation_kg_required) > 0) {
      const kg = Number(course.donation_kg_required);
      parts.push(`${kg % 1 === 0 ? kg.toFixed(0) : kg.toFixed(1).replace('.', ',')} kg de ração`);
    }
    return parts.length ? parts.join(' + ') : 'Gratuito';
  }

  function formatDateBr(isoDate) {
    if (!isoDate) return '';
    const [year, month, day] = isoDate.split('-');
    return `${day}/${month}`;
  }

  function formatTimeBr(time) {
    if (!time) return '';
    return time.slice(0, 5).replace(':', 'h');
  }

  function renderInfo(course) {
    const next = course.next_lesson;
    const certificateLine = course.has_certificate
      ? `
        <p class="course-detail__certificate">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 15l-2 5l1-3h2l1 3l-2-5z"/>
            <circle cx="12" cy="9" r="6"/>
          </svg>
          Certificado disponibilizado
        </p>
      `
      : '';

    if (!next) {
      return `
        <p class="course-detail__no-lesson">Nenhuma turma agendada no momento.</p>
        ${certificateLine}
      `;
    }

    const date = formatDateBr(next.start_date);
    const start = formatTimeBr(next.start_time);
    const end = formatTimeBr(next.end_time);

    return `
      <p class="course-detail__date">Dia ${escapeHtml(date)}</p>
      <p class="course-detail__time">
        <span>Das ${escapeHtml(start)} às ${escapeHtml(end)}</span>
        <span>${escapeHtml(formatPrice(course))}</span>
      </p>
      ${certificateLine}
      <a href="/inscricao/?course=${course.id}&lesson=${next.id}" class="btn btn--olive course-detail__cta">
        GARANTA SUA VAGA
      </a>
    `;
  }

  function renderCourse(course) {
    document.title = `${course.name} - Bioparque Macuco`;

    const nameEl = document.getElementById('course-name');
    const bodyEl = document.getElementById('course-body');
    const imageEl = document.getElementById('course-image');
    const infoEl = document.getElementById('course-info');
    const instructorsEl = document.getElementById('course-instructors');

    if (nameEl) nameEl.textContent = course.name;
    if (bodyEl) bodyEl.innerHTML = renderSyllabus(course.syllabus);
    if (imageEl) {
      imageEl.src = course.image || PLACEHOLDER_IMAGE;
      imageEl.alt = course.name || 'Imagem do curso';
    }
    if (infoEl) infoEl.innerHTML = renderInfo(course);
    if (instructorsEl) instructorsEl.innerHTML = renderInstructors(course.instructors);
  }

  function renderError(message) {
    const bodyEl = document.getElementById('course-body');
    const infoEl = document.getElementById('course-info');
    if (bodyEl) bodyEl.innerHTML = `<p class="course-detail__error">${message}</p>`;
    if (infoEl) infoEl.innerHTML = '';
  }

  async function loadCourse(courseId) {
    try {
      const response = await fetch(`/api/courses/${courseId}/`, {
        headers: { Accept: 'application/json' },
      });
      if (response.status === 404) {
        renderError('Curso não encontrado.');
        return;
      }
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const course = await response.json();
      renderCourse(course);
    } catch (error) {
      console.error('Failed to load course:', error);
      renderError('Não foi possível carregar o curso. Tente novamente em instantes.');
    }
  }

  function init() {
    const root = document.querySelector('[data-course-id]');
    if (!root) return;
    const courseId = root.dataset.courseId;
    if (!courseId) {
      renderError('Curso inválido.');
      return;
    }
    loadCourse(courseId);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
