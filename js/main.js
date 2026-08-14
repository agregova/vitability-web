if (window.location.protocol.startsWith('http')) {
  const { pathname, search, hash } = window.location;
  const lastPathSegment = pathname.split('/').pop() || '';
  const hasFileExtension = lastPathSegment.includes('.');

  if (!pathname.endsWith('/') && !hasFileExtension) {
    window.location.replace(`${pathname}/${search}${hash}`);
  }
}

const menuToggle = document.querySelector('.menu-toggle');
const mainNav = document.querySelector('.main-nav');

menuToggle?.addEventListener('click', () => {
  const isOpen = mainNav.classList.toggle('is-open');
  menuToggle.setAttribute('aria-expanded', String(isOpen));
});

mainNav?.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    mainNav.classList.remove('is-open');
    menuToggle?.setAttribute('aria-expanded', 'false');
  });
});

const lessonsContainer = document.querySelector('#lessons');

async function loadCurrentLessons() {
  try {
    const response = await fetch('data/aktualne.json', { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const data = await response.json();
    const lessons = Array.isArray(data.lessons) ? data.lessons : [];

    if (!lessons.length) {
      lessonsContainer.innerHTML = '<p class="empty">Tento týždeň nie sú naplánované žiadne verejné hodiny.</p>';
      return;
    }

    lessonsContainer.innerHTML = lessons.map((lesson) => `
      <article class="lesson">
        <div class="lesson-time">${escapeHtml(lesson.time)}</div>
        <div>
          <p class="eyebrow">${escapeHtml(lesson.day)}</p>
          <h3>${escapeHtml(lesson.name)}</h3>
          <p class="lesson-meta">${escapeHtml(lesson.place)}</p>
          ${lesson.note ? `<p class="lesson-note">${escapeHtml(lesson.note)}</p>` : ''}
        </div>
      </article>
    `).join('');
  } catch (error) {
    console.error('Nepodarilo sa načítať aktuálne hodiny:', error);
    lessonsContainer.innerHTML = '<p class="empty">Aktuálne hodiny sa momentálne nepodarilo načítať.</p>';
  }
}

function escapeHtml(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

document.querySelector('#year').textContent = new Date().getFullYear();
loadCurrentLessons();

document.querySelectorAll("[data-carousel]").forEach((carousel) => {
  const track = carousel.querySelector(".carousel-track");
  const slides = [...carousel.querySelectorAll(".carousel-slide")];
  const dotsContainer = carousel.querySelector(".carousel-dots");

  if (!track || !dotsContainer || slides.length === 0) {
    return;
  }

  const dots = slides.map((slide, index) => {
    const dot = document.createElement("button");

    dot.className = "carousel-dot";
    dot.type = "button";
    dot.setAttribute("aria-label", `Zobraziť položku ${index + 1}`);

    if (index === 0) {
      dot.classList.add("is-active");
    }

    dot.addEventListener("click", () => {
      slide.scrollIntoView({
        behavior: "smooth",
        block: "nearest",
        inline: "start"
      });
    });

    dotsContainer.appendChild(dot);

    return dot;
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }

        const index = slides.indexOf(entry.target);

        dots.forEach((dot, dotIndex) => {
          dot.classList.toggle("is-active", dotIndex === index);
        });
      });
    },
    {
      root: track,
      threshold: 0.6
    }
  );

  slides.forEach((slide) => observer.observe(slide));
});
