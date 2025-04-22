/**
 * script.js - Updated for skill bar animations and other interactive features.
 */
document.addEventListener("DOMContentLoaded", () => {
  initScrollAnimations();
  initVideoSpeedControl();
  initRippleEffect();
  initScrollUpButton();
  initNavbarTransform();
  initIconHoverEffects();
  initSkillBarAnimations();

  // NEW: Initialize the 3D deck assembly cards if present
  init3DDeckAssembly();

  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(handleGlobalScroll);
      ticking = true;
    } else {
      ticking = false;
    }
  });
});

/**
 * 1. Scroll-triggered animations for sections, etc.
 */
function initScrollAnimations() {
  const elements = document.querySelectorAll(
    '.section:not(.animate), .fade-in-left:not(.animate), .fade-in-right:not(.animate), .zoom-in:not(.animate)'
  );
  const observerOptions = { threshold: 0.15, rootMargin: '0px 0px -50px 0px' };
  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.transitionDelay = `${Math.random() * 0.3}s`;
        entry.target.classList.add('animate');
        obs.unobserve(entry.target);
      }
    });
  }, observerOptions);
  elements.forEach(el => observer.observe(el));
}

/**
 * 2. Video background speed control (optional).
 */
function initVideoSpeedControl() {
  const video = document.querySelector('.video-background');
  if (!video) return;
  video.playbackRate = 1.0;
  video.muted = true;
  video.autoplay = true;
  video.loop = true;
  video.play().catch(e => console.warn("Autoplay prevented:", e));
}

function updateVideoSpeeds() {
  const video = document.querySelector('.video-background');
  if (!video) return;
  const rect = video.getBoundingClientRect();
  const percentVisible = Math.max(
    0,
    Math.min(1, (window.innerHeight - rect.top) / (window.innerHeight + rect.height))
  );
  // Example: Slight speed variation based on scroll
  video.playbackRate = 1.0 + (percentVisible - 0.5) * 0.5;
}

/**
 * 3. Ripple effect for buttons.
 */
function initRippleEffect() {
  document.addEventListener('pointerdown', (e) => {
    const button = e.target.closest('.btn-custom');
    if (!button) return;
    button.querySelectorAll('.ripple').forEach(r => r.remove());
    const ripple = document.createElement('span');
    ripple.className = 'ripple';
    const rect = button.getBoundingClientRect();
    const maxDim = Math.max(rect.width, rect.height) * 2;
    ripple.style.width = ripple.style.height = `${maxDim}px`;
    ripple.style.left = `${e.clientX - rect.left - maxDim / 2}px`;
    ripple.style.top = `${e.clientY - rect.top - maxDim / 2}px`;
    button.appendChild(ripple);
    ripple.addEventListener('animationend', () => ripple.remove());
  });
}

/**
 * 4. Scroll-up button logic.
 */
function initScrollUpButton() {
  let scrollBtn = document.querySelector('.scroll-up-btn');
  if (!scrollBtn) {
    scrollBtn = document.createElement('div');
    scrollBtn.className = 'scroll-up-btn';
    scrollBtn.setAttribute('aria-label', 'Scroll to top');
    scrollBtn.setAttribute('role', 'button');
    scrollBtn.innerHTML = '↑';
    scrollBtn.style.opacity = '0';
    scrollBtn.style.transform = 'scale(0.8)';
    document.body.appendChild(scrollBtn);
    scrollBtn.addEventListener('click', smoothScrollToTop);
  }
  if (!document.querySelector('.scroll-progress')) {
    const progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress';
    document.body.appendChild(progressBar);
  }
}

function updateScrollButtonAndProgress(scrollTop) {
  const doc = document.documentElement;
  const height = doc.scrollHeight - doc.clientHeight;
  const scrolledPercent = (scrollTop / height) * 100;
  const progressBar = document.querySelector('.scroll-progress');
  if (progressBar) progressBar.style.width = `${scrolledPercent}%`;

  const scrollBtn = document.querySelector('.scroll-up-btn');
  if (scrollBtn) {
    if (scrollTop > 300) {
      scrollBtn.style.opacity = '1';
      scrollBtn.style.transform = 'scale(1)';
    } else {
      scrollBtn.style.opacity = '0';
      scrollBtn.style.transform = 'scale(0.8)';
    }
  }
}

