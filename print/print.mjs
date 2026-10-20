// Print a module's HTML to an A4 PDF with Chromium (Playwright).
// Usage: NODE_PATH="$(npm root -g)" node print/print.mjs <input.html> <output.pdf> "<footer title>"
import { createRequire } from "module";
import { resolve } from "path";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const [, , src, out, title = ""] = process.argv;
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + resolve(src));
await page.pdf({
  path: out, format: "A4", printBackground: true, preferCSSPageSize: true,
  displayHeaderFooter: true, headerTemplate: "<span></span>",
  footerTemplate: '<div style="width:100%;font-family:Inter,sans-serif;font-size:7.5px;color:#4b5260;padding:0 15mm;display:flex;justify-content:space-between">'
    + "<span>" + title + '</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
});
await browser.close();
