---
name: delo-report-13
description: Extract report #13 'Движение по импорту' from ДЕЛО ТЕХ (rlisystems.ru/conterra/) for Терминал Врангель. Trigger when user asks for 'Отчёт 13', 'Движение по импорту', 'отчётность по обработке груза', or any report from the ДЕЛО ТЕХ system for a specific date range. Automatically logs in, navigates to the report, sets dates, generates the report, and creates an Excel file with the data.
---

# ДЕЛО ТЕХ — Отчёт №13: Движение по импорту

## Overview

This skill automates extraction of report #13 from the ДЕЛО ТЕХ (РОЛИС) system at https://rlisystems.ru/conterra/ for ООО "РУСАЛТРАНС" (Терминал Врангель).

## Authentication

- **Login**: `pl_11640`
- **Password**: `Qwerty123`
- **Terminal**: Терминал Врангель

Login is performed via JavaScript evaluation (direct DOM manipulation) — native Playwright fill/click methods fail on this Vaadin 7.7.15 application.

## Workflow

### Step 1: Login
1. Open https://rlisystems.ru/conterra/
2. Set `.v-textfield[0]` to login, `.v-textfield[1]` to password
3. Dispatch input/change events
4. Click `.v-button` with text containing "Вход"
5. Wait 15 seconds

### Step 2: Select Terminal
1. Click `.v-filterselect` (terminal dropdown)
2. Wait 2 seconds
3. Find and click menu item containing "Терминал Врангель"
4. Wait 10 seconds

### Step 3: Navigate to Report
1. Click at coordinates (200, 570) — "Дополнительные услуги" arrow
2. Wait 3 seconds
3. Click at coordinates (150, 700) — "Отчетность по обработке груза"
4. Wait 10 seconds for report list to load

### Step 4: Open Report #13
1. Single-click (NOT double-click) on row containing "13. Движение по импорту"
2. Wait 5 seconds for dialog to open

### Step 5: Set Dates
1. Find `.v-datefield-textfield` inputs (first = start, second = end)
2. Set values directly via JavaScript
3. Dispatch input/change events
4. Wait 2 seconds

### Step 6: Generate Report
1. Find `.v-button` with text containing "ПОКАЗАТЬ"
2. Dispatch MouseEvent('click') with bubbles/cancelable
3. Wait 15 seconds for report to generate

### Step 7: Extract Data
1. Take screenshot of the generated report
2. Read screenshot and extract all data fields
3. Create Excel file using openpyxl with identical structure

## Report Structure

Columns (in order):
1. № (номер по порядку)
2. Контейнер (номер контейнера)
3. ISO тип (22G1, 45G1, etc.)
4. Размер (DC 20, HC 40, etc.)
5. Высотность (DC, HC)
6. Вес брутто
7. Вес нетто
8. Вес тары
9. Трафарет (вес макс.)
10. Порожний (Да/пусто)
11. Пломбы
12. № коносамента
13. Порожний как груз (БН/пусто)
14. Дата коносамента
15. Наименование груза
16. Грузоотправитель

## Excel Output

- Sheet name: "Движение по импорту"
- Title rows with merged cells
- Header row with blue background (#D9E1F2)
- Alternating row colors
- Proper column widths
- All data centered and wrapped

## Known Limitations

- **Export button does NOT work via automation** — screenshot + manual Excel creation is required
- Vaadin 7 ignores synthetic click events; use MouseEvent with bubbles/cancelable
- Date validation may show red exclamation marks but report still generates
- Menu coordinates are fixed for 1280x1024 viewport

## Usage

```
User: "Отчёт 13 за 10.06.2026-20.06.2026"
→ Use this skill → Generate Excel file → Send to user
```
