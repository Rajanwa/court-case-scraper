import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
from datetime import datetime
import base64
import requests
from PIL import Image, ImageTk
from io import BytesIO

class CourtCaseSearchAutomation:
    def __init__(self, root):
        self.root = root
        self.root.title("Court Case Search Automation - Faridabad District Court")
        self.root.geometry("600x800")
        self.root.resizable(True, True)
        
        # Browser instance
        self.driver = None
        self.wait = None
        self.current_case_window = None
        self.captcha_photo = None
        self.browser_initialized = False
        self.view_buttons = None
        
        # Case type options
        self.case_types = {
            "": "--Select--",
            "61": "446 CR. P.C",
            "3": "APP",
            "13": "ARB",
            "25": "BA",
            "1": "CA",
            "37": "CHA",
            "36": "CHI",
            "2": "CMA",
            "18": "CM APPLI",
            "39": "COMA",
            "38": "COMI",
            "69": "COMMERCIAL APPEAL",
            "68": "COMMERCIAL SUIT",
            "64": "CP",
            "49": "CR",
            "35": "CRA",
            "24": "CRM",
            "40": "CRMP",
            "33": "CRR",
            "4": "CS",
            "11": "CS37",
            "31": "DMC",
            "29": "ELC",
            "48": "EP",
            "12": "EXE",
            "8": "FD",
            "9": "GW",
            "67": "HAMA",
            "58": "HDRA",
            "46": "HMA",
            "57": "HMCA",
            "15": "INDIG",
            "16": "INDIGA",
            "21": "INSO",
            "60": "IT ACT",
            "23": "JJB",
            "14": "LAC",
            "62": "LAC EXE",
            "63": "LAC MISC",
            "44": "MACM",
            "66": "MACM- FORM1",
            "43": "MACP",
            "51": "MHA",
            "26": "MNT125",
            "19": "MPL",
            "20": "MPLA",
            "56": "NACT",
            "27": "NDPS",
            "53": "OBJ",
            "28": "PC",
            "22": "PFA",
            "50": "PFC",
            "65": "PP",
            "32": "PRI",
            "17": "PROB",
            "6": "RA",
            "47": "REMP",
            "10": "REW APP",
            "5": "RP",
            "34": "SC",
            "7": "SUCC",
            "41": "SUMM",
            "45": "TA",
            "55": "TELA ACT",
            "59": "TELE ACT",
            "52": "TRA",
            "54": "UCR",
            "30": "WKF"
        }
        
        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Court Case Search Automation",
                              font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Court Complex
        ttk.Label(main_frame, text="Court Complex:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.court_complex_var = tk.StringVar(value="District Court, Faridabad")
        court_complex_label = ttk.Label(main_frame, text="District Court, Faridabad",
                                      font=("Arial", 10, "bold"))
        court_complex_label.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Case Type Dropdown
        ttk.Label(main_frame, text="Case Type:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.case_type_var = tk.StringVar()
        case_type_combo = ttk.Combobox(main_frame, textvariable=self.case_type_var,
                                     values=list(self.case_types.values()),
                                     state="readonly", width=30)
        case_type_combo.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        case_type_combo.set("--Select--")
        
        # Case Number
        ttk.Label(main_frame, text="Case Number:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.case_number_var = tk.StringVar()
        case_number_entry = ttk.Entry(main_frame, textvariable=self.case_number_var, width=32)
        case_number_entry.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Case Year
        ttk.Label(main_frame, text="Case Year:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.case_year_var = tk.StringVar()
        case_year_entry = ttk.Entry(main_frame, textvariable=self.case_year_var, width=32)
        case_year_entry.grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Captcha section
        captcha_frame = ttk.LabelFrame(main_frame, text="Captcha", padding="10")
        captcha_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Captcha display frame
        captcha_display_frame = ttk.Frame(captcha_frame)
        captcha_display_frame.grid(row=0, column=0, columnspan=2, pady=5)
        
        # Captcha image display
        self.captcha_label = tk.Label(captcha_display_frame, 
                                    text="Click Refresh to initialize browser and load captcha",
                                    background="lightgray", width=30, height=8,
                                    relief="sunken", borderwidth=2)
        self.captcha_label.grid(row=0, column=0, pady=5)
        
        # Refresh captcha button
        refresh_btn = ttk.Button(captcha_display_frame, text="🔄 Refresh",
                               command=self.refresh_captcha)
        refresh_btn.grid(row=0, column=1, padx=(10, 0), sticky=tk.N)
        
        # Captcha input frame
        captcha_input_frame = ttk.Frame(captcha_frame)
        captcha_input_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Label(captcha_input_frame, text="Enter Captcha:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.captcha_var = tk.StringVar()
        captcha_entry = ttk.Entry(captcha_input_frame, textvariable=self.captcha_var, width=15)
        captcha_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Search button
        search_btn = ttk.Button(buttons_frame, text="Search Case",
                              command=self.search_case)
        search_btn.grid(row=0, column=0, padx=5)
        
        # View button
        self.view_btn = ttk.Button(buttons_frame, text="View Details",
                                 command=self.view_case_details,
                                 state=tk.DISABLED)
        self.view_btn.grid(row=0, column=1, padx=5)
        
        # Close Browser button
        close_btn = ttk.Button(buttons_frame, text="Close Browser",
                             command=self.close_browser)
        close_btn.grid(row=0, column=3, padx=5)
        
        # PDF Generation button
        pdf_frame = ttk.Frame(main_frame)
        pdf_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        self.pdf_button = ttk.Button(pdf_frame, text="Generate PDF",
                                   command=self.generate_pdf,
                                   state=tk.DISABLED)
        self.pdf_button.grid(row=0, column=0, padx=5)
        
        # Status text area
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="5")
        status_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.status_text = tk.Text(status_frame, height=10, width=70)
        scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(8, weight=1)
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)

    def log_status(self, message):
        """Add message to status text area"""
        if hasattr(self, 'status_text'):
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.status_text.see(tk.END)
            self.root.update()
        else:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {message}")
        
    def initialize_browser(self):
        """Initialize Chrome browser in headless mode"""
        try:
            self.log_status("Initializing Chrome browser in headless mode...")
            
            # Chrome options
            chrome_options = Options()
            
            # Always run in headless mode
            chrome_options.add_argument("--headless=new")  # New headless mode in Chrome 109+
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            
            # Initialize driver
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 20)
            
            # Navigate to the website
            self.driver.get("https://faridabad.dcourts.gov.in/case-status-search-by-case-number/")
            self.log_status("Browser initialized in headless mode and navigated to court website")
            
            # Set up the court complex
            self.setup_court_complex()
            
            self.browser_initialized = True
            return True
            
        except Exception as e:
            self.log_status(f"Error initializing browser: {str(e)}")
            messagebox.showerror("Error", f"Failed to initialize browser: {str(e)}")
            return False

    def setup_court_complex(self):
        """Set up the court complex selection"""
        try:
            # Wait for and select court complex
            court_select = self.wait.until(
                EC.presence_of_element_located((By.NAME, "est_code"))
            )
            select_obj = Select(court_select)
            select_obj.select_by_value("HRFB01,HRFB02,HRFB03")
            self.log_status("Court complex set to District Court, Faridabad")
            
        except Exception as e:
            self.log_status(f"Error setting up court complex: {str(e)}")

    def load_captcha(self):
        """Load and display captcha in tkinter"""
        if not self.driver:
            messagebox.showwarning("Warning", "Please initialize browser first")
            return False
            
        try:
            self.log_status("Loading captcha...")
            
            # Find captcha image
            captcha_img = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img[src*='captcha']"))
            )
            
            # Get captcha image source
            captcha_src = captcha_img.get_attribute("src")
            self.log_status("Captcha found, downloading image...")
            
            # Download and display captcha
            self.display_captcha_image(captcha_src)
            return True
            
        except Exception as e:
            self.log_status(f"Error loading captcha: {str(e)}")
            return False

    def display_captcha_image(self, captcha_src):
        """Download and display captcha image in tkinter with better quality"""
        try:
            # Handle different types of captcha sources
            if captcha_src.startswith('data:image'):
                # Base64 encoded image
                header, data = captcha_src.split(',', 1)
                image_data = base64.b64decode(data)
                image = Image.open(BytesIO(image_data))
            else:
                # URL-based image - use selenium to get cookies for session
                if captcha_src.startswith('/'):
                    # Relative URL
                    base_url = self.driver.current_url.split('/')[0:3]
                    captcha_src = '/'.join(base_url) + captcha_src
                
                # Get cookies from selenium session
                cookies = self.driver.get_cookies()
                session = requests.Session()
                for cookie in cookies:
                    session.cookies.set(cookie['name'], cookie['value'])
                
                response = session.get(captcha_src)
                response.raise_for_status()
                image = Image.open(BytesIO(response.content))
            
            # Enhance image quality and contrast
            image = image.convert('L')  # Convert to grayscale
            image = image.point(lambda x: 0 if x < 128 else 255)  # Increase contrast
            
            # Resize image while maintaining aspect ratio
            original_width, original_height = image.size
            max_width, max_height = 300, 100  # Increased size for better visibility
            
            # Calculate new dimensions
            ratio = min(max_width/original_width, max_height/original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            
            # Resize with anti-aliasing
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage for tkinter
            self.captcha_photo = ImageTk.PhotoImage(image)
            
            # Update the label with the image
            self.captcha_label.config(
                image=self.captcha_photo, 
                text="",
                width=max_width, 
                height=max_height
            )
            
            self.log_status("Captcha image loaded successfully")
            
        except Exception as e:
            self.log_status(f"Error displaying captcha image: {str(e)}")
            self.captcha_label.config(
                text=f"Failed to load captcha\n{str(e)}",
                width=300, 
                height=100
            )

    def refresh_captcha(self):
        """Refresh captcha - now also handles browser initialization"""
        try:
            # First check if browser needs to be initialized
            if not self.browser_initialized or not self.driver:
                if not self.initialize_browser():
                    return
            
            # Then load the captcha
            if not self.load_captcha():
                return
            
            # Clear any existing captcha text
            self.captcha_var.set("")
            
            self.log_status("Captcha refreshed")
            
            # Additional wait time for headless
            time.sleep(2)
            
        except Exception as e:
            self.log_status(f"Error refreshing captcha: {str(e)}")

    def search_case(self):
        """Perform case search"""
        if not self.driver or not self.browser_initialized:
            messagebox.showwarning("Warning", "Please refresh to initialize browser first")
            return
        
        # Validate inputs
        if not self.validate_inputs():
            return
        
        try:
            self.log_status("Starting case search...")
            
            # Get case type value
            case_type_text = self.case_type_var.get()
            case_type_value = ""
            for value, text in self.case_types.items():
                if text == case_type_text:
                    case_type_value = value
                    break
            
            # Fill case type
            case_type_select = self.driver.find_element(By.NAME, "case_type")
            select_obj = Select(case_type_select)
            select_obj.select_by_value(case_type_value)
            self.log_status(f"Case type set to: {case_type_text}")
            
            # Fill case number
            case_number_input = self.driver.find_element(By.NAME, "reg_no")
            case_number_input.clear()
            case_number_input.send_keys(self.case_number_var.get())
            self.log_status(f"Case number entered: {self.case_number_var.get()}")
            
            # Fill case year
            case_year_input = self.driver.find_element(By.NAME, "reg_year")
            case_year_input.clear()
            case_year_input.send_keys(self.case_year_var.get())
            self.log_status(f"Case year entered: {self.case_year_var.get()}")
            
            # Fill captcha
            captcha_input = self.driver.find_element(By.NAME, "siwp_captcha_value")
            captcha_input.clear()
            captcha_input.send_keys(self.captcha_var.get())
            self.log_status(f"Captcha entered: {self.captcha_var.get()}")
            
            # Submit search
            search_button = self.driver.find_element(By.CSS_SELECTOR, "input[value='Search']")
            search_button.click()
            
            self.log_status("Search submitted. Waiting for results...")
            
            # Longer wait time for headless mode
            time.sleep(5)
            
            # Clear captcha for next search
            self.captcha_var.set("")
            self.refresh_captcha()
            
            # Enable View button (user can click it if they want to view results)
            self.view_btn.config(state=tk.NORMAL)
            self.pdf_button.config(state=tk.NORMAL)
                
        except Exception as e:
            self.log_status(f"Error during search: {str(e)}")
            self.view_btn.config(state=tk.DISABLED)
            self.pdf_button.config(state=tk.DISABLED)

    def view_case_details(self):
        """View case details by finding and clicking the View button"""
        if not self.driver or not self.browser_initialized:
            messagebox.showwarning("Warning", "Please refresh to initialize browser first")
            return
            
        try:
            self.log_status("Looking for case details view buttons...")
            
            # Find all view buttons on the page
            self.view_buttons = self.driver.find_elements(By.CLASS_NAME, "viewCnrDetails")
            if not self.view_buttons:
                messagebox.showwarning("Warning", "No case details available to view")
                self.view_btn.config(state=tk.DISABLED)
                self.pdf_button.config(state=tk.DISABLED)
                return
                
            self.log_status(f"Found {len(self.view_buttons)} case(s). Opening details...")
            
            # Store current window handle
            self.current_case_window = self.driver.current_window_handle
            
            # Scroll to the button and click the first one
            self.driver.execute_script("arguments[0].scrollIntoView();", self.view_buttons[0])
            time.sleep(0.5)
            self.view_buttons[0].click()
            
            self.log_status("Waiting 3 seconds for details to load...")
            time.sleep(3)
            
            # Check if new window was opened
            if len(self.driver.window_handles) > 1:
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.log_status("Switched to case details window")
            else:
                self.log_status("Case details loaded in current window")
            
        except Exception as e:
            self.log_status(f"Error viewing case details: {str(e)}")
            self.view_btn.config(state=tk.DISABLED)
            self.pdf_button.config(state=tk.DISABLED)

    def save_page_as_pdf(self):
        """Save current page as PDF to the specified location without prompting"""
        try:
            # Define the save location
            save_location = r"C:\Users\Lenovo\OneDrive\Desktop\Rajan\Project assignment\case_details.pdf"
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(save_location), exist_ok=True)
            
            # Method 1: Try Chrome DevTools Protocol
            try:
                self.log_status("Attempting to save PDF using Chrome DevTools...")
                
                print_options = {
                    'landscape': False,
                    'displayHeaderFooter': False,
                    'printBackground': True,
                    'preferCSSPageSize': True,
                    'marginTop': 0,
                    'marginBottom': 0,
                    'marginLeft': 0,
                    'marginRight': 0
                }
                
                result = self.driver.execute_cdp_cmd("Page.printToPDF", print_options)
                
                # Save PDF
                with open(save_location, 'wb') as file:
                    file.write(base64.b64decode(result['data']))
                
                self.log_status(f"Case details saved as PDF: {save_location}")
                return True
                
            except Exception as cdp_error:
                self.log_status(f"Chrome DevTools method failed: {str(cdp_error)}")
            
            # Method 2: Use keyboard shortcut to trigger print dialog
            try:
                self.log_status("Opening browser print dialog...")
                self.driver.execute_script("window.print();")
                time.sleep(2)  # Wait for print dialog
                
                # This method may not work without user interaction
                return False
                
            except Exception as print_error:
                self.log_status(f"Print dialog method failed: {str(print_error)}")
                return False
            
        except Exception as e:
            self.log_status(f"Error in save_page_as_pdf: {str(e)}")
            return False

    def generate_pdf(self):
        """Generate PDF from the current case details and exit"""
        if not self.driver or not self.browser_initialized:
            messagebox.showwarning("Warning", "Please refresh to initialize browser first")
            return
            
        try:
            # Check if we're already on a case details page
            current_url = self.driver.current_url.lower()
            if "case-details" in current_url or "cnrno" in current_url:
                if self.save_page_as_pdf():
                    self.log_status("PDF saved successfully, exiting...")
                else:
                    self.log_status("PDF save failed")
                
                # Close the browser
                self.close_browser()
                # Exit the application
                self.root.quit()
                return
                
            # If not, try to find view buttons
            try:
                view_buttons = self.driver.find_elements(By.CLASS_NAME, "viewCnrDetails")
                if view_buttons:
                    self.view_case_details()
                    time.sleep(3)  # Wait for details to load
                    if self.save_page_as_pdf():
                        self.log_status("PDF saved successfully, exiting...")
                    else:
                        self.log_status("PDF save failed")
                    
                    # Close the browser
                    self.close_browser()
                    # Exit the application
                    self.root.quit()
                else:
                    self.log_status("No case details available to save as PDF")
            except Exception as e:
                self.log_status(f"Error finding case details: {str(e)}")
                
        except Exception as e:
            self.log_status(f"Error generating PDF: {str(e)}")

    def validate_inputs(self):
        """Validate user inputs"""
        if self.case_type_var.get() == "--Select--" or self.case_type_var.get() == "":
            messagebox.showwarning("Warning", "Please select a case type")
            return False
        
        if not self.case_number_var.get().strip():
            messagebox.showwarning("Warning", "Please enter case number")
            return False
        
        if not self.case_year_var.get().strip():
            messagebox.showwarning("Warning", "Please enter case year")
            return False
        
        if not self.captcha_var.get().strip():
            messagebox.showwarning("Warning", "Please enter captcha")
            return False
        
        return True

    def reset_form(self):
        """Reset all form fields"""
        self.case_type_var.set("--Select--")
        self.case_number_var.set("")
        self.case_year_var.set("")
        self.captcha_var.set("")
        self.captcha_label.config(image="", text="Click Refresh to initialize browser and load captcha")
        self.captcha_photo = None
        self.pdf_button.config(state=tk.DISABLED)
        self.view_btn.config(state=tk.DISABLED)
        if hasattr(self, 'view_buttons'):
            del self.view_buttons
        self.log_status("Form reset")

    def close_browser(self):
        """Close browser session"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                self.wait = None
                self.current_case_window = None
                self.browser_initialized = False
                self.pdf_button.config(state=tk.DISABLED)
                self.view_btn.config(state=tk.DISABLED)
                if hasattr(self, 'view_buttons'):
                    del self.view_buttons
                self.captcha_label.config(image="", text="Click Refresh to initialize browser and load captcha")
                self.log_status("Browser closed")
            except Exception as e:
                self.log_status(f"Error closing browser: {str(e)}")
        else:
            self.log_status("No browser session to close")

    def __del__(self):
        """Cleanup when object is destroyed"""
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
        except:
            pass  # Ignore any errors during cleanup

def main():
    root = tk.Tk()
    app = CourtCaseSearchAutomation(root)
    
    # Handle window close event
    def on_closing():
        app.close_browser()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()