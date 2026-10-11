/* Vĩnh Lộc Plastic — tương tác giao diện.
   Nội dung đã có sẵn trong HTML (tốt cho SEO); file này chỉ thêm hành vi. */
document.documentElement.classList.add('js');

const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];

/* Mở website trực tiếp từ máy (file://): trình duyệt không tự mở index.html trong thư mục,
   nên thêm "index.html" vào các link dạng thư mục. Trên hosting giữ nguyên URL đẹp. */
if (location.protocol === 'file:') {
  const fix = h => {
    if (!h || /^([a-z]+:|#|\/\/)/i.test(h)) return h;
    const i = h.indexOf('#');
    const p = i < 0 ? h : h.slice(0, i), hash = i < 0 ? '' : h.slice(i);
    if (p === '' || /\.[a-z0-9]+$/i.test(p)) return h;
    return (p.endsWith('/') ? p : p + '/') + 'index.html' + hash;
  };
  $$('a[href]').forEach(a => a.setAttribute('href', fix(a.getAttribute('href'))));
  $$('[data-target]').forEach(el => (el.dataset.target = fix(el.dataset.target)));
  $$('[data-href]').forEach(el => (el.dataset.href = fix(el.dataset.href)));
}
const store = {
  get(k) { try { return sessionStorage.getItem(k); } catch (_) { return null; } },
  set(k, v) { try { v == null ? sessionStorage.removeItem(k) : sessionStorage.setItem(k, v); } catch (_) {} },
};

function toast(msg) {
  const t = $('#toast');
  if (!t) return;
  t.textContent = msg;
  t.classList.add('is-show');
  clearTimeout(toast._t);
  toast._t = setTimeout(() => t.classList.remove('is-show'), 2800);
}

/* ===== Slider (trang chủ) ===== */
(function slider() {
  const root = $('#slider');
  if (!root) return;
  const track = $('.slider__track', root);
  const slides = $$('.slide', root);
  const dotsWrap = $('.slider__dots', root);
  let i = 0, timer;
  slides.forEach((_, k) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.setAttribute('aria-label', `Slide ${k + 1}`);
    b.onclick = () => go(k, true);
    dotsWrap.appendChild(b);
  });
  const dots = $$('button', dotsWrap);
  function go(n, user) {
    i = (n + slides.length) % slides.length;
    track.style.transform = `translateX(-${i * 100}%)`;
    slides.forEach((s, k) => s.classList.toggle('is-active', k === i));
    dots.forEach((d, k) => d.classList.toggle('is-active', k === i));
    if (user) restart();
  }
  function restart() { clearInterval(timer); timer = setInterval(() => go(i + 1), 5000); }
  $('.slider__btn--prev', root).onclick = () => go(i - 1, true);
  $('.slider__btn--next', root).onclick = () => go(i + 1, true);
  root.addEventListener('mouseenter', () => clearInterval(timer));
  root.addEventListener('mouseleave', restart);
  let x0 = null;
  root.addEventListener('touchstart', e => (x0 = e.touches[0].clientX), { passive: true });
  root.addEventListener('touchend', e => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 40) go(i + (dx < 0 ? 1 : -1), true);
    x0 = null;
  });
  go(0); restart();
})();

/* ===== Lọc sản phẩm theo tab + tìm kiếm ===== */
const grid = $('#productGrid');
let currentCat = 'all', query = '';

function applyFilter() {
  if (!grid) return;
  const q = query.trim().toLowerCase();
  const limit = +grid.dataset.limit || 0;
  let shown = 0;
  $$('.card', grid).forEach(card => {
    const match = (currentCat === 'all' || card.dataset.cat === currentCat) && (!q || card.dataset.name.includes(q));
    const visible = match && !(limit && currentCat === 'all' && !q && shown >= limit);
    card.hidden = !visible;
    if (visible) shown++;
  });
  const empty = $('#emptyMsg');
  if (empty) {
    empty.hidden = shown > 0;
    empty.textContent = `Không tìm thấy sản phẩm phù hợp với “${query}”.`;
  }
}

$$('#tabs .tab').forEach(tab => tab.addEventListener('click', () => {
  currentCat = tab.dataset.filter;
  $$('#tabs .tab').forEach(t => {
    const on = t === tab;
    t.classList.toggle('is-active', on);
    t.setAttribute('aria-selected', on);
  });
  const link = $('#catLink');
  if (link) { link.href = tab.dataset.href; link.textContent = tab.dataset.label; }
  applyFilter();
}));

const searchForm = $('#searchForm'), searchInput = $('#searchInput');
if (searchInput) {
  if (grid) {
    // Trang có lưới sản phẩm: lọc ngay khi gõ
    const saved = store.get('vl-search');
    if (saved) { searchInput.value = query = saved; store.set('vl-search', null); applyFilter(); }
    searchInput.addEventListener('input', e => {
      query = e.target.value;
      if (query) grid.scrollIntoView({ behavior: 'smooth', block: 'start' });
      applyFilter();
    });
    searchForm.addEventListener('submit', e => e.preventDefault());
  } else {
    // Trang khác: Enter để chuyển sang trang sản phẩm và lọc ở đó
    searchForm.addEventListener('submit', e => {
      e.preventDefault();
      if (!searchInput.value.trim()) return;
      store.set('vl-search', searchInput.value.trim());
      location.href = searchForm.dataset.target;
    });
  }
}
applyFilter();

