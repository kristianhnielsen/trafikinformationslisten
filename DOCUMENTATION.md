# Trafikinformationslisten - Project Documentation

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Project Structure](#project-structure)
6. [Architecture](#architecture)
7. [Module Documentation](#module-documentation)
8. [API Reference](#api-reference)
9. [Report Generation](#report-generation)
10. [Output Structure](#output-structure)
11. [Scheduling](#scheduling)
12. [Known Issues](#known-issues)
13. [Troubleshooting](#troubleshooting)
14. [Future Improvements](#future-improvements)

---

## Overview

**Trafikinformationslisten** is an automated Danish traffic information reporting system that fetches road work and traffic data from the Vejle Kommune (Vejle Municipality) Geographic Information System (GIS) API and generates professional Word documents with weekly and monthly traffic reports.

### Key Features

- **Automated Report Generation**: Automatically generates weekly and monthly traffic reports in Danish
- **GIS Data Integration**: Queries live traffic roadwork data from the Vejle Kommune GIS API
- **Professional Document Output**: Creates formatted Word documents (.docx) with structured traffic information
- **Smart Scheduling**: Automatically determines whether to generate weekly, monthly, or both reports based on the current date
- **Data Processing**: Cleans, formats, and sorts traffic data for professional presentation
- **Template-Based**: Uses Word document templates for consistent, customizable report formatting

### Target Users

- Vejle Kommune traffic management staff
- Municipal planners and engineers
- Public information officers
- Anyone needing automated traffic roadwork reporting

---

## Quick Start

### Prerequisites

- Python 3.11 or higher
- `pip` or `uv` package manager
- Internet access to GIS API
- Output folder path accessible on the system

### 5-Minute Setup

1. **Clone or download the project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   # or with uv
   uv sync
   ```

3. **Create `.env` file** in the project root:
   ```
   OUTPUT_FOLDER=C:/path/to/output/folder
   ```

4. **Ensure template exists**: Verify `trafik_info_template.docx` is in the project root

5. **Run the script**:
   ```bash
   python main.py
   ```

6. **Check output**: Generated reports appear in `{OUTPUT_FOLDER}/{year}/`

---

## Installation

### System Requirements

- **OS**: Windows, macOS, or Linux
- **Python Version**: 3.11 or higher
- **Disk Space**: ~100MB for dependencies + space for generated reports

### Step-by-Step Installation

#### Using `uv` (Recommended - Faster)

```bash
# Install uv if not already installed
pip install uv

# Navigate to project directory
cd trafikinformationslisten

# Install dependencies
uv sync
```

#### Using `pip` (Standard Method)

```bash
# Navigate to project directory
cd trafikinformationslisten

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Verify Installation

```bash
python -c "import requests, pandas, docxtpl; print('All dependencies installed successfully!')"
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root directory with the following variable:

```env
OUTPUT_FOLDER=C:/path/to/your/reports/folder
```

#### Configuration Options

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `OUTPUT_FOLDER` | Yes | Base directory where reports are saved. The script creates subdirectories by year automatically. | `C:/Reports/TrafficInfo` or `/home/user/reports/` |

### `.env` File Template

Create an `.env` file by copying this template:

```bash
# Traffic Information Reports Output Directory
# This folder will contain subfolders per year (e.g., 2026/)
# The script creates the directory structure automatically if it doesn't exist
OUTPUT_FOLDER=C:\Users\YourUsername\Documents\TrafficReports
```

### Important Notes

- **Windows paths**: Use either forward slashes `/` or double backslashes `\\` in `.env` file
- **Folder Creation**: The script automatically creates the output folder and year subfolder if they don't exist
- **Permissions**: Ensure the process running this script has write permissions to the `OUTPUT_FOLDER`
- **Security**: Never commit `.env` file to version control (it's already in `.gitignore`)

---

## Project Structure

```
trafikinformationslisten/
│
├── main.py                          # Entry point - orchestrates weekly/monthly reports
├── trafik_info.py                   # Core module - all business logic and functions
├── trafik_info_template.docx        # Word document template for report rendering
│
├── pyproject.toml                   # Project metadata and dependencies
├── requirements.txt                 # Package requirements for pip/uv
├── README.md                        # Quick start guide
├── DOCUMENTATION.md                 # This file - comprehensive documentation
│
├── .env                             # Environment variables (not in version control)
├── .venv/                           # Virtual environment (if created locally)
│
└── output/                          # Generated reports (example, actual path from .env)
    └── 2026/
        ├── TRAFIK-INFO - UGE 11 2026.docx
        └── TRAFIK-INFO - MÅNED marts 2026.docx
```

### File Descriptions

| File | Purpose |
|------|---------|
| `main.py` | Entry point that checks the current date and orchestrates execution of `weekly_report()` and conditional `monthly_report()` |
| `trafik_info.py` | Core module containing all functions for data retrieval, processing, formatting, and report generation |
| `trafik_info_template.docx` | Word document template with placeholders for dynamic content insertion via `docxtpl` |
| `pyproject.toml` | Project metadata (name, version, Python version) and actual dependency specifications |
| `requirements.txt` | Simplified package list for `pip`/`uv` installation (derives from `pyproject.toml`) |
| `.env` | Environment configuration file (not tracked in Git) - contains `OUTPUT_FOLDER` path |

---

## Architecture

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     main.py (Entry Point)                   │
│  - Checks current date                                      │
│  - Calls weekly_report()                                    │
│  - Calls monthly_report() if day <= 7                       │
└────────────┬────────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────┐
│              trafik_info.py (Core Logic)                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ weekly_report() / monthly_report()                  │   │
│  │ - Define GIS query parameters                       │   │
│  │ - Call get_report()                                 │   │
│  └────────────┬────────────────────────────────────────┘   │
│               │                                             │
│               ↓                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ get_report(filename, query_params)                  │   │
│  │ - Calls get_data() to fetch from API                │   │
│  │ - Calls format_data() to process data               │   │
│  │ - Loads Word template                               │   │
│  │ - Renders and saves document                        │   │
│  └────────────┬────────────────────────────────────────┘   │
│               │                                             │
│   ┌───────────┴──────────────┬──────────────┐              │
│   ↓                          ↓              ↓              │
│ get_data()           format_data()   get_file_output_path() │
│ - Calls GIS API      - Clean text    - Load .env           │
│ - Returns JSON       - Rename cols   - Create folders      │
│ - Extractfeatures    - Sort data     - Return file path    │
│                      - Calculate     - Local_logs module   │
│                        durations       (update_log)        │
└─────────────────────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────┐
│  Vejle Kommune GIS API                                      │
│  https://kortservice.vejle.dk/gis/...                       │
│    Returns: GeoJSON with roadwork features                  │
└─────────────────────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────┐
│  Generated Word Documents (.docx files)                     │
│  Saved to: {OUTPUT_FOLDER}/{year}/                          │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **HTTP Client** | `requests` | Fetch data from GIS API |
| **Data Processing** | `pandas` | Manipulate and format road work data |
| **Document Generation** | `docxtpl` + `python-docx` | Create and render Word documents |
| **Environment Config** | `python-dotenv` | Load `.env` configuration variables |
| **Language** | Python 3.11+ | Core programming language |

---

## Module Documentation

### main.py

**Purpose**: Entry point that orchestrates the report generation process.

**Behavior**:
- Always runs `weekly_report()` to generate the current week's traffic report
- Checks if the current day of month is between 1-7
- If true, also runs `monthly_report()` for the current month's traffic report

**Code Structure**:

```python
import datetime
from trafik_info import weekly_report, monthly_report

if __name__ == "__main__":
    # Run the weekly report
    weekly_report()
    
    if datetime.datetime.today().day <= 7:
        # Run the monthly report (first week of month only)
        monthly_report()
```

**Key Points**:
- Simple orchestration - all logic is in `trafik_info.py`
- Date checking ensures monthly reports are generated once per month
- Both reports can run in succession without issues

---

### trafik_info.py

**Purpose**: Core module containing all business logic for data retrieval, processing, and report generation.

#### Function: `weekly_report()`

Generates a weekly traffic roadwork report showing work starting within the next 10 days.

**Parameters**: None

**Returns**: None (saves `.docx` file to disk)

**Process**:
1. Gets current date and calculates next week number
2. Queries GIS API for roadwork with `traficstatus = 'Trafikudmeldt'` and `dagetilstart <= 10`
3. Generates report with filename: `TRAFIK-INFO - UGE {week_number} {year}.docx`
4. Logs success or catches exceptions

**GIS Query Parameters**:
| Parameter | Value | Purpose |
|-----------|-------|---------|
| `where` | `traficstatus = 'Trafikudmeldt' and dagetilstart <= 10` | Filter for announced traffic and work starting in next 10 days |
| `returnGeometry` | `true` | Include geographic data |
| `outSR` | `25832` | Output spatial reference (ETRS89 UTM Zone 32N) |
| `f` | `geojson` | Return format |
| `outFields` | `*` | Return all fields |
| `orderByFields` | `startdate` | Sort by start date |

**Example Output Filename**: `TRAFIK-INFO - UGE 11 2026.docx`

**Error Handling**: Wraps execution in try-except block, logs errors via `update_log()`

#### Function: `monthly_report()`

Generates a monthly traffic roadwork report showing work starting within the current month (32 days).

**Parameters**: None

**Returns**: None (saves `.docx` file to disk)

**Process**:
1. Gets current date and month name in Danish
2. Queries GIS API for roadwork with `traficstatus = 'Trafikudmeldt'` and `dagetilstart <= 32`
3. Generates report with filename: `TRAFIK-INFO - MÅNED {month_name} {year}.docx`
4. Logs success or catches exceptions

**GIS Query Parameters**:
| Parameter | Value | Purpose |
|-----------|-------|---------|
| `where` | `traficstatus = 'Trafikudmeldt' and dagetilstart <= 32` | Filter for announced traffic and work starting in current month |
| `returnGeometry` | `true` | Include geographic data |
| `outSR` | `25832` | Output spatial reference |
| `f` | `geojson` | Return format |
| `outFields` | `*` | Return all fields |
| `orderByFields` | `startdate` | Sort by start date |

**Example Output Filename**: `TRAFIK-INFO - MÅNED marts 2026.docx`

**Danish Month Names**: januar, februar, marts, april, maj, juni, juli, august, september, oktober, november, december

**Error Handling**: Wraps execution in try-except block, logs errors via `update_log()`

#### Function: `get_report(output_filename: str, query_params: dict[str, Any])`

Core function that fetches data, formats it, and generates the Word document.

**Parameters**:
- `output_filename` (str): Name of the output file (e.g., `TRAFIK-INFO - UGE 11 2026.docx`)
- `query_params` (dict): GIS API query parameters including filters, fields, and format specifications

**Returns**: None (saves `.docx` file to disk and updates log)

**Process**:
1. Gets date data (today's date, formatted date, next week number)
2. Determines output file path using `get_file_output_path()`
3. Fetches raw data from GIS API via `get_data(query_params)`
4. Creates pandas DataFrame from API response
5. Formats data using `format_data(df)`
6. Removes duplicate records based on `case_id` and `source`
7. Loads `trafik_info_template.docx` as a template
8. Converts DataFrame to list of dictionaries (records)
9. Renders template with context containing:
   - `roadwork`: List of road work records
   - `today_date`: Formatted today's date (DD-MM-YYYY)
   - `current_year`: Current year
   - `week_number`: Next week number
   - `document_type`: Either `UGE {week_number}` or `MÅNED {month_name}`
10. Saves rendered document to output path

#### Function: `get_data(params: dict[str, Any])`

Fetches traffic roadwork data from the Vejle Kommune GIS API.

**Parameters**:
- `params` (dict): Query parameters for the API request (where clause, fields, format, etc.)

**Returns**: list of dicts - Properties of each road work feature from the API

**API Endpoint**: 
```
https://kortservice.vejle.dk/gis/rest/services/SEPTIMA/vej_sw/MapServer/23/query
```

**Process**:
1. Makes HTTP GET request to GIS API with provided parameters
2. Parses JSON response
3. Extracts `properties` from each feature in the GeoJSON response
4. Returns list of property dictionaries

**Example Property Fields**:
- `name`: Contractor company name
- `oov2roadinfo`: Road work title/description
- `oov2roaduserdescription`: Detailed user-facing description
- `contractorcontactperson`: Contact person name
- `contractormobile`: Contractor phone number
- `ownermailaddress`: Contractor email
- `startdate`: Start date (DD-MM-YYYY)
- `enddate`: End date (DD-MM-YYYY)
- `oov2roadmarkstart`: Start time (HH:MM)
- `oov2roadmarkend`: End time (HH:MM)
- `serialnumber`: Unique case ID
- `modulename`: Source module name

#### Function: `format_data(df: pd.DataFrame)`

Cleans, processes, and reformats the DataFrame for Word document template rendering.

**Parameters**:
- `df` (pd.DataFrame): DataFrame with raw GIS API data

**Returns**: None (modifies DataFrame in-place)

**Processing Steps**:

1. **XML Escape & Strip**: Replace `&` with `&amp;` in all text columns and remove whitespace
2. **Extract Road Info**: Create `road_info` column from `oov2roaduserdescription`
3. **Rename Columns**: Standardize column names to match template placeholders:
   - `oov2roadinfo` → `title`
   - `contractorcontactperson` → `contractor_contact_person`
   - `contractormobile` → `contractor_phone`
   - `ownermailaddress` → `contractor_email`
   - `name` → `contractor_company`
   - `oov2roadmarkstart` → `starttime`
   - `oov2roadmarkend` → `endtime`
   - `serialnumber` → `case_id`
   - `modulename` → `source`

4. **Convert & Sort Dates**:
   - Convert `startdate` and `enddate` to datetime objects
   - Sort by `startdate` and `starttime` in descending (newest first) order
   - Convert dates back to string format (DD-MM-YYYY)

5. **Calculate Duration**: Create human-readable `duration` field:
   - If start and end dates are same: `"{date} fra kl. {start_time} til kl. {end_time}"` (Danish: "from {time} to {time}")
   - Otherwise: `"fra {start_date} til {end_date}"` (Danish: "from {start_date} to {end_date}")

6. **Capitalize Names**: Capitalize each word in `contractor_contact_person` for professional presentation

#### Function: `get_file_output_path(filename: str) -> str`

Determines the full file path for saving the report.

**Parameters**:
- `filename` (str): Desired filename (e.g., `TRAFIK-INFO - UGE 11 2026.docx`)

**Returns**: str - Full file path to save the file

**Process**:
1. Loads environment variables from `.env` file
2. Gets today's date and extracts year
3. Reads `OUTPUT_FOLDER` from environment (empty string if not set)
4. Creates path: `{OUTPUT_FOLDER}/{year}/{filename}`
5. Creates directories if they don't exist
6. Returns full output path

**Example Return Value**: `C:\Reports\TrafficInfo\2026\TRAFIK-INFO - UGE 11 2026.docx`

#### Function: `get_dt_data() -> tuple[date, str, int]`

Helper function that provides current date information.

**Parameters**: None

**Returns**: Tuple containing:
- `today_date` (datetime.date): Today's date object
- `today_date_text` (str): Today's date formatted as DD-MM-YYYY
- `next_week_number` (int): ISO week number starting next week

**Example Return**:
```python
(datetime.date(2026, 3, 12), "12-03-2026", 12)
```

#### Function: `get_dk_month_name(month_number: int) -> str`

Converts month number to Danish month name.

**Parameters**:
- `month_number` (int): Month number (1-12)

**Returns**: str - Danish month name in lowercase

**Month Mapping**:
| Number | Danish Name |
|--------|-------------|
| 1 | januar |
| 2 | februar |
| 3 | marts |
| 4 | april |
| 5 | maj |
| 6 | juni |
| 7 | juli |
| 8 | august |
| 9 | september |
| 10 | oktober |
| 11 | november |
| 12 | december |

**Example**: `get_dk_month_name(3)` returns `"marts"`

---

## API Reference

### Vejle Kommune GIS API

#### Endpoint

```
https://kortservice.vejle.dk/gis/rest/services/SEPTIMA/vej_sw/MapServer/23/query
```

#### Request Method

`GET` via HTTP

#### Query Parameters for Weekly Report

```python
{
    "returnGeometry": "true",
    "outSR": "25832",
    "f": "geojson",
    "outFields": "*",
    "where": "traficstatus = 'Trafikudmeldt' and dagetilstart <= 10",
    "orderByFields": "startdate",
}
```

#### Query Parameters for Monthly Report

```python
{
    "returnGeometry": "true",
    "outSR": "25832",
    "f": "geojson",
    "outFields": "*",
    "where": "traficstatus = 'Trafikudmeldt' and dagetilstart <= 32",
    "orderByFields": "startdate",
}
```

#### Response Format

GeoJSON FeatureCollection with the following structure:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": { ... },
      "properties": {
        "serialnumber": "12345",
        "name": "Contractor Company",
        "oov2roadinfo": "Road Work Title",
        "oov2roaduserdescription": "Detailed description",
        "contractorcontactperson": "John Doe",
        "contractormobile": "20 30 40 50",
        "ownermailaddress": "john@contractor.dk",
        "startdate": "12-03-2026",
        "enddate": "15-03-2026",
        "oov2roadmarkstart": "08:00",
        "oov2roadmarkend": "16:00",
        "modulename": "vej_sw",
        "traficstatus": "Trafikudmeldt",
        "dagetilstart": 5
      }
    }
  ]
}
```

#### Parameter Explanations

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `returnGeometry` | `true` | Include geographic geometry in response |
| `outSR` | `25832` | Output Spatial Reference: ETRS89/UTM Zone 32N (Danish standard) |
| `f` | `geojson` | Response format: GeoJSON |
| `outFields` | `*` | Return all available fields |
| `where` | SQL-like filter clause | Filter results by status and days until start |
| `orderByFields` | `startdate` | Sort results by start date |

#### Filter Clause Explanation

**`traficstatus = 'Trafikudmeldt'`**:
- Filters for "announced traffic" status only
- `Trafikudmeldt` means the roadwork has been officially announced

**`dagetilstart <= 10`** (weekly) / **`<= 32`** (monthly):
- Returns roadwork where the start date is within the specified number of days
- Weekly: Work starting in the next 10 days
- Monthly: Work starting in the next 32 days (approximately 1 month)

---

## Report Generation

### Generation Process

```
1. Determine Report Type
   └─> Check date and report type needed
   
2. Define Query Parameters
   └─> Set GIS API filters for data scope
   
3. Fetch Data from GIS API
   └─> Make HTTP request and retrieve GeoJSON data
   
4. Create DataFrame
   └─> Convert API response to pandas DataFrame
   
5. Format Data
   └─> Clean text, rename columns, sort, calculate durations
   
6. Deduplicate
   └─> Remove duplicate entries by case_id and source
   
7. Load Word Template
   └─> Read trafik_info_template.docx
   
8. Prepare Context
   └─> Create dictionary with roadwork records and metadata
   
9. Render Template
   └─> Sub in data and generate Word document
   
10. Save to Disk
    └─> Write .docx file to OUTPUT_FOLDER/{year}/
    
11. Log Result
    └─> Record success/error via update_log()
```

### Weekly Report Details

**When Generated**: Every time `main.py` runs (usually daily)

**Scope**: Road work announcements starting in the next 10 days

**Filename Format**: `TRAFIK-INFO - UGE {week_number} {year}.docx`

**Example**: `TRAFIK-INFO - UGE 11 2026.docx`

**Content Sorting**: Newest first (descending by start date and time)

**Overwrite Behavior**: If the same week number is run again in the same day, it overwrites the previous file

### Monthly Report Details

**When Generated**: Only during the first 7 days of each month (via `main.py` date check)

**Scope**: Road work announcements starting in the next 32 days (approximately the current month)

**Filename Format**: `TRAFIK-INFO - MÅNED {danish_month_name} {year}.docx`

**Example**: `TRAFIK-INFO - MÅNED marts 2026.docx`

**Content Sorting**: Newest first (descending by start date and time)

**Overwrite Behavior**: Generated only once per month; subsequent runs in the same month skip this

### Word Template for customization

**Template File**: `trafik_info_template.docx`

**Location**: Project root directory

**Templating Engine**: `docxtpl` (Jinja2-style templating for Word documents)

**Available Variables**:
- `roadwork`: List of road work records (can be iterated with `{% for %}`...`{% endfor %}`)
- `today_date`: Today's date (DD-MM-YYYY format)
- `current_year`: Current year (YYYY format)
- `week_number`: Next week number (integer, 1-53)
- `document_type`: Either `"UGE {week_number}"` or `"MÅNED {month_name}"`

**Record Fields** (inside `roadwork` loop):
- `title`, `contractor_company`, `contractor_contact_person`, `contractor_phone`, `contractor_email`
- `startdate`, `enddate`, `duration`
- `starttime`, `endtime`, `case_id`, `source`
- `road_info`

**Template Customization**: Modify the template using Microsoft Word while maintaining template variables (in `{{ }}` brackets)

---

## Output Structure

### Directory Layout

```
OUTPUT_FOLDER/                                   (set in .env)
├── 2025/
│   ├── TRAFIK-INFO - UGE 43 2025.docx
│   ├── TRAFIK-INFO - UGE 44 2025.docx
│   └── TRAFIK-INFO - MÅNED december 2025.docx
│
├── 2026/
│   ├── TRAFIK-INFO - UGE 10 2026.docx
│   ├── TRAFIK-INFO - UGE 11 2026.docx
│   └── TRAFIK-INFO - MÅNED marts 2026.docx
│
└── 2027/
    └── TRAFIK-INFO - UGE 1 2027.docx
```

### Filename Convention

**Weekly Report**: `TRAFIK-INFO - UGE {week_number} {year}.docx`
- Example: `TRAFIK-INFO - UGE 11 2026.docx`

**Monthly Report**: `TRAFIK-INFO - MÅNED {month_name} {year}.docx`
- Example: `TRAFIK-INFO - MÅNED marts 2026.docx`

### File Path Example

```
C:\Users\Traffic\Reports\2026\TRAFIK-INFO - UGE 11 2026.docx
                          ^^^^

(year automatically inserted into directory structure)
```

### Document Content Structure

Each generated Word document contains:

1. **Document Header**: 
   - Document type (`UGE 11` or `MÅNED marts`)
   - Current year
   - Generation date

2. **Road Work Table/List**:
   - Sorted by start date (newest first)
   - Deduplicated by case ID and source
   - For each road work entry:
     - Title (road work description)
     - Duration (formatted period with times if same day)
     - Contractor company name
     - Contact person name
     - Contact phone number
     - Contact email
     - Road information
     - Case ID
     - Source

3. **Data Cleaning Applied**:
   - Special character escaping (`&` → `&amp;`)
   - Text trimming (no extra whitespace)
   - Proper name capitalization (contractor contact person)
   - Consistent date formatting (DD-MM-YYYY)

---

## Known Issues

### 1. Missing `local_logs` Module

**Issue**: The script imports `from local_logs import update_log` but this module doesn't exist in the project.

**Impact**: The script will crash when trying to call `update_log()` during report generation.

**Error Message**:
```
ModuleNotFoundError: No module named 'local_logs'
```

**Workaround**: 

Create a `local_logs.py` file in the project root:

```python
# local_logs.py
import datetime

def update_log(message: str) -> None:
    """
    Log a message with timestamp.
    
    Args:
        message: The message to log
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    
    # Optional: Write to file
    # with open("traffic_reports.log", "a") as log_file:
    #     log_file.write(f"[{timestamp}] {message}\n")
```

**Solution Status**: ⏳ Pending - see [Future Improvements](#future-improvements)

### 2. Incomplete `requirements.txt`

**Issue**: `requirements.txt` contains only basic Python distributions (`numpy`, `pip`, `uv`) and doesn't include actual project dependencies.

**Impact**: Installation via `pip install -r requirements.txt` won't install required packages (`requests`, `pandas`, `docxtpl`, `python-docx`, `python-dotenv`).

**Current workaround**: Use `pyproject.toml` dependencies which are correct:
```bash
pip install docxtpl pandas python-docx python-dotenv requests
```

**Solution Status**: ⏳ Pending - `requirements.txt` should be regenerated from `pyproject.toml`

### 3. Missing `.env` File

**Issue**: The `.env` file is not included in the repository (correctly, for security reasons), so users must create it manually.

**Impact**: If `.env` is missing, `OUTPUT_FOLDER` will be empty (default value) and reports might fail to save or save to unexpected locations.

**Error Signs**: Reports not found in expected output folder

**Workaround**: Create `.env` file with:
```
OUTPUT_FOLDER=C:/your/path/here
```

---

## Troubleshooting

### Report File Not Generated

**Symptoms**: Script runs but no `.docx` file appears in output folder

**Possible Causes**:

1. **Incorrect `OUTPUT_FOLDER`** in `.env`
   - Check: Is the path correct and accessibility?
   - Fix: Update `.env` with valid, writable path
   - Test: Create a test file manually in that folder

2. **Missing permissions** on output directory
   - Check: Can your user write to the folder?
   - Fix: Update folder permissions (right-click → Properties → Security)

3. **Network issue** - API unreachable
   - Check: Can you ping `kortservice.vejle.dk`?
   - Fix: Check internet connection, firewall, proxy settings

4. **API returns no data**
   - Check: Are there any active road works to report?
   - Check: Is the GIS API working? Try: `https://kortservice.vejle.dk/gis/rest/services/SEPTIMA/vej_sw/MapServer/23/query?f=json`

5. **`local_logs` module missing** (see Known Issues)
   - Fix: Create `local_logs.py` as described above

### Script Crashes with Error

**ModuleNotFoundError: No module named 'X'**

1. Verify dependencies are installed:
   ```bash
   pip list
   ```

2. Reinstall missing packages:
   ```bash
   pip install requests pandas docxtpl python-docx python-dotenv
   ```

3. Activate virtual environment (if using one):
   ```bash
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

**FileNotFoundError: trafik_info_template.docx**

- Verify template exists in project root
- Check filename spelling (case-sensitive on Linux/Mac)

**PermissionError: Access denied**

- Check that output folder path is correct
- Ensure you have write permissions
- Close any open `.docx` files from previous report runs

### API/Network Issues

**Connection timeout**

```python
# The script may hang on the requests.get() call
# To add timeout, you could modify get_data():
# response = requests.get(url, params=params, timeout=10)
```

**SSL/Certificate errors**

- Install certificate updates: `pip install --upgrade certifi`
- Check company proxy/firewall settings

### Date/Time Issues

**Wrong week number in report**

- Verify system date is correct
- Remember: Week numbers follow ISO 8601 standard (may differ from other systems)


---

**Last Updated**: March 2026  
**Project Version**: 0.1.0  
**Documentation Version**: 1.0
