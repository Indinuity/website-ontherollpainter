/* On The Roll Painters — shared behaviour for every page. No dependencies. */
document.querySelectorAll('#yr').forEach(el => { el.textContent = new Date().getFullYear(); });

/* ---------- mobile menu ---------- */
const menuBtn = document.querySelector('.menu-btn');
const nav = document.getElementById('nav');
const setMenu = open => {
  nav.classList.toggle('open', open);
  menuBtn.setAttribute('aria-expanded', String(open));
};
menuBtn.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
nav.addEventListener('click', e => { if (e.target.tagName === 'A') setMenu(false); });
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); menuBtn.focus(); }
});
document.addEventListener('click', e => {
  if (nav.classList.contains('open') && !e.target.closest('.bar')) setMenu(false);
});

/* ---------- lightbox: only wired up once a real image has loaded ---------- */
const lb = document.getElementById('lb');
const lbImg = document.createElement('img');
lbImg.alt = '';
lb.append(lbImg);
document.querySelectorAll('#work .shot:not(.compare), #beforeafter .shot:not(.compare), .project .shot:not(.compare)').forEach(fig => {
  const img = fig.querySelector('img.after') || fig.querySelector('img');  // a twin opens its after
  const open = () => {
    lbImg.src = img.currentSrc || img.src;
    lbImg.alt = img.alt;
    lb.showModal();
  };
  const enable = () => {
    if (img.naturalWidth === 0) return;
    fig.classList.add('zoomable');
    fig.tabIndex = 0;
    fig.setAttribute('role', 'button');
    fig.setAttribute('aria-label', 'Enlarge: ' + img.alt);
    fig.addEventListener('click', open);
    fig.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
    });
  };
  if (img.complete) enable(); else img.addEventListener('load', enable, { once: true });
});
lb.querySelector('.close').addEventListener('click', () => lb.close());
lb.addEventListener('click', e => { if (e.target === lb) lb.close(); });
lb.addEventListener('close', () => { lbImg.removeAttribute('src'); });

/* ---------- before/after sliders ---------- */
const hoverFollows = matchMedia('(hover:hover) and (pointer:fine)').matches;
document.querySelectorAll('.compare').forEach(fig => {
  const range = fig.querySelector('input[type=range]');
  const set = v => {
    v = Math.round(Math.max(0, Math.min(100, v)));
    range.value = v;
    fig.style.setProperty('--pos', v + '%');
    range.setAttribute('aria-valuetext', v + '% before, ' + (100 - v) + '% after');
  };
  range.addEventListener('input', () => set(+range.value));
  if (hoverFollows) fig.addEventListener('pointermove', e => {
    if (e.pointerType !== 'mouse') return;
    const r = fig.getBoundingClientRect();
    set((e.clientX - r.left) / r.width * 100);
  });
  set(+range.value);
});

/* ---------- quote form ---------- */
const form = document.getElementById('quoteForm');
const note = document.getElementById('formnote');
const emailText = (document.querySelector('footer a[href^="mailto:"]') || {}).textContent || '';
const say = msg => { note.textContent = msg; note.classList.add('show'); };

if (form) form.addEventListener('submit', async e => {
  e.preventDefault();
  if (form.getAttribute('action').includes('YOUR_FORM_ID')) {
    say('The form isn’t connected yet. Add your Formspree ID to the form action.');
    return;
  }
  const btn = form.querySelector('button[type=submit]');
  btn.disabled = true; btn.textContent = 'Sending';
  try {
    const res = await fetch(form.getAttribute('action'), {
      method: 'POST',
      body: new FormData(form),
      headers: { Accept: 'application/json' }
    });
    if (!res.ok) throw new Error('Form service returned ' + res.status);
    form.classList.add('sent');
    say('Got it. Expect a reply within a day.');
  } catch (err) {
    btn.disabled = false; btn.textContent = 'Send request';
    say('That didn’t send. Email ' + emailText.trim() + ' instead.');
  }
});
