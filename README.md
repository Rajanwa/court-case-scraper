# Court Case Search Automation

A Python GUI application for automating case searches on the Faridabad District Court website using Selenium WebDriver and Tkinter.

## Features

- **Automated Court Selection**: Pre-configured for District Court, Faridabad
- **Case Search**: Search by case type, number, and year
- **CAPTCHA Handling**: Visual CAPTCHA display and manual entry
- **Headless Browser**: Runs Chrome in headless mode for better performance
- **PDF Generation**: Automatically save case details as PDF
- **User-Friendly GUI**: Simple Tkinter interface with status logging

## Prerequisites

### Required Software
- Python 3.7 or higher
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version)

### Python Dependencies
```bash
pip install selenium
pip install pillow
pip install requests
pip install tkinter  # Usually comes with Python
```

## Installation

1. **Clone or download the script**
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Download ChromeDriver**:
   - Visit [ChromeDriver Downloads](https://chromedriver.chromium.org/)
   - Download the version matching your Chrome browser
   - Add ChromeDriver to your system PATH or place it in the script directory

## Environment Variables (Optional)

You can set the following environment variables for customization:

```bash
# Chrome driver path (if not in PATH)
CHROME_DRIVER_PATH=/path/to/chromedriver

# PDF save location (default: C:\Users\Lenovo\OneDrive\Desktop\Rajan\Project assignment\case_details.pdf)
PDF_SAVE_PATH=/path/to/save/case_details.pdf

# Browser timeout (default: 20 seconds)
BROWSER_TIMEOUT=30
```

## Usage

### Starting the Application
```bash
python court_case_search.py
```

### Step-by-Step Process

1. **Initialize Browser**:
   - Click "🔄 Refresh" to initialize the headless Chrome browser
   - The application will navigate to the Faridabad District Court website
   - Court complex is automatically set to "District Court, Faridabad"

2. **Fill Case Details**:
   - **Case Type**: Select from the dropdown (e.g., "CS", "CRM", "APP", etc.)
   - **Case Number**: Enter the case registration number
   - **Case Year**: Enter the year of case registration

3. **Handle CAPTCHA**:
   - CAPTCHA image will be displayed automatically
   - Enter the CAPTCHA text in the input field
   - If CAPTCHA is unclear, click "🔄 Refresh" to reload

4. **Search Case**:
   - Click "Search Case" to submit the search
   - Wait for results to load (status will be shown)

5. **View Details**:
   - Click "View Details" to open case information
   - The application will automatically find and click the view button

6. **Generate PDF**:
   - Click "Generate PDF" to save case details as PDF
   - PDF will be saved to the configured location
   - Application will automatically close after PDF generation

## Court Case Types

The application supports all case types available on the Faridabad District Court website:

| Code | Case Type | Description |
|------|-----------|-------------|
| CS | Civil Suit | Civil cases |
| CRM | Criminal Misc | Criminal miscellaneous cases |
| APP | Appeal | Appeal cases |
| CMA | Civil Misc Appeal | Civil miscellaneous appeals |
| BA | Bail Application | Bail applications |
| And many more... | | See dropdown for complete list |

## CAPTCHA Strategy

The application implements several strategies for CAPTCHA handling:

1. **Image Enhancement**: Converts to grayscale and increases contrast
2. **Quality Improvement**: Resizes with anti-aliasing for better visibility
3. **Session Management**: Maintains browser session cookies for CAPTCHA requests
4. **Manual Entry**: User inputs CAPTCHA text manually
5. **Refresh Option**: Easy refresh if CAPTCHA is unclear

## File Structure

```
court_case_search/
├── court_case_search.py    # Main application file
├── README.md              # This file
├── requirements.txt       # Python dependencies
└── case_details.pdf       # Generated PDF (after search)
```

## Configuration

### Default Settings
- **Court Complex**: District Court, Faridabad (HRFB01,HRFB02,HRFB03)
- **Browser**: Chrome Headless Mode
- **PDF Location**: `C:\Users\Lenovo\OneDrive\Desktop\Rajan\Project assignment\case_details.pdf`
- **Window Size**: 1920x1080 (headless)

### Browser Options
The application runs Chrome with the following options:
- Headless mode for better performance
- Disabled automation detection
- Optimized for court website compatibility

## Troubleshooting

### Common Issues

1. **Browser Initialization Failed**:
   - Ensure ChromeDriver is installed and in PATH
   - Check Chrome browser version compatibility
   - Verify internet connection

2. **CAPTCHA Not Loading**:
   - Click "🔄 Refresh" to reload
   - Check if website is accessible
   - Verify browser session is active

3. **Search Not Working**:
   - Verify all fields are filled correctly
   - Check CAPTCHA is entered accurately
   - Ensure case details exist in the system

4. **PDF Generation Failed**:
   - Check file path permissions
   - Ensure target directory exists
   - Verify case details page is loaded

### Error Messages
- **"Please refresh to initialize browser first"**: Click refresh button
- **"Please select a case type"**: Choose a case type from dropdown
- **"Please enter captcha"**: Fill in the CAPTCHA field
- **"No case details available"**: Case not found or search failed

## Security Notes

- Application runs in headless mode for privacy
- No user credentials are stored
- Browser session is cleaned up on exit
- CAPTCHA is handled locally without external services

## Technical Details

### Dependencies
- **selenium**: Web automation framework
- **tkinter**: GUI framework (built-in with Python)
- **PIL (Pillow)**: Image processing for CAPTCHA display
- **requests**: HTTP requests for CAPTCHA images
- **base64**: Image encoding/decoding

### Browser Automation
- Uses Chrome WebDriver in headless mode
- Implements explicit waits for element loading
- Handles dynamic content and AJAX requests
- Maintains session cookies for CAPTCHA handling

## Support

For technical issues or questions:
1. Check the status log in the application
2. Verify all prerequisites are installed
3. Ensure stable internet connection
4. Check ChromeDriver version compatibility

## License

This tool is for educational and legitimate case lookup purposes only. Users must comply with the court website's terms of service and applicable laws.
