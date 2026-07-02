import asyncio, sqlite3, random, os
from datetime import date
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()

PHONE = os.getenv("PHONE", "+974 30282575")
CITY  = os.getenv("CITY", "Doha")
EMAIL = os.getenv("LINKEDIN_EMAIL", "abdallamohmed2015@gmail.com")
LIMIT = int(os.getenv("SAFE_DAILY_LIMIT", "40"))
CV    = "C:\\AutoApply\\abdalla.pdf"
NAME  = "Abdalla adam"

JOBS = [
    "Syastem Analyst",
    "IT Officer",
    "Technical Support",
    " IT Operations",
    "Software Engineer",
    "Systems Analyst",
    "Operations Supervisor",
    "Safety Officer",
    "Systems Administrator",
    "Security Manager",
    "Data Analyst",
    "CCTV Operator",
    "Access Control Officer",
]
LOCS = ["Qatar", "Dubai UAE", "Abu Dhabi UAE", "Saudi Arabia"]

# ── Database ──────────────────────────────────────────────────────────────────
def db():
    c = sqlite3.connect("C:\\AutoApply\\jobs.db")
    c.execute("""CREATE TABLE IF NOT EXISTS applied(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id TEXT UNIQUE, title TEXT, company TEXT,
        status TEXT, date TEXT)""")
    c.commit()
    return c

def done(c, jid):
    return c.execute(
        "SELECT id FROM applied WHERE job_id=?", (jid,)
    ).fetchone()

def save(c, jid, t, co, st):
    try:
        c.execute(
            "INSERT INTO applied VALUES(NULL,?,?,?,?,?)",
            (jid, t, co, st, date.today().isoformat())
        )
        c.commit()
    except:
        pass

def cnt(c):
    return c.execute(
        "SELECT COUNT(*) FROM applied WHERE date=?",
        (date.today().isoformat(),)
    ).fetchone()[0]

# ── Helpers ───────────────────────────────────────────────────────────────────
async def w(a=1.5, b=3.5):
    await asyncio.sleep(random.uniform(a, b))

async def go(page, url):
    try:
        await page.evaluate(f"window.location.href='{url}'")
        await page.wait_for_load_state("domcontentloaded", timeout=25000)
        await asyncio.sleep(4)
    except:
        await asyncio.sleep(4)

# ── Fill form fields ──────────────────────────────────────────────────────────
async def fill(page):
    for s in ['input[id*="phone"]', 'input[name*="phone"]',
              'input[placeholder*="Phone"]', 'input[type="tel"]']:
        try:
            f = await page.query_selector(s)
            if f and not await f.input_value():
                await f.fill(PHONE)
                await w(0.2, 0.4)
        except:
            pass

    for s in ['input[id*="name"]', 'input[name*="name"]',
              'input[placeholder*="Name"]']:
        try:
            f = await page.query_selector(s)
            if f:
                val = await f.input_value()
                if not val or len(val) < 2:
                    await f.fill(NAME)
                    await w(0.2, 0.4)
        except:
            pass

    for s in ['input[type="email"]', 'input[id*="email"]']:
        try:
            f = await page.query_selector(s)
            if f and not await f.input_value():
                await f.fill(EMAIL)
                await w(0.2, 0.4)
        except:
            pass

    for s in ['input[id*="city"]', 'input[name*="city"]',
              'input[placeholder*="City"]']:
        try:
            f = await page.query_selector(s)
            if f and not await f.input_value():
                await f.fill(CITY)
                await w(0.2, 0.4)
        except:
            pass

    if os.path.exists(CV):
        for fi in await page.query_selector_all('input[type="file"]'):
            try:
                await fi.set_input_files(CV)
                await w(1, 2)
            except:
                pass

    for r in await page.query_selector_all('input[type="radio"]'):
        try:
            v = (await r.get_attribute("value") or "").lower()
            if v in ("yes", "true", "1") and not await r.is_checked():
                await r.click()
                await w(0.2, 0.3)
        except:
            pass

    for s in await page.query_selector_all("select"):
        try:
            opts = await s.query_selector_all("option")
            if len(opts) > 1:
                await s.select_option(index=1)
                await w(0.2, 0.3)
        except:
            pass

    for ta in await page.query_selector_all("textarea"):
        try:
            val = await ta.input_value()
            if not val:
                txt = (
                    f"Dear Hiring Team,\n\n"
                    f"I am excited to apply for this position. "
                    f"As a Security Supervisor with over 1 year of experience "
                    f"managing 37 security personnel across 3 facilities in Doha, "
                    f"Qatar, I bring strong leadership and operational excellence. "
                    f"I achieved a 90% reduction in unauthorized access attempts "
                    f"and hold a degree in Aviation Management.\n\n"
                    f"Best regards,\n{NAME}\n{PHONE}"
                )
                await ta.fill(txt)
                await w(0.5, 1)
        except:
            pass

