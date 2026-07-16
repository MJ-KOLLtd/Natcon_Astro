const TARGET = new Date('2026-07-30T08:00:00+08:00').getTime();

function pad(n: number) {
  return String(n).padStart(2, '0');
}

function remainingParts(remaining: number) {
  return {
    days: Math.floor(remaining / 86400000),
    hours: Math.floor((remaining % 86400000) / 3600000),
    mins: Math.floor((remaining % 3600000) / 60000),
    secs: Math.floor((remaining % 60000) / 1000),
  };
}

function tickCompact() {
  const nodes = document.querySelectorAll('[data-nc-countdown-compact]');
  if (!nodes.length) return;

  const remaining = TARGET - Date.now();
  nodes.forEach((node) => {
    if (remaining <= 0) {
      node.textContent = 'Live now';
      node.classList.add('is-live');
      return;
    }
    const { days, hours, mins } = remainingParts(remaining);
    node.textContent = `${days}d ${pad(hours)}h ${pad(mins)}m`;
  });
}

function tickFull() {
  const root = document.querySelector('[data-nc-countdown]');
  if (!root) return;

  const daysEl = root.querySelector('[data-nc-countdown-days]');
  const hoursEl = root.querySelector('[data-nc-countdown-hours]');
  const minsEl = root.querySelector('[data-nc-countdown-mins]');
  const secsEl = root.querySelector('[data-nc-countdown-secs]');
  const labelEl = root.querySelector('.nc-countdown-label');
  if (!daysEl || !hoursEl || !minsEl || !secsEl) return;

  const remaining = TARGET - Date.now();
  if (remaining <= 0) {
    root.classList.add('is-live');
    daysEl.textContent = '00';
    hoursEl.textContent = '00';
    minsEl.textContent = '00';
    secsEl.textContent = '00';
    if (labelEl) labelEl.textContent = 'Livestream is active';
    return;
  }

  const { days, hours, mins, secs } = remainingParts(remaining);
  daysEl.textContent = String(days);
  hoursEl.textContent = pad(hours);
  minsEl.textContent = pad(mins);
  secsEl.textContent = pad(secs);
}

function tick() {
  tickCompact();
  tickFull();
}

export function initCountdown() {
  if (window.__ncCountdownInit) return;
  window.__ncCountdownInit = true;
  tick();
  window.setInterval(tick, 1000);
}

declare global {
  interface Window {
    __ncCountdownInit?: boolean;
  }
}