/* ===== Header khi cuộn + nút lên đầu ===== */
const header = $('#header'), toTop = $('#toTop');
addEventListener('scroll', () => {
  header && header.classList.toggle('is-scrolled', scrollY > 10);
  toTop && toTop.classList.toggle('is-visible', scrollY > 600);
}, { passive: true });
if (toTop) toTop.onclick = () => scrollTo({ top: 0, behavior: 'smooth' });

/* ===== Menu mobile ===== */
const burger = $('#burger'), nav = $('#nav');
if (burger && nav) {
  burger.onclick = () => {
    const open = nav.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', open);
  };
  $$('#nav a').forEach(a => a.addEventListener('click', () => {
    nav.classList.remove('is-open'); burger.setAttribute('aria-expanded', false);
  }));
}

/* ===== Hiệu ứng xuất hiện + đếm số ===== */
const io = new IntersectionObserver(entries => entries.forEach(en => {
  if (!en.isIntersecting) return;
  en.target.classList.add('is-in');
  $$('[data-count]', en.target).forEach(countUp);
  io.unobserve(en.target);
}), { threshold: 0, rootMargin: '0px 0px -8% 0px' });
$$('.reveal').forEach(el => io.observe(el));

function countUp(el) {
  const end = +el.dataset.count, t0 = performance.now(), dur = 1400;
  (function step(t) {
    const p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.round(end * e).toLocaleString('vi-VN');
    if (p < 1) requestAnimationFrame(step);
  })(t0);
}

/* ===== Biểu mẫu báo giá ===== */
const modal = $('#modal');
function closeModal() { if (!modal) return; modal.classList.remove('is-open'); modal.setAttribute('aria-hidden', true); }
document.addEventListener('click', e => {
  const open = e.target.closest('[data-open-modal]');
  if (open && modal) {
    modal.classList.add('is-open'); modal.setAttribute('aria-hidden', false);
    $('#fNote').value = open.dataset.product ? `Cần báo giá: ${open.dataset.product}` : '';
    setTimeout(() => $('#fName').focus(), 200);
  }
  if (e.target.closest('[data-close-modal]')) closeModal();
});
addEventListener('keydown', e => e.key === 'Escape' && closeModal());

/* Gửi form: trên hosting thật (có data-form-endpoint) gửi tới gui-yeu-cau.php để chuyển về email;
   khi xem thử (mở file trên máy, bản preview) chỉ hiện thông báo minh họa. */
const endpoint = document.body.dataset.formEndpoint || (window.VL_FORM_ENDPOINT || '').trim();
const canSend = endpoint && /^https?:$/.test(location.protocol);
$$('form[data-form]').forEach(form => form.addEventListener('submit', async e => {
  e.preventDefault();
  const btn = form.querySelector('button:not([type=button])');
  const done = msg => { form.reset(); if (form.id === 'contactForm') closeModal(); toast(msg); };
  const off = document.body.dataset.formOff;
  if (off && !endpoint && /^https?:$/.test(location.protocol)) {
    // Website thật nhưng chưa nối dịch vụ nhận form: hướng khách gọi/nhắn Zalo, giữ nguyên nội dung đã nhập
    return toast(`Form tạm chưa nhận yêu cầu. Vui lòng gọi hoặc nhắn Zalo ${off}.`);
  }
  if (!canSend) return done(form.id === 'subscribe'
    ? 'Cảm ơn bạn! Chúng tôi sẽ gọi lại để tư vấn.'
    : 'Đã ghi nhận yêu cầu. Vĩnh Lộc Plastic sẽ liên hệ lại sớm.');
  const data = new FormData(form);
  data.append('page', location.href);
  if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = 'Đang gửi…'; }
  try {
    const res = await fetch(endpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } });
    const json = await res.json().catch(() => ({}));
    if (res.ok && json.ok) done(json.message || 'Đã gửi yêu cầu. Chúng tôi sẽ liên hệ lại sớm.');
    else toast(json.message || 'Chưa gửi được. Vui lòng gọi hoặc nhắn Zalo cho chúng tôi.');
  } catch (_) {
    toast('Mất kết nối. Vui lòng thử lại hoặc gọi cho chúng tôi.');
  } finally {
    if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label; }
  }
}));

$$('[data-copy]').forEach(btn => btn.addEventListener('click', () => {
  const text = btn.dataset.copy;
  const done = () => toast(`Đã sao chép ${text}`);
  if (navigator.clipboard) navigator.clipboard.writeText(text).then(done).catch(() => toast(`Số điện thoại: ${text}`));
  else toast(`Số điện thoại: ${text}`);
}));


/* ===== Giao diện sáng/tối ===== */
(function theme() {
  const root = document.documentElement;
  let saved = null;
  try { saved = localStorage.getItem('vl-theme'); } catch (_) {}
  if (saved) root.dataset.theme = saved;
  const btn = $('#themeToggle');
  if (btn) btn.onclick = () => {
    const dark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    root.dataset.theme = dark ? 'light' : 'dark';
    try { localStorage.setItem('vl-theme', root.dataset.theme); } catch (_) {}
  };
})();
