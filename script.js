/* =============================================
   SHAMIM TEXTILE MILLS PVT LTD
   ============================================= */

(function () {
  'use strict';

  var WHATSAPP_NUMBER = '923315444435';

  /* ---- Navbar scroll effect ---- */
  var navbar = document.getElementById('navbar');
  function onScroll() {
    if (window.scrollY > 40) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
    toggleBackToTop();
    updateActiveNavLink();
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---- Mobile hamburger menu ---- */
  var hamburger = document.getElementById('hamburger');
  var navLinks = document.getElementById('navLinks');

  hamburger.addEventListener('click', function () {
    var isOpen = navLinks.classList.toggle('open');
    hamburger.classList.toggle('active', isOpen);
    hamburger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    document.body.style.overflow = isOpen ? 'hidden' : '';
  });

  navLinks.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () {
      navLinks.classList.remove('open');
      hamburger.classList.remove('active');
      hamburger.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    });
  });

  document.addEventListener('click', function (e) {
    if (navLinks.classList.contains('open') && !navbar.contains(e.target)) {
      navLinks.classList.remove('open');
      hamburger.classList.remove('active');
      hamburger.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }
  });

  /* ---- Back to top ---- */
  var backToTop = document.getElementById('backToTop');
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

  /* ---- Scroll-reveal ---- */
  function initAOS() {
    var elements = document.querySelectorAll('[data-aos]');
    if (!('IntersectionObserver' in window)) {
      elements.forEach(function (el) { el.classList.add('aos-animate'); });
      return;
    }
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var delay = parseInt(entry.target.dataset.delay || 0, 10);
          setTimeout(function () {
            entry.target.classList.add('aos-animate');
          }, delay);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    elements.forEach(function (el) { observer.observe(el); });
  }

  function staggerCards() {
    document.querySelectorAll('.service-card, .why-card').forEach(function (card, index) {
      if (!card.dataset.delay) {
        card.dataset.delay = String((index % 3) * 100);
      }
    });
  }

  /* ---- Contact form → WhatsApp ---- */
  var contactForm = document.getElementById('contactForm');

  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();

      var name = document.getElementById('name').value.trim();
      var company = document.getElementById('company').value.trim();
      var email = document.getElementById('email').value.trim();
      var phone = document.getElementById('phone').value.trim();
      var service = document.getElementById('service').value.trim();
      var message = document.getElementById('message').value.trim();

      if (!name || !message) {
        showFormError('Please enter your name and message.');
        return;
      }

      if (email && !isValidEmail(email)) {
        showFormError('Please enter a valid email address.');
        return;
      }

      var lines = [
        'Hello Shamim Textile Mills,',
        '',
        'I would like to inquire about your dyeing & finishing services.',
        '',
        'Name: ' + name
      ];
      if (company) lines.push('Company: ' + company);
      if (email) lines.push('Email: ' + email);
      if (phone) lines.push('Phone: ' + phone);
      if (service) lines.push('Service: ' + service);
      lines.push('', 'Requirements:', message);

      var url = 'https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encodeURIComponent(lines.join('\n'));
      window.open(url, '_blank', 'noopener,noreferrer');
    });
  }

  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  function showFormError(msg) {
    var existing = contactForm.querySelector('.form-error-msg');
    if (existing) existing.remove();

    var err = document.createElement('p');
    err.className = 'form-error-msg';
    err.style.cssText = 'color:#c0392b;font-size:0.85rem;margin-bottom:12px;font-weight:600;';
    err.textContent = msg;
    contactForm.querySelector('button[type="submit"]').before(err);
    setTimeout(function () { err.remove(); }, 4000);
  }

  /* ---- Active nav on scroll ---- */
  function updateActiveNavLink() {
    var sections = document.querySelectorAll('section[id]');
    var scrollPos = window.scrollY + 140;
    var current = '';

    sections.forEach(function (section) {
      var top = section.offsetTop;
      var bottom = top + section.offsetHeight;
      if (scrollPos >= top && scrollPos < bottom) {
        current = section.getAttribute('id');
      }
    });

    document.querySelectorAll('.nav-links a').forEach(function (a) {
      a.classList.remove('active');
      if (current && a.getAttribute('href') === '#' + current) {
        a.classList.add('active');
      }
    });
  }

  /* ---- Gallery video: inline only, no fullscreen / native player ---- */
  function lockGalleryVideo() {
    var video = document.getElementById('printingVideo');
    if (!video) return;

    video.setAttribute('playsinline', '');
    video.setAttribute('webkit-playsinline', '');
    video.controls = false;
    video.disablePictureInPicture = true;
    if (video.disableRemotePlayback !== undefined) {
      video.disableRemotePlayback = true;
    }

    function blockFullscreen(e) {
      e.preventDefault();
      if (document.fullscreenElement) {
        document.exitFullscreen().catch(function () {});
      }
      if (document.webkitFullscreenElement && document.webkitExitFullscreen) {
        document.webkitExitFullscreen();
      }
    }

    ['fullscreenchange', 'webkitfullscreenchange'].forEach(function (evt) {
      document.addEventListener(evt, function () {
        if (document.fullscreenElement === video || document.webkitFullscreenElement === video) {
          blockFullscreen({ preventDefault: function () {} });
        }
      });
    });

    video.addEventListener('loadeddata', function () {
      var playPromise = video.play();
      if (playPromise && playPromise.catch) {
        playPromise.catch(function () {});
      }
    });
  }

  /* ---- Init ---- */
  function init() {
    staggerCards();
    initAOS();
    lockGalleryVideo();
    onScroll();
    // Safety: never leave sections invisible if observer misses them
    setTimeout(function () {
      document.querySelectorAll('[data-aos]:not(.aos-animate)').forEach(function (el) {
        el.classList.add('aos-animate');
      });
    }, 2500);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