function smoothScrollToTop() {
  const currentScroll = document.documentElement.scrollTop || document.body.scrollTop;
  if (currentScroll > 0) {
    window.requestAnimationFrame(smoothScrollToTop);
    window.scrollTo(0, currentScroll - currentScroll / 8);
  }
}

/**
 * 5. Navbar transform on scroll.
 */
function initNavbarTransform() {
  const navbar = document.querySelector('.navbar');
  if (!navbar) return;
  window.addEventListener('scroll', () => {
    const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    navbar.classList.toggle('scrolled', scrollTop > 100);
  });
}

/**
 * 6. Icon hover effects.
 */
function initIconHoverEffects() {
  const icons = document.querySelectorAll('.icon, .fa, .fas, .far, .fab');
  if (!icons.length) return;
  icons.forEach(icon => {
    icon.style.transform = 'scale(1)';
    icon.style.transition = 'transform 0.3s ease';
    icon.addEventListener('mouseenter', () => {
      icon.style.transform = 'scale(1.2)';
    });
    icon.addEventListener('mouseleave', () => {
      icon.style.transform = 'scale(1)';
    });
  });
}

/**
 * 7. Skill Bar Animations using IntersectionObserver.
 */
function initSkillBarAnimations() {
  const bars = document.querySelectorAll('.progress-bar');
  if (!bars.length) return;

  const observerOptions = { threshold: 0.2 };
  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const bar = entry.target;
        const level = bar.getAttribute('data-skill-level');
        // Set the custom property for the CSS transform
        bar.style.setProperty('--skill-scale', level / 100);
        // Add a class that triggers the CSS animation
        bar.classList.add('animate');
        // Unobserve so each bar animates only once
        obs.unobserve(bar);
      }
    });
  }, observerOptions);

  bars.forEach(bar => observer.observe(bar));
}

/**
 * 8. 3D Deck Assembly Initialization
 *    Dynamically assign transforms or angles to .deck-card if you want random or custom layout.
 */

/**
 * Global scroll handler for combined functionalities.
 */
function handleGlobalScroll() {
  const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
  updateScrollButtonAndProgress(scrollTop);
  updateVideoSpeeds(); // optional if using video speed variation
}


function init3DDeckAssembly() {
  const deckContainer = document.querySelector('.deck-container');
  if (!deckContainer) return; // Skip if no deck exists

  const cards = deckContainer.querySelectorAll('.deck-card');
  const totalCards = cards.length;
  const spread = 10;      // degrees of rotation from center (reduced for minimal overlap)
  const offsetX = 150;    // horizontal spacing to avoid overlapping
  const offsetZ = 20;     // z-axis offset per step
  const middleIndex = Math.floor(totalCards / 2);

  cards.forEach((card, i) => {
    const indexFromMiddle = i - middleIndex;
    const angle = indexFromMiddle * spread;
    const xTrans = indexFromMiddle * offsetX;
    const zTrans = Math.abs(indexFromMiddle) * offsetZ * -1;
    // Save the original transform for restoration on mouseleave
    const originalTransform = `rotateY(${angle}deg) translateX(${xTrans}px) translateZ(${zTrans}px)`;
    card.dataset.originalTransform = originalTransform;
    card.style.transform = originalTransform;
    card.style.zIndex = `${10 - Math.abs(indexFromMiddle)}`;

    // On hover, enlarge and bring the card forward
    card.addEventListener('mouseenter', () => {
      card.style.transform = `translateZ(80px) scale(1.25) rotateY(0deg)`;
      card.style.zIndex = '999';
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = card.dataset.originalTransform;
      card.style.zIndex = `${10 - Math.abs(indexFromMiddle)}`;
    });
  });
}
