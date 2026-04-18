/* =============================================
   SHAMIM TEXTILE MILLS PVT LTD
   JavaScript - Interactions & Animations
   ============================================= */

(function () {
  'use strict';

  /* ---- Navbar scroll effect ---- */
  const navbar = document.getElementById('navbar');
  function onScroll() {
    if (window.scrollY > 60) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
    toggleBackToTop();
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---- Mobile hamburger menu ---- */
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('navLinks');

  hamburger.addEventListener('click', function () {
    const isOpen = navLinks.classList.toggle('open');
    hamburger.classList.toggle('active', isOpen);
    document.body.style.overflow = isOpen ? 'hidden' : '';
  });

  // Close menu on nav link click
  navLinks.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () {
      navLinks.classList.remove('open');
      hamburger.classList.remove('active');
      document.body.style.overflow = '';
    });
  });

  // Close menu on outside click
  document.addEventListener('click', function (e) {
    if (navLinks.classList.contains('open') && !navbar.contains(e.target)) {
      navLinks.classList.remove('open');
      hamburger.classList.remove('active');
      document.body.style.overflow = '';
    }
  });

  /* ---- Back to top button ---- */
  const backToTop = document.getElementById('backToTop');
  function toggleBackToTop() {
    if (window.scrollY > 400) {
      backToTop.classList.add('show');
    } else {
      backToTop.classList.remove('show');
    }
  }
  backToTop.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  /* ---- Hero floating particles ---- */
  function createParticles() {
    const container = document.getElementById('particles');
    if (!container) return;
    const count = 18;
    for (let i = 0; i < count; i++) {
      const p = document.createElement('div');
      p.classList.add('particle');
      const size = Math.random() * 60 + 10;
      const left = Math.random() * 100;
      const duration = Math.random() * 20 + 15;
      const delay = Math.random() * 20;
      p.style.cssText = `
        width: ${size}px;
        height: ${size}px;
        left: ${left}%;
        animation-duration: ${duration}s;
        animation-delay: -${delay}s;
      `;
      container.appendChild(p);
    }
  }
  createParticles();

  /* ---- Scroll-reveal (AOS-lite) ---- */
  function initAOS() {
    const elements = document.querySelectorAll('[data-aos]');
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          const delay = parseInt(entry.target.dataset.delay || 0, 10);
          setTimeout(function () {
            entry.target.classList.add('aos-animate');
          }, delay);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    elements.forEach(function (el) {
      observer.observe(el);
    });
  }

  /* ---- Service cards staggered delay ---- */
  function staggerCards() {
    const cards = document.querySelectorAll('.service-card, .why-card');
    cards.forEach(function (card, index) {
      if (!card.dataset.delay) {
        card.dataset.delay = (index % 3) * 120;
      }
    });
  }
  staggerCards();

  /* ---- Contact Form handling ---- */
  const contactForm = document.getElementById('contactForm');
  const formSuccess = document.getElementById('formSuccess');

  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();

      // Basic validation
      const name = document.getElementById('name').value.trim();
      const email = document.getElementById('email').value.trim();
      const message = document.getElementById('message').value.trim();

      if (!name || !email || !message) {
        showFormError('Please fill in all required fields.');
        return;
      }

      if (!isValidEmail(email)) {
        showFormError('Please enter a valid email address.');
        return;
      }

      // Simulate form submission
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending...';

      setTimeout(function () {
        contactForm.style.display = 'none';
        formSuccess.classList.add('show');
      }, 1200);
    });
  }

  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  function showFormError(msg) {
    // Remove existing error
    const existing = contactForm.querySelector('.form-error-msg');
    if (existing) existing.remove();

    const err = document.createElement('p');
    err.className = 'form-error-msg';
    err.style.cssText = 'color:#ef4444; font-size:0.85rem; margin-bottom:12px; font-weight:500;';
    err.textContent = msg;
    contactForm.querySelector('button[type="submit"]').before(err);

    setTimeout(function () { err.remove(); }, 4000);
  }

  /* ---- Smooth active nav link on scroll ---- */
  function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const scrollPos = window.scrollY + 100;

    sections.forEach(function (section) {
      const top = section.offsetTop;
      const bottom = top + section.offsetHeight;
      const id = section.getAttribute('id');
      const link = document.querySelector(`.nav-links a[href="#${id}"]`);
      if (link) {
        if (scrollPos >= top && scrollPos < bottom) {
          document.querySelectorAll('.nav-links a').forEach(function (a) {
            a.style.color = '';
          });
          link.style.color = 'var(--accent)';
        }
      }
    });
  }
  window.addEventListener('scroll', updateActiveNavLink, { passive: true });

  /* ---- Counter animation for hero stats ---- */
  function animateCounter(el, target, duration) {
    const isText = isNaN(parseInt(target));
    if (isText) return; // skip non-numeric like "Export"

    let start = 0;
    const end = parseInt(target);
    if (end === 0) return;

    const increment = end / (duration / 16);
    const suffix = target.includes('+') ? '+' : (target.includes('%') ? '%' : '');

    function step() {
      start += increment;
      if (start >= end) {
        el.textContent = end + suffix;
        return;
      }
      el.textContent = Math.floor(start) + suffix;
      requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function initCounters() {
    const counters = document.querySelectorAll('.stat-num');
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          const el = entry.target;
          const val = el.textContent.trim();
          animateCounter(el, val, 1500);
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.5 });

    counters.forEach(function (c) { observer.observe(c); });
  }

  /* ---- Init all on DOM ready ---- */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    initAOS();
    initCounters();
    onScroll(); // run once to set initial state
  }

})();
