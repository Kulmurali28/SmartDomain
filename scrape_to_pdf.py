"""
VIT Pune Website Scraper → PDF
Scrapes key pages from https://www.vit.edu and saves them as PDFs.
Then upload the PDFs to SiteSense as knowledge sources.

Usage:
    python scrape_to_pdf.py
"""

import asyncio
import os
from playwright.async_api import async_playwright

BASE_URL = "https://www.vit.edu"

# ── All confirmed real pages from vit.edu ────────────────────────────────────
PAGES = [
    # Institute / General
    (f"{BASE_URL}/",                                        "home.pdf"),
    (f"{BASE_URL}/admissions",                             "admissions.pdf"),
    (f"{BASE_URL}/infrastructure/",                        "infrastructure.pdf"),
    (f"{BASE_URL}/research/",                              "research.pdf"),
    (f"{BASE_URL}/alumni/",                                "alumni.pdf"),
    (f"{BASE_URL}/apex/",                                  "alumni_apex_entrepreneurship.pdf"),

    # Departments — About
    (f"{BASE_URL}/computer/",                              "dept_computer_engineering.pdf"),
    (f"{BASE_URL}/IT/about/",                              "dept_IT_about.pdf"),
    (f"{BASE_URL}/CSE-AI/about/",                          "dept_CSE_AI_about.pdf"),
    (f"{BASE_URL}/CSE-AI-ML/",                             "dept_CSE_AIML.pdf"),
    (f"{BASE_URL}/mechanical/",                            "dept_mechanical.pdf"),
    (f"{BASE_URL}/CIVIL/",                                 "dept_civil.pdf"),
    (f"{BASE_URL}/instrumentation/",                       "dept_instrumentation.pdf"),

    # Placements
    (f"{BASE_URL}/CSE-AI/placements/",                     "placements_CSE_AI.pdf"),
    (f"{BASE_URL}/computer/placements/",                   "placements_computer.pdf"),
    (f"{BASE_URL}/IT/placements/",                         "placements_IT.pdf"),
    (f"{BASE_URL}/mechanical/placements/",                 "placements_mechanical.pdf"),

    # Facilities
    (f"{BASE_URL}/computer/facilities/",                   "facilities_computer.pdf"),
    (f"{BASE_URL}/CSE-AI-ML/facilities/",                  "facilities_CSE_AIML.pdf"),
    (f"{BASE_URL}/mechanical/facilities/",                 "facilities_mechanical.pdf"),
    (f"{BASE_URL}/CIVIL/facilities/",                      "facilities_civil.pdf"),
    (f"{BASE_URL}/instrumentation/facilities/",            "facilities_instrumentation.pdf"),

    # Directly accessible PDFs (fees, admission notices)
    # These will be downloaded as-is by the browser PDF renderer
    (
        "https://www.vit.edu/wp-content/uploads/2026/07/FRA-Fee-Structure-AY-2026-27.pdf",
        "fee_structure_2026_27.pdf"
    ),
    (
        "https://www.vit.edu/wp-content/uploads/2026/09/Important-Instructions-and-Links-for-FY-CAP-Admissions-%E2%80%93-Academic-Year-2026%E2%80%9327-1.pdf",
        "admissions_FY_CAP_2026_27.pdf"
    ),
]

# ── Output folder ─────────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "college_pdfs")


async def scrape_pages():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"\n📁 Saving PDFs to: {OUTPUT_DIR}")
    print(f"📄 Total pages to scrape: {len(PAGES)}\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )
        page = await context.new_page()

        success = []
        failed = []

        for url, filename in PAGES:
            output_path = os.path.join(OUTPUT_DIR, filename)
            print(f"  ⏳ Scraping: {url}")
            try:
                await page.goto(url, wait_until="networkidle", timeout=45000)

                # Wait a bit for JS-rendered content to load
                await page.wait_for_timeout(2000)

                await page.pdf(
                    path=output_path,
                    format="A4",
                    print_background=True,
                    margin={
                        "top": "15mm",
                        "bottom": "15mm",
                        "left": "12mm",
                        "right": "12mm"
                    }
                )
                size_kb = round(os.path.getsize(output_path) / 1024, 1)
                print(f"  ✔ Saved:  {filename}  ({size_kb} KB)")
                success.append(filename)

            except Exception as e:
                print(f"  ✘ Failed: {filename}")
                print(f"           Reason: {e}\n")
                failed.append((filename, str(e)))

        await browser.close()

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*55}")
    print(f"  Done!  {len(success)} saved,  {len(failed)} failed.")

    if failed:
        print(f"\n  Failed pages:")
        for name, err in failed:
            print(f"    - {name}")

    print(f"\n  Next step:")
    print(f"  1. Open http://localhost:3001")
    print(f"  2. Open your bot → Sources tab")
    print(f"  3. Upload each PDF from: {OUTPUT_DIR}")
    print(f"  4. Click Ingest and wait for status: indexed")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    asyncio.run(scrape_pages())
