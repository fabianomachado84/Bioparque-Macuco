/**
 * Public courses listing — fetches active courses from the API and renders
 * them as cards inside #courses-grid. Cards link to the detail page.
 */
(function () {
  const COURSES_ENDPOINT = '/api/courses/';
  const PLACEHOLDER_IMAGE = '/static/images/curso-placeholder.svg';

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

  function escapeHtml(value) {
    if (value == null) return '';
    return String(value)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

  function renderCertificateBadge(hasCertificate) {
    if (!hasCertificate) return '';
    return `
      <div class="card-curso__cert">
        <svg viewBox="0 0 24 24" width="25" height="25" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 15l-2 5l1-3h2l1 3l-2-5z"/>
          <circle cx="12" cy="9" r="6"/>
        </svg>
        <p>Certificado disponibilizado</p>
      </div>
    `;
  }

  function renderCard(course) {
    const detailUrl = `/cursos/${course.id}/`;
    const imageUrl = course.image || PLACEHOLDER_IMAGE;

    return `
      <article class="card-curso">
        <a href="${detailUrl}" class="card-curso__image">
          <img src="${escapeHtml(imageUrl)}" alt="${escapeHtml(course.name)}">
        </a>
        <div class="card-curso__body">
          <h3 class="card-curso__title">${escapeHtml(course.name)}</h3>
          <p class="card-curso__desc">${escapeHtml(course.description)}</p>
          <div class="card-curso__meta">
            <span class="card-curso__duration">${escapeHtml(course.duration_hours)} horas</span>
            <span class="card-curso__price">${escapeHtml(formatPrice(course))}</span>
          </div>
          <div class="card-curso__footer">
            ${renderCertificateBadge(course.has_certificate)}
            <div>
              <a href="${detailUrl}" class="btn-saiba-mais">SAIBA MAIS</a>
            </div>
          </div>
        </div>
      </article>
    `;
  }

  function renderError(grid, message) {
    grid.innerHTML = `<p class="cursos__error">${escapeHtml(message)}</p>`;
  }

  function getResultsArray(payload) {
    // Supports both paginated (`{results: [...]}`) and bare-array responses.
    if (Array.isArray(payload)) return payload;
    if (payload && Array.isArray(payload.results)) return payload.results;
    return [];
  }

  async function loadCourses(grid, options) {
    const params = new URLSearchParams();
    if (options.limit) params.set('page_size', options.limit);

    const url = params.toString()
      ? `${COURSES_ENDPOINT}?${params.toString()}`
      : COURSES_ENDPOINT;

    try {
      const response = await fetch(url, { headers: { Accept: 'application/json' } });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const payload = await response.json();
      let courses = getResultsArray(payload);

      if (options.limit) {
        courses = courses.slice(0, options.limit);
      }

      if (courses.length === 0) {
        const emptyMessage = grid.dataset.emptyMessage || 'Nenhum curso disponível.';
        grid.innerHTML = `<p class="cursos__empty">${escapeHtml(emptyMessage)}</p>`;
        return;
      }

      grid.innerHTML = courses.map(renderCard).join('');
    } catch (error) {
      console.error('Failed to load courses:', error);
      renderError(grid, 'Não foi possível carregar os cursos. Tente novamente em instantes.');
    }
  }

  function init() {
    const grids = document.querySelectorAll('[data-courses-grid], #courses-grid, #featured-courses-grid');
    grids.forEach((grid) => {
      const limit = grid.dataset.limit ? parseInt(grid.dataset.limit, 10) : null;
      loadCourses(grid, { limit });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
