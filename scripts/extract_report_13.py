import asyncio
import sys
import os
from datetime import datetime
from playwright.async_api import async_playwright

# Default config
DEFAULT_URL = 'https://rlisystems.ru/conterra/'
DEFAULT_LOGIN = 'pl_11640'
DEFAULT_PASSWORD = 'Qwerty123'
DEFAULT_TERMINAL = 'Терминал Врангель'

async def extract_report_13(start_date: str, end_date: str, output_dir: str = '/tmp'):
    """
    Extract report #13 'Движение по импорту' from ДЕЛО ТЕХ system.
    
    Args:
        start_date: Start date in format DD.MM.YYYY
        end_date: End date in format DD.MM.YYYY
        output_dir: Directory to save screenshots
    
    Returns:
        Path to the screenshot file with the report data
    """
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True, 
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        context = await browser.new_context(viewport={'width': 1280, 'height': 1024})
        page = await context.new_page()
        
        print(f"[1/6] Opening {DEFAULT_URL}...")
        await page.goto(DEFAULT_URL, wait_until='networkidle')
        await asyncio.sleep(5)
        
        # Step 2: Login via JavaScript (most reliable method)
        print("[2/6] Logging in...")
        await page.evaluate('''() => {
            const inputs = document.querySelectorAll('.v-textfield');
            if (inputs.length >= 2) {
                inputs[0].value = '''' + DEFAULT_LOGIN + '''';
                inputs[0].dispatchEvent(new Event('input', {bubbles:true}));
                inputs[0].dispatchEvent(new Event('change', {bubbles:true}));
                inputs[1].value = '''' + DEFAULT_PASSWORD + '''';
                inputs[1].dispatchEvent(new Event('input', {bubbles:true}));
                inputs[1].dispatchEvent(new Event('change', {bubbles:true}));
            }
            const buttons = document.querySelectorAll('.v-button');
            for (let b of buttons) {
                if (b.textContent.includes('Вход')) { b.click(); break; }
            }
        }''')
        
        await asyncio.sleep(15)
        
        # Step 3: Select terminal
        print("[3/6] Selecting terminal...")
        await page.click('.v-filterselect')
        await asyncio.sleep(2)
        
        # Find and click the terminal
        await page.evaluate('''() => {
            const items = document.querySelectorAll('.gwt-MenuItem, .v-filterselect-suggestmenu .gwt-MenuItem');
            for (let item of items) {
                if (item.textContent.includes('Терминал Врангель')) {
                    item.click();
                    return;
                }
            }
        }''')
        await asyncio.sleep(10)
        
        # Step 4: Navigate to menu
        print("[4/6] Navigating to Отчетность по обработке груза...")
        
        # Click on "Дополнительные услуги" arrow
        await page.mouse.click(200, 570)
        await asyncio.sleep(3)
        
        # Click on "Отчетность по обработке груза"
        await page.mouse.click(150, 700)
        await asyncio.sleep(10)
        
        # Step 5: Open report #13
        print("[5/6] Opening report #13...")
        await page.locator('text=13. Движение по импорту').click(timeout=5000)
        await asyncio.sleep(5)
        
        # Set dates using JavaScript
        print(f"[6/6] Setting dates: {start_date} - {end_date}...")
        await page.evaluate(f'''() => {{
            const dateInputs = document.querySelectorAll('.v-datefield-textfield');
            if (dateInputs.length >= 2) {{
                dateInputs[0].value = '{start_date}';
                dateInputs[0].dispatchEvent(new Event('input', {{bubbles:true}}));
                dateInputs[0].dispatchEvent(new Event('change', {{bubbles:true}}));
                dateInputs[1].value = '{end_date}';
                dateInputs[1].dispatchEvent(new Event('input', {{bubbles:true}}));
                dateInputs[1].dispatchEvent(new Event('change', {{bubbles:true}}));
            }}
        }}''')
        await asyncio.sleep(2)
        
        # Click ПОКАЗАТЬ ОТЧЁТ
        await page.evaluate('''() => {
            const buttons = document.querySelectorAll('.v-button');
            for (let b of buttons) {
                const text = b.textContent || b.innerText || '';
                if (text.toUpperCase().includes('ПОКАЗАТЬ')) {
                    b.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true}));
                    break;
                }
            }
        }''')
        
        await asyncio.sleep(15)
        
        # Save screenshot
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = os.path.join(output_dir, f'report_13_{timestamp}.png')
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"✓ Screenshot saved: {screenshot_path}")
        
        await browser.close()
        return screenshot_path

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python extract_report_13.py <start_date> <end_date> [output_dir]")
        print("Example: python extract_report_13.py 10.06.2026 20.06.2026 /tmp")
        sys.exit(1)
    
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else '/tmp'
    
    screenshot = asyncio.run(extract_report_13(start_date, end_date, output_dir))
    print(f"\nReport generated: {screenshot}")