# ── Easy Apply ────────────────────────────────────────────────────────────────
async def apply_easy(page, url):
    try:
        await go(page, url)
        btn = None
        for s in [
            'button.jobs-apply-button',
            'button[aria-label*="Easy Apply"]',
            'button[aria-label*="easy apply"]',
        ]:
            try:
                btn = await page.wait_for_selector(s, timeout=4000)
                if btn:
                    break
            except:
                pass

        if not btn:
            return "no_easy_apply"

        await btn.click()
        await w(2, 3)

        for _ in range(12):
            await fill(page)
            await w(1, 1.5)

            for s in [
                'button[aria-label="Submit application"]',
                'button:has-text("Submit application")',
            ]:
                try:
                    b = await page.wait_for_selector(s, timeout=2000)
                    await b.click()
                    await w(2, 3)
                    return "success"
                except:
                    pass

            moved = False
            for s in [
                'button[aria-label="Continue to next step"]',
                'button[aria-label="Review your application"]',
                'button:has-text("Next")',
                'button:has-text("Review")',
            ]:
                try:
                    b = await page.wait_for_selector(s, timeout=2000)
                    await b.click()
                    await w(1, 2)
                    moved = True
                    break
                except:
                    pass

            if not moved:
                break

        try:
            d = await page.query_selector('button[aria-label="Dismiss"]')
            if d:
                await d.click()
        except:
            pass

        return "failed"
    except:
        return "failed"

# ── External Apply ────────────────────────────────────────────────────────────
async def apply_external(page, url):
    try:
        await go(page, url)

        apply_btn = None
        for s in [
            'button.jobs-apply-button',
            'button:has-text("Apply")',
            'a:has-text("Apply")',
        ]:
            try:
                apply_btn = await page.wait_for_selector(s, timeout=3000)
                if apply_btn:
                    break
            except:
                pass

        if not apply_btn:
            return "skipped"

        await apply_btn.click()
        await w(3, 5)
        await fill(page)
        await w(1, 2)

        for s in [
            'button[type="submit"]',
            'button:has-text("Submit")',
            'button:has-text("Apply")',
            'input[type="submit"]',
        ]:
            try:
                b = await page.wait_for_selector(s, timeout=3000)
                await b.click()
                await w(2, 3)
                return "success"
            except:
                pass

        return "failed"
    except:
        return "skipped"

