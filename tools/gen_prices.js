#!/usr/bin/env node
// Regenerate northroom_prices.json from the LIVE storefront catalog.
// Usage: node tools/gen_prices.js [baseUrl]   (default https://www.northroomhome.com)
// Mirrors cart.html: products.js, then prices.js overrides. Only published catalog SKUs are included.
const fs = require('fs');
const path = require('path');
const base = (process.argv[2] || 'https://www.northroomhome.com').replace(/\/$/, '');
(async () => {
  const g = {};
  for (const f of ['products.js', 'prices.js']) {
    const r = await fetch(`${base}/${f}?v=${Date.now()}`, { cache: 'no-store' });
    if (!r.ok) throw new Error(`${f}: HTTP ${r.status}`);
    new Function('window', await r.text())(g);
  }
  const products = g.NORTHROOM_PRODUCTS || [];
  if (products.length < 50) throw new Error(`catalog too small (${products.length}); refusing to write`);
  const skus = {};
  for (const p of products) {
    const cents = Math.round(Number(p.price) * 100);
    if (!p.id || !(cents > 0)) throw new Error(`bad product ${JSON.stringify(p).slice(0, 120)}`);
    skus[p.id] = { title: p.title, unit_amount: cents, price_matched: !!p.priceMatched };
  }
  const out = { generated_at: new Date().toISOString(), source: `${base}/products.js`, count: products.length, skus };
  const dest = path.join(__dirname, '..', 'northroom_prices.json');
  fs.writeFileSync(dest, JSON.stringify(out, null, 1) + '\n');
  console.log(`wrote ${dest}: ${products.length} SKUs`);
})().catch((e) => { console.error(e.message); process.exit(1); });
