/* teler.net: progressive enhancement only. Without this file every section still reads top to bottom. */
(() => {
  'use strict';

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const smooth = (x) => x * x * (3 - 2 * x);

  /* One rAF-throttled scroll/resize loop that every feature subscribes to. */
  const onFrame = [];
  let ticking = false;
  const requestTick = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      onFrame.forEach((fn) => fn());
    });
  };
  window.addEventListener('scroll', requestTick, { passive: true });
  window.addEventListener('resize', requestTick);

  /* ---------------- Nav: shrink, progress, active section, mobile menu ---------------- */
  const nav = document.querySelector('[data-nav]');
  if (nav) {
    const progress = nav.querySelector('.nav-progress');
    const links = [...nav.querySelectorAll('.nav-links a')];
    const indicator = nav.querySelector('.nav-indicator');
    const sections = links
      .map((a) => document.getElementById(a.hash.slice(1)))
      .filter(Boolean);
    let current = null;

    const moveIndicator = (link) => {
      if (!indicator) return;
      if (!link) { indicator.classList.remove('is-on'); return; }
      indicator.style.setProperty('--ix', `${link.offsetLeft}px`);
      indicator.style.setProperty('--iw', `${link.offsetWidth}px`);
      indicator.classList.add('is-on');
    };

    onFrame.push(() => {
      const y = window.scrollY;
      const max = document.documentElement.scrollHeight - window.innerHeight;
      nav.classList.toggle('is-scrolled', y > 24);
      if (progress) progress.style.setProperty('--progress', max > 0 ? (y / max).toFixed(4) : 0);

      let active = null;
      const line = window.innerHeight * 0.4;
      sections.forEach((s) => { if (s.getBoundingClientRect().top <= line) active = s.id; });
      if (active !== current) {
        current = active;
        const link = links.find((a) => a.hash === `#${active}`) || null;
        links.forEach((a) => a.classList.toggle('is-active', a === link));
        moveIndicator(link);
      }
    });
    window.addEventListener('resize', () => moveIndicator(links.find((a) => a.classList.contains('is-active'))));

    // Switching language keeps you on the section you were reading.
    document.querySelectorAll('[data-lang-switch]').forEach((a) => {
      a.addEventListener('click', () => {
        const base = a.getAttribute('href').split('#')[0];
        a.setAttribute('href', current ? `${base}#${current}` : base);
      });
    });

    const toggle = nav.querySelector('.nav-toggle');
    const menu = document.getElementById('mobile-menu');
    if (toggle && menu) {
      const setOpen = (open) => {
        toggle.setAttribute('aria-expanded', String(open));
        toggle.setAttribute('aria-label', open ? (toggle.dataset.labelClose || 'Close menu') : (toggle.dataset.labelOpen || 'Open menu'));
        document.body.style.overflow = open ? 'hidden' : '';
        if (open) {
          menu.hidden = false;
          requestAnimationFrame(() => requestAnimationFrame(() => menu.classList.add('is-open')));
        } else {
          menu.classList.remove('is-open');
          setTimeout(() => { if (!menu.classList.contains('is-open')) menu.hidden = true; }, reduceMotion.matches ? 0 : 400);
        }
      };
      toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));
      menu.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => setOpen(false)));
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') { setOpen(false); toggle.focus(); }
      });
      window.matchMedia('(min-width: 861px)').addEventListener('change', (e) => { if (e.matches) setOpen(false); });
    }
  }

  /* ---------------- Hero: courier network canvas ---------------- */
  const canvas = document.querySelector('[data-network]');
  const hero = document.querySelector('[data-hero]');
  if (canvas && hero) {
    const ctx = canvas.getContext('2d');
    let w = 0, h = 0, dpr = 1, hubs = [], edges = [], packets = [], running = false, raf = 0;
    const mouse = { x: -9999, y: -9999 };

    const build = () => {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = hero.clientWidth; h = hero.clientHeight;
      canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      // Jittered grid of hubs, so the network covers the hero evenly.
      const cell = w < 700 ? 120 : 150;
      hubs = [];
      for (let y = cell * 0.4; y < h; y += cell) {
        for (let x = cell * 0.3; x < w; x += cell) {
          hubs.push({
            x: x + (Math.random() - 0.5) * cell * 0.8,
            y: y + (Math.random() - 0.5) * cell * 0.8,
            major: Math.random() < 0.12,
            phase: Math.random() * Math.PI * 2,
            links: [],
          });
        }
      }
      // Connect each hub to its two nearest neighbours.
      const seen = new Set();
      edges = [];
      hubs.forEach((a, i) => {
        hubs
          .map((b, j) => ({ j, d: (a.x - b.x) ** 2 + (a.y - b.y) ** 2 }))
          .filter((o) => o.j !== i)
          .sort((p, q) => p.d - q.d)
          .slice(0, 2)
          .forEach(({ j }) => {
            const key = i < j ? `${i}-${j}` : `${j}-${i}`;
            if (seen.has(key)) return;
            seen.add(key);
            const b = hubs[j];
            const mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2;
            const nx = -(b.y - a.y) * 0.18, ny = (b.x - a.x) * 0.18;
            const e = { a: i, b: j, cx: mx + nx, cy: my + ny };
            edges.push(e);
            a.links.push(e); b.links.push(e);
          });
      });
      const count = Math.round(clamp((w * h) / 70000, 6, 18));
      packets = Array.from({ length: count }, () => spawnPacket());
    };

    const spawnPacket = (from) => {
      const start = from ?? Math.floor(Math.random() * hubs.length);
      const options = hubs[start].links;
      const edge = options[Math.floor(Math.random() * options.length)];
      return { edge, from: start, t: Math.random() * (from === undefined ? 1 : 0), speed: 0.0025 + Math.random() * 0.003, trail: [] };
    };

    const pointOn = (e, from, t) => {
      const A = hubs[from], B = hubs[from === e.a ? e.b : e.a];
      const u = 1 - t;
      return { x: u * u * A.x + 2 * u * t * e.cx + t * t * B.x, y: u * u * A.y + 2 * u * t * e.cy + t * t * B.y };
    };

    const draw = (time = 0) => {
      ctx.clearRect(0, 0, w, h);
      // Routes
      ctx.lineWidth = 1;
      edges.forEach((e) => {
        const A = hubs[e.a], B = hubs[e.b];
        const near = Math.hypot((A.x + B.x) / 2 - mouse.x, (A.y + B.y) / 2 - mouse.y);
        const glow = clamp(1 - near / 260);
        ctx.strokeStyle = `rgba(201,161,74,${0.07 + glow * 0.25})`;
        ctx.beginPath(); ctx.moveTo(A.x, A.y); ctx.quadraticCurveTo(e.cx, e.cy, B.x, B.y); ctx.stroke();
      });
      // Hubs
      hubs.forEach((p) => {
        const near = clamp(1 - Math.hypot(p.x - mouse.x, p.y - mouse.y) / 220);
        ctx.fillStyle = `rgba(201,161,74,${0.25 + near * 0.6})`;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.major ? 2.6 : 1.6, 0, Math.PI * 2); ctx.fill();
        if (p.major) {
          const k = ((time / 2600) + p.phase) % 1;
          ctx.strokeStyle = `rgba(201,161,74,${0.35 * (1 - k)})`;
          ctx.beginPath(); ctx.arc(p.x, p.y, 3 + k * 22, 0, Math.PI * 2); ctx.stroke();
        }
      });
      // Parcels with a short trail
      packets.forEach((pk) => {
        const pt = pointOn(pk.edge, pk.from, pk.t);
        pk.trail.push(pt);
        if (pk.trail.length > 14) pk.trail.shift();
        for (let i = 1; i < pk.trail.length; i++) {
          ctx.strokeStyle = `rgba(235,211,156,${(i / pk.trail.length) * 0.45})`;
          ctx.lineWidth = 1.5;
          ctx.beginPath(); ctx.moveTo(pk.trail[i - 1].x, pk.trail[i - 1].y); ctx.lineTo(pk.trail[i].x, pk.trail[i].y); ctx.stroke();
        }
        ctx.save();
        ctx.translate(pt.x, pt.y);
        ctx.shadowColor = 'rgba(201,161,74,.9)'; ctx.shadowBlur = 10;
        ctx.fillStyle = '#e3c27a';
        ctx.fillRect(-2.5, -2.5, 5, 5);
        ctx.restore();
      });
    };

    const step = (time) => {
      packets.forEach((pk, i) => {
        pk.t += pk.speed;
        if (pk.t >= 1) {
          const arrived = pk.from === pk.edge.a ? pk.edge.b : pk.edge.a;
          packets[i] = { ...spawnPacket(arrived), trail: pk.trail };
        }
      });
      draw(time);
      if (running) raf = requestAnimationFrame(step);
    };

    const start = () => { if (running || reduceMotion.matches) return; running = true; raf = requestAnimationFrame(step); };
    const stop = () => { running = false; cancelAnimationFrame(raf); };

    build();
    if (reduceMotion.matches) draw(); else start();

    new IntersectionObserver(([entry]) => (entry.isIntersecting ? start() : stop())).observe(hero);
    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => { build(); if (!running) draw(); }, 150);
    });

    // Cursor: network glow, gold spotlight and a slight portrait tilt.
    const portrait = hero.querySelector('[data-tilt]');
    if (finePointer.matches) {
      hero.addEventListener('pointermove', (e) => {
        const r = hero.getBoundingClientRect();
        mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
        hero.style.setProperty('--mx', `${mouse.x}px`);
        hero.style.setProperty('--my', `${mouse.y}px`);
        if (portrait && !reduceMotion.matches) {
          const px = (e.clientX / window.innerWidth) - 0.5, py = (e.clientY / window.innerHeight) - 0.5;
          portrait.style.setProperty('--ry', `${(px * 8).toFixed(2)}deg`);
          portrait.style.setProperty('--rx', `${(-py * 8).toFixed(2)}deg`);
        }
      });
      hero.addEventListener('pointerleave', () => {
        mouse.x = mouse.y = -9999;
        portrait?.style.setProperty('--rx', '0deg');
        portrait?.style.setProperty('--ry', '0deg');
      });
    }
  }

  /* ---------------- Count-up for the career numbers ---------------- */
  const counters = document.querySelectorAll('[data-count]');
  if (counters.length && !reduceMotion.matches) {
    counters.forEach((el) => { el.textContent = `0${el.dataset.suffix || ''}`; });
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        io.unobserve(el);
        const target = parseInt(el.dataset.count, 10);
        const suffix = el.dataset.suffix || '';
        const delay = el.getBoundingClientRect().top < window.innerHeight ? 900 : 0;
        setTimeout(() => {
          const t0 = performance.now();
          const tick = (now) => {
            const k = clamp((now - t0) / 1600);
            el.textContent = `${Math.round(target * (1 - Math.pow(1 - k, 4)))}${suffix}`;
            if (k < 1) requestAnimationFrame(tick);
          };
          requestAnimationFrame(tick);
        }, delay);
      });
    }, { threshold: 0.5 });
    counters.forEach((el) => io.observe(el));
  }

  /* ---------------- About: statement lights up word by word as you read ---------------- */
  const statement = document.querySelector('[data-words]');
  if (statement && !reduceMotion.matches) {
    const words = statement.textContent.trim().split(/\s+/);
    statement.setAttribute('aria-label', statement.textContent.trim());
    statement.innerHTML = words.map((word) => `<span class="w" aria-hidden="true">${word}</span>`).join(' ');
    const spans = [...statement.querySelectorAll('.w')];
    let last = -1;
    onFrame.push(() => {
      const r = statement.getBoundingClientRect();
      const vh = window.innerHeight;
      const p = clamp((vh * 0.85 - r.top) / (r.height + vh * 0.3));
      const lit = p * spans.length * 1.05;
      if (Math.abs(lit - last) < 0.05) return;
      last = lit;
      spans.forEach((s, i) => s.style.setProperty('--o', (0.16 + 0.84 * clamp(lit - i)).toFixed(3)));
    });
  }

  /* ---------------- Journey: scroll drives a parcel along the career route ---------------- */
  const journey = document.querySelector('[data-journey]');
  if (journey) {
    const route = journey.querySelector('[data-route]');
    const parcel = journey.querySelector('[data-parcel]');
    const dotsLayer = journey.querySelector('[data-stop-dots]');
    const stops = [...journey.querySelectorAll('.stop')];
    const counter = journey.querySelector('[data-stop-index]');
    const n = stops.length;
    const canPin = window.matchMedia('(min-width: 861px) and (min-height: 600px)');
    let pinned = false, L = 0, dots = [], activeIdx = -1;

    const buildDots = () => {
      L = route.getTotalLength();
      route.style.strokeDasharray = `${L}`;
      dotsLayer.innerHTML = '';
      dots = stops.map((stop, i) => {
        const pt = route.getPointAtLength((L * i) / (n - 1));
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('class', 'jr-dot');
        const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        c.setAttribute('cx', pt.x); c.setAttribute('cy', pt.y); c.setAttribute('r', 7);
        const t = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        t.setAttribute('x', pt.x);
        t.setAttribute('y', pt.y < 105 ? pt.y + 36 : pt.y - 22);
        t.textContent = stop.dataset.year;
        g.append(c, t);
        dotsLayer.append(g);
        return g;
      });
    };

    const setActive = (i) => {
      if (i === activeIdx) return;
      activeIdx = i;
      stops.forEach((s, k) => s.classList.toggle('is-active', k === i));
      if (counter) counter.textContent = String(i + 1);
    };

    const update = () => {
      if (!pinned) return;
      const total = journey.offsetHeight - window.innerHeight;
      const p = clamp(-journey.getBoundingClientRect().top / total);
      const t = p * (n - 1);
      const i = Math.min(Math.floor(t), n - 1);
      const f = t - i;
      // Dwell at each stop, travel in between.
      const pos = i >= n - 1 ? 1 : (i + smooth(clamp((f - 0.3) / 0.4))) / (n - 1);
      const len = L * pos;
      const pt = route.getPointAtLength(len);
      const ahead = route.getPointAtLength(Math.min(L, len + 1));
      const angle = Math.atan2(ahead.y - pt.y, ahead.x - pt.x) * 180 / Math.PI;
      parcel.setAttribute('transform', `translate(${pt.x} ${pt.y}) rotate(${angle.toFixed(1)})`);
      route.style.strokeDashoffset = `${L - len}`;
      const active = clamp(f < 0.5 ? i : i + 1, 0, n - 1);
      dots.forEach((d, k) => {
        d.classList.toggle('is-passed', k / (n - 1) <= pos + 0.001);
        d.classList.toggle('is-active', k === active);
      });
      setActive(active);
    };

    const configure = () => {
      const want = canPin.matches && !reduceMotion.matches;
      if (want === pinned) return;
      pinned = want;
      journey.classList.toggle('is-pinned', pinned);
      if (pinned) { if (!dots.length) buildDots(); activeIdx = -1; update(); }
      else stops.forEach((s) => s.classList.remove('is-active'));
    };

    // Clicking a hub on the map scrolls to that stop.
    dotsLayer.parentElement.parentElement.addEventListener('click', (e) => {
      const g = e.target.closest('.jr-dot');
      if (!g || !pinned) return;
      const k = dots.indexOf(g);
      const total = journey.offsetHeight - window.innerHeight;
      window.scrollTo({ top: journey.offsetTop + (total * k) / (n - 1), behavior: reduceMotion.matches ? 'auto' : 'smooth' });
    });

    canPin.addEventListener('change', configure);
    reduceMotion.addEventListener('change', configure);
    configure();
    onFrame.push(update);
  }

  /* ---------------- Projects: reveal once, run the app mock-ups only while visible ---------------- */
  const revealables = document.querySelectorAll('[data-reveal]');
  if (revealables.length) {
    if (!('IntersectionObserver' in window)) {
      revealables.forEach((el) => el.classList.add('is-visible'));
    } else {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) entry.target.classList.add('is-visible');
        });
      }, { threshold: 0.18, rootMargin: '0px 0px -40px 0px' });
      revealables.forEach((el) => io.observe(el));
    }
  }

  /* ---------------- Cursor spotlight (expertise rows, in-house tools) ---------------- */
  if (finePointer.matches) {
    document.querySelectorAll('[data-spotlight]').forEach((el) => {
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        el.style.setProperty('--x', `${e.clientX - r.left}px`);
        el.style.setProperty('--y', `${e.clientY - r.top}px`);
      });
    });
  }

  /* ---------------- Magnetic buttons (re-bound after HTMX swaps) ---------------- */
  const bindMagnetic = (root) => {
    if (!finePointer.matches || reduceMotion.matches) return;
    root.querySelectorAll('[data-magnetic]').forEach((el) => {
      if (el.dataset.magneticBound) return;
      el.dataset.magneticBound = '1';
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        const dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2);
        el.style.transform = `translate(${dx * 0.18}px, ${dy * 0.3}px)`;
      });
      el.addEventListener('pointerleave', () => { el.style.transform = ''; });
    });
  };
  bindMagnetic(document);
  document.addEventListener('htmx:load', (e) => bindMagnetic(e.target));

  /* ---------------- Copy email ---------------- */
  document.querySelectorAll('[data-copy]').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const done = btn.querySelector('.copy-done');
      try {
        await navigator.clipboard.writeText(btn.dataset.copy);
        if (done) done.textContent = btn.dataset.copied || 'Copied';
      } catch {
        if (done) done.textContent = btn.dataset.copyFallback || 'Press Ctrl+C';
      }
      btn.classList.add('is-copied');
      setTimeout(() => btn.classList.remove('is-copied'), 1800);
    });
  });

  requestTick();
})();
