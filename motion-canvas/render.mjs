// Headless render: start Vite, open the editor in Chromium, press RENDER, wait for the mp4.
import {createServer} from 'vite';
import puppeteer from 'puppeteer-core';
import fs from 'node:fs';

const chrome = process.env.CHROME || '/opt/pw-browsers/chromium';
const server = await createServer({server: {port: 9000}});
await server.listen();
const browser = await puppeteer.launch({executablePath: chrome, args: ['--no-sandbox', '--use-gl=swiftshader']});
const page = await browser.newPage();
page.on('console', (m) => process.env.DEBUG && console.log('page:', m.text()));
await page.goto('http://localhost:9000/', {waitUntil: 'networkidle0'});
const before = new Set(fs.existsSync('output') ? fs.readdirSync('output', {recursive: true}) : []);
await page.waitForFunction(() => [...document.querySelectorAll('button')].some((b) => /render/i.test(b.textContent)), {timeout: 60000});
await page.evaluate(() => [...document.querySelectorAll('button')].find((b) => /^render$/i.test(b.textContent.trim()))?.click());
const t0 = Date.now();
let done = null;
while (!done && Date.now() - t0 < 30 * 60000) {
  await new Promise((r) => setTimeout(r, 2000));
  const files = fs.existsSync('output') ? fs.readdirSync('output', {recursive: true}).filter((f) => f.endsWith('.mp4') && !before.has(f)) : [];
  const idle = await page.evaluate(() => [...document.querySelectorAll('button')].some((b) => /^render$/i.test(b.textContent.trim())));
  if (files.length && idle) done = files;
}
console.log(done ? `rendered: ${done.map((f) => 'output/' + f).join(', ')}` : 'render timed out');
await browser.close();
await server.close();
