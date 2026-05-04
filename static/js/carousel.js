/**
 * Hero carousel — fetches banners from /api/banners/ and renders a sliding
 * carousel with arrows, dots and auto-rotation. Hidden if no banners.
 *
 * Behavior:
 * - Auto-rotates every AUTO_ROTATE_MS milliseconds
 * - Pauses while the user hovers, focuses inside, or the tab is hidden
 * - Arrow keys (when focused) navigate between slides
 * - Lazy loads images that are not the active slide
 */
(function () {
  const ENDPOINT = '/api/banners/';
  const AUTO_ROTATE_MS = 15000;

  function escapeHtml(value) {
    if (value == null) return '';
    return String(value)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

  function getResultsArray(payload) {
    if (Array.isArray(payload)) return payload;
    if (payload && Array.isArray(payload.results)) return payload.results;
    return [];
  }

  function renderSlide(banner, index) {
    const isFirst = index === 0;
    const ctaInner = banner.link_label && banner.link_url
      ? `<a class="carousel__cta btn btn--primary" href="${escapeHtml(banner.link_url)}">${escapeHtml(banner.link_label)}</a>`
      : '';

    const innerContent = `
      <img class="carousel__image"
           src="${escapeHtml(banner.image)}"
           alt="${escapeHtml(banner.title || '')}"
           ${isFirst ? '' : 'loading="lazy"'}>
      <div class="carousel__caption">
        ${banner.title ? `<h2 class="carousel__title">${escapeHtml(banner.title)}</h2>` : ''}
        ${banner.subtitle ? `<p class="carousel__subtitle">${escapeHtml(banner.subtitle)}</p>` : ''}
        ${ctaInner}
      </div>
    `;

    // If the banner is fully clickable (has link but no separate CTA label),
    // wrap the whole slide in an <a>. Otherwise just render the content.
    const wholeBlockClickable = banner.link_url && !banner.link_label;
    const body = wholeBlockClickable
      ? `<a class="carousel__link" href="${escapeHtml(banner.link_url)}">${innerContent}</a>`
      : innerContent;

    return `
      <li class="carousel__slide" role="group" aria-roledescription="slide" aria-hidden="${!isFirst}">
        ${body}
      </li>
    `;
  }

  function renderDot(index, total) {
    return `
      <button type="button" class="carousel__dot${index === 0 ? ' is-active' : ''}"
              role="tab" aria-selected="${index === 0}"
              aria-label="Ir para banner ${index + 1} de ${total}"
              data-index="${index}"></button>
    `;
  }

  function setupCarousel(root, banners) {
    const track = root.querySelector('#carousel-track');
    const dotsContainer = root.querySelector('#carousel-dots');
    const prevBtn = root.querySelector('#carousel-prev');
    const nextBtn = root.querySelector('#carousel-next');

    track.innerHTML = banners.map(renderSlide).join('');
    dotsContainer.innerHTML = banners.map((_, i) => renderDot(i, banners.length)).join('');

    let current = 0;
    let autoTimer = null;
    let isHovered = false;
    let isFocused = false;

    const slides = Array.from(track.querySelectorAll('.carousel__slide'));
    const dots = Array.from(dotsContainer.querySelectorAll('.carousel__dot'));

    // Navigation controls only matter when there's more than one slide.
    const singleSlide = banners.length <= 1;
    if (singleSlide) {
      prevBtn.hidden = true;
      nextBtn.hidden = true;
      dotsContainer.hidden = true;
    }

    function goTo(index) {
      const next = (index + banners.length) % banners.length;
      track.style.transform = `translateX(-${next * 100}%)`;
      slides.forEach((slide, i) => {
        slide.setAttribute('aria-hidden', String(i !== next));
      });
      dots.forEach((dot, i) => {
        dot.classList.toggle('is-active', i === next);
        dot.setAttribute('aria-selected', String(i === next));
      });
      current = next;
    }

    function startAutoRotation() {
      if (singleSlide) return;
      stopAutoRotation();
      autoTimer = window.setInterval(() => {
        if (isHovered || isFocused || document.hidden) return;
        goTo(current + 1);
      }, AUTO_ROTATE_MS);
    }

    function stopAutoRotation() {
      if (autoTimer) {
        window.clearInterval(autoTimer);
        autoTimer = null;
      }
    }

    prevBtn.addEventListener('click', () => goTo(current - 1));
    nextBtn.addEventListener('click', () => goTo(current + 1));

    dotsContainer.addEventListener('click', (event) => {
      const target = event.target.closest('.carousel__dot');
      if (!target) return;
      goTo(parseInt(target.dataset.index, 10));
    });

    root.addEventListener('mouseenter', () => { isHovered = true; });
    root.addEventListener('mouseleave', () => { isHovered = false; });
    root.addEventListener('focusin', () => { isFocused = true; });
    root.addEventListener('focusout', () => { isFocused = false; });

    root.addEventListener('keydown', (event) => {
      if (singleSlide) return;
      if (event.key === 'ArrowLeft') {
        event.preventDefault();
        goTo(current - 1);
      } else if (event.key === 'ArrowRight') {
        event.preventDefault();
        goTo(current + 1);
      }
    });

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        stopAutoRotation();
      } else {
        startAutoRotation();
      }
    });

    root.hidden = false;
    startAutoRotation();
  }

  async function init() {
    const root = document.getElementById('hero-carousel');
    if (!root) return;

    try {
      const response = await fetch(ENDPOINT, { headers: { Accept: 'application/json' } });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const payload = await response.json();
      const banners = getResultsArray(payload);

      if (banners.length === 0) {
        // No active banners — keep the section hidden.
        return;
      }

      setupCarousel(root, banners);
    } catch (error) {
      console.error('Failed to load banners:', error);
      // Stay hidden on error — no broken carousel skeleton on screen.
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
