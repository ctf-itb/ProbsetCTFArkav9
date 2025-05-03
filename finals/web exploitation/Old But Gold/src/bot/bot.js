const puppeteer = require('puppeteer');

const CONFIG = {
    APPNAME: process.env['APPNAME'] || "Admin",
    APPURL: process.env['APPURL'] || "http://172.17.0.1",
    APPURLREGEX: process.env['APPURLREGEX'] || "^.*$",
    APPLIMITTIME: Number(process.env['APPLIMITTIME'] || "60000"),
    APPLIMIT: Number(process.env['APPLIMIT'] || "5"),
}

console.table(CONFIG)

const initBrowser = puppeteer.launch({
    executablePath: "/usr/bin/chromium-browser",
    headless: 'new',
    args: [
        '--disable-dev-shm-usage',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-gpu',
        '--no-gpu',
        '--disable-default-apps',
        '--disable-translate',
        '--disable-device-discovery-notifications',
        '--disable-software-rasterizer',
        '--disable-xss-auditor',
        '--incognito'
    ],
    ipDataDir: '/home/bot/data/',
    ignoreHTTPSErrors: true
});

console.log("Bot started...");

module.exports = {
    name: CONFIG.APPNAME,
    urlRegex: CONFIG.APPURLREGEX,
    rateLimit: {
        windowMs: CONFIG.APPLIMITTIME,
        max: CONFIG.APPLIMIT
    },
    bot: async (urlToVisit) => {
        const browser = await initBrowser;
        const context = await browser.createBrowserContext(); 
        const page = await context.newPage();
        page.setDefaultTimeout(5000);

        try {
            console.log(`Bot visiting: ${urlToVisit}`);
            await page.goto(urlToVisit, { waitUntil: 'networkidle2' });

            await page.waitForSelector('body', { timeout: 5000 });

            const viewport = page.viewport();
            const centerX = viewport.width / 2;
            const centerY = viewport.height / 2;

            const [response] = await Promise.all([
                page.waitForNavigation({ timeout: 5000 }).catch(() => null),
                page.mouse.click(centerX, centerY)
            ]);

            await context.close();
            return true;
        } catch (e) {
            console.error(e);
            await context.close();
            return false;
        }
    }
}; 