# ── Search with pagination ────────────────────────────────────────────────────
async def search(page, conn, job, loc):
    all_links = []

    # 4 pages × 25 jobs = up to 100 jobs per search
    for page_num in range(4):
        if cnt(conn) >= LIMIT:
            break

        start = page_num * 25
        url = (
            f"https://www.linkedin.com/jobs/search/"
            f"?keywords={job.replace(' ', '+')}"
            f"&location={loc.replace(' ', '+')}"
            f"&sortBy=DD&start={start}"
        )

        print(f"\n🔍 '{job}' in '{loc}' — page {page_num + 1}")
        await go(page, url)

        for _ in range(8):
            await page.mouse.wheel(0, random.randint(400, 700))
            await w(0.4, 0.7)

        await asyncio.sleep(3)

        links = await page.evaluate("""()=>{
            const r=[], seen=new Set();
            document.querySelectorAll('a').forEach(a=>{
                if(a.href && a.href.includes('/jobs/view/') && !seen.has(a.href)){
                    seen.add(a.href);
                    const u=a.href.split('?')[0];
                    const id=u.split('/').filter(Boolean).pop();
                    const card=a.closest('li')||a.closest('div.job-card-container');
                    const tEl=card?card.querySelector(
                        '.job-card-list__title,h3,h2,strong'):null;
                    const cEl=card?card.querySelector(
                        '.job-card-container__primary-description,h4'):null;
                    r.push({
                        url:u, id:id,
                        title:tEl?tEl.innerText.trim():'',
                        company:cEl?cEl.innerText.trim():''
                    });
                }
            });
            return r;
        }""")

        existing_ids = [x['id'] for x in all_links]
        new_links = [lk for lk in links if lk['id'] not in existing_ids]
        all_links.extend(new_links)
        print(f"   Found {len(new_links)} new (total: {len(all_links)})")

        if len(new_links) == 0:
            break

    # Apply to all found jobs
    for lk in all_links:
        if cnt(conn) >= LIMIT:
            break
        if done(conn, lk['id']):
            continue

        title   = lk.get('title') or job
        company = lk.get('company') or "Unknown"
        print(f"   → {title[:38]} @ {company[:22]}...", end=" ", flush=True)

        status = await apply_easy(page, lk['url'])
        if status == "no_easy_apply":
            status = await apply_external(page, lk['url'])

        save(conn, lk['id'], title, company, status)
        icon = "✅" if status == "success" else "❌" if status == "failed" else "⏭"
        print(f"{icon} {status} [{cnt(conn)}/{LIMIT}]")

        if status in ("success", "failed"):
            delay = random.uniform(30, 60)
            print(f"   ⏳ {delay:.0f}s...")
            await asyncio.sleep(delay)

# ── Main ──────────────────────────────────────────────────────────────────────
async def main():
    conn = db()
    print(f"\n{'='*55}")
    print(f"🚀 AutoApply — abdalla mohamed ")
    print(f"   Applied today: {cnt(conn)}/{LIMIT}")
    print(f"   Jobs: {len(JOBS)} titles × {len(LOCS)} locations")
    print(f"   Pages per search: 4 (up to 100 jobs each)")
    print(f"{'='*55}\n")

    async with async_playwright() as pw:
        br = await pw.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--start-maximized",
                "--disable-infobars",
            ],
        )
        ctx = await br.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        )
        await ctx.add_init_script(
            "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
        )
        page = await ctx.new_page()

        # Login
        await page.goto(
            "https://www.linkedin.com/login",
            wait_until="domcontentloaded",
            timeout=30000,
        )
        print("⚠️ Please login to Chrome now ")
        input("✅ Press Enter After you see the feed page ...\n")
        try:
            await page.wait_for_url("**/feed/**", timeout=10000)
        except:
            pass
        await asyncio.sleep(3)
        print("✅ login successfully , Starting seaech...\n")

        # Search all combinations
        for job in JOBS:
            for loc in LOCS:
                if cnt(conn) >= LIMIT:
                    print("\n⛔ Safe daily limit reached!")
                    break
                await search(page, conn, job, loc)
                await w(2, 5)

        # Summary
        total = cnt(conn)
        rows = conn.execute(
            "SELECT title, company, status FROM applied "
            "WHERE date=? ORDER BY id DESC",
            (date.today().isoformat(),),
        ).fetchall()

        success = sum(1 for r in rows if r[2] == "success")
        failed  = sum(1 for r in rows if r[2] == "failed")
        skipped = sum(1 for r in rows if r[2] == "skipped")

        print(f"\n{'='*55}")
        print(f"✅ Done Applied today: {total}/{LIMIT}")
        print(f"   ✅ Success: {success} | ❌ Failed: {failed} | ⏭ Skipped: {skipped}")
        print(f"\n📋 Application log:")
        for r in rows:
            icon = "✅" if r[2]=="success" else "❌" if r[2]=="failed" else "⏭"
            print(f"   {icon} {r[0][:35]} @ {r[1][:25]}")
        print(f"{'='*55}")

        await br.close()
        conn.close()

if __name__ == "__main__":
    asyncio.run(main())