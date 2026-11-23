// Mobil öykünme + CPU yavaşlatma altında tıklama gecikmesi (INP) ölçümü.
// Kullanım: node inp.mjs <url> <seçici> <bekleme_ms> <cpu_kat>
import { spawn } from 'node:child_process';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const [url, sel, waitMs = '4000', cpu = '4', ek = ''] = process.argv.slice(2);
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const prof = mkdtempSync(join(process.env.TMPDIR || tmpdir(), 'inp-'));
const port = 9300 + Math.floor(Math.random() * 500);
const ch = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, '--no-first-run', '--mute-audio', 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let ws, id = 0; const pend = new Map();
for (let i = 0; i < 50; i++) {
  try { const t = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); const pg = t.find((x) => x.type === 'page'); if (pg) { ws = new WebSocket(pg.webSocketDebuggerUrl); break; } } catch {}
  await sleep(200);
}
await new Promise((r) => ws.addEventListener('open', r));
ws.addEventListener('message', (m) => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); } });
const cmd = (method, params = {}) => new Promise((r) => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (expr) => (await cmd('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true })).result?.result?.value;

await cmd('Page.enable'); await cmd('Runtime.enable');
await cmd('Emulation.setDeviceMetricsOverride', { width: 375, height: 812, deviceScaleFactor: 3, mobile: true });
await cmd('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
await cmd('Emulation.setCPUThrottlingRate', { rate: Number(cpu) });
await cmd('Network.enable');
await cmd('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: 200000, uploadThroughput: 94000 }); // ~1,6 Mbit/sn "yavaş 4G"
if (ek) await cmd('Page.addScriptToEvaluateOnNewDocument', { source: ek });
await cmd('Page.addScriptToEvaluateOnNewDocument', { source: `try{localStorage.setItem('ibav_cookieConsent','rejected')}catch(e){};window.__ev=[];new PerformanceObserver(l=>{for(const e of l.getEntries())window.__ev.push({n:e.name,d:Math.round(e.duration),delay:Math.round(e.processingStart-e.startTime),proc:Math.round(e.processingEnd-e.processingStart),pres:Math.round(e.startTime+e.duration-e.processingEnd),t:Math.round(e.startTime)})}).observe({type:'event',buffered:true,durationThreshold:16});` });
const t0 = Date.now();
await cmd('Page.navigate', { url });
await sleep(Number(waitMs));
const r = await ev(`(()=>{const el=document.querySelector(${JSON.stringify(sel)});if(!el)return null;const b=el.getBoundingClientRect();return {x:b.x+b.width/2,y:b.y+b.height/2,rs:document.readyState}})()`);
if (!r) { console.log('seçici yok', await ev('location.href+" "+document.readyState+" "+document.title')); process.exit(1); }
const tp = [{ x: r.x, y: r.y }];
await cmd('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: tp });
await sleep(60);
await cmd('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
await sleep(1500);
const evs = await ev('window.__ev.filter(e=>/pointer|click|touch/.test(e.n))');
const inp = Math.max(0, ...evs.map((e) => e.d));
console.log(JSON.stringify({ sel, waitMs: Number(waitMs), cpu: Number(cpu), readyState: r.rs, inp, evs }));
ws.close(); ch.kill();
