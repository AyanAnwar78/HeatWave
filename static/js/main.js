/* HeatGuard – main.js */

// ── Mobile nav toggle ─────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const btn  = document.getElementById('menuBtn');
  const menu = document.getElementById('mobileMenu');
  if (btn && menu) {
    btn.addEventListener('click', () => menu.classList.toggle('hidden'));
  }

  // Auto-dismiss alerts after 4 s
  document.querySelectorAll('[data-dismiss]').forEach(el => {
    setTimeout(() => el.remove(), 4000);
  });

  // Current local time display (re-formats ISO time string)
  const timeEl = document.getElementById('localTime');
  if (timeEl) {
    const raw = timeEl.textContent.trim();
    if (raw) {
      try {
        const d   = new Date(raw);
        const fmt = d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        timeEl.textContent = `Last updated ${fmt}`;
      } catch (_) {}
    }
  }
});

