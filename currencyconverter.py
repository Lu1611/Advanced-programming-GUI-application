import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw
import os

# -----------------------------
# API HANDLER (KEYLESS VERSION)
# -----------------------------
class CurrencyAPI:
    def __init__(self):
        # Using ExchangeRate-API (No key required for latest rates)
        self.base_url = "https://open.er-api.com/v6/latest/"

    def get_exchange_rate(self, base, target):
        try:
            response = requests.get(f"{self.base_url}{base}", timeout=10)
            data = response.json()
            
            if data.get("result") == "success":
                return data["rates"][target]
            else:
                raise Exception(data.get("error-type", "Unknown API error"))
        except Exception as e:
            raise Exception(f"Connection failed: {e}")

# -----------------------------
# MAIN APPLICATION CLASS
# -----------------------------
class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Global Currency Converter")
        self.root.geometry("500x600")
        self.bg_color = "#f4f4f9"
        self.root.configure(bg=self.bg_color)

        self.api = CurrencyAPI()

        # Variables
        self.amount_var = tk.StringVar(value="1.00")
        self.result_var = tk.StringVar(value="Select currencies and hit Convert")
        self.search_var = tk.StringVar()

        self.currencies = [
            "USD", "EUR", "GBP", "JPY", "AUD",
            "CAD", "CHF", "CNY", "NZD", "INR", "AED", "BRL"
        ]
        
        self.flag_images = {}
        self.load_flags()
        self.create_widgets()
        self.update_flags()

    def load_flags(self):
        """Loads images if they exist, otherwise creates colored placeholders."""
        for code in self.currencies:
            path = f"flags/{code.lower()}.png"
            try:
                if os.path.exists(path):
                    img = Image.open(path).resize((40, 25), Image.Resampling.LANCZOS)
                else:
                    # Create a colorful placeholder so the app still looks good
                    img = Image.new('RGB', (40, 25), color='#cccccc')
                    draw = ImageDraw.Draw(img)
                    draw.text((5, 5), code[:2], fill="black")
                
                self.flag_images[code] = ImageTk.PhotoImage(img)
            except:
                pass

    def create_widgets(self):
        # Header
        tk.Label(self.root, text="Currency Converter", font=("Arial", 20, "bold"), 
                 bg=self.bg_color, fg="#333").pack(pady=20)

        # Main Container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(padx=20, fill="x")

        # Amount Input
        tk.Label(main_frame, text="Amount to Convert:", bg=self.bg_color).grid(row=0, column=0, sticky="w")
        tk.Entry(main_frame, textvariable=self.amount_var, font=("Arial", 12)).grid(row=1, column=0, columnspan=2, sticky="we", pady=5)

        # Search Bar
        tk.Label(main_frame, text="Filter Currencies:", bg=self.bg_color).grid(row=2, column=0, sticky="w", pady=(10,0))
        search_entry = tk.Entry(main_frame, textvariable=self.search_var, font=("Arial", 10), fg="grey")
        search_entry.grid(row=3, column=0, columnspan=2, sticky="we", pady=5)
        search_entry.bind("<KeyRelease>", self.filter_currencies)

        # From Currency
        tk.Label(main_frame, text="From:", bg=self.bg_color).grid(row=4, column=0, sticky="w", pady=5)
        self.from_currency = ttk.Combobox(main_frame, values=self.currencies, state="readonly")
        self.from_currency.set("USD")
        self.from_currency.grid(row=5, column=0, sticky="we")
        self.from_currency.bind("<<ComboboxSelected>>", lambda e: self.update_flags())
        
        self.from_flag_label = tk.Label(main_frame, bg=self.bg_color)
        self.from_flag_label.grid(row=5, column=1, padx=10)

        # To Currency
        tk.Label(main_frame, text="To:", bg=self.bg_color).grid(row=6, column=0, sticky="w", pady=5)
        self.to_currency = ttk.Combobox(main_frame, values=self.currencies, state="readonly")
        self.to_currency.set("EUR")
        self.to_currency.grid(row=7, column=0, sticky="we")
        self.to_currency.bind("<<ComboboxSelected>>", lambda e: self.update_flags())

        self.to_flag_label = tk.Label(main_frame, bg=self.bg_color)
        self.to_flag_label.grid(row=7, column=1, padx=10)

        # Buttons
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Swap ⇅", command=self.swap_currencies, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Convert", command=self.convert, bg="#4CAF50", fg="white", width=15, font=("Arial", 10, "bold")).pack(side="left", padx=5)

        # Result display
        tk.Label(self.root, textvariable=self.result_var, font=("Arial", 14, "bold"), bg=self.bg_color, fg="#2c3e50").pack(pady=10)

        # History Box
        tk.Label(self.root, text="Recent Conversions:", bg=self.bg_color, font=("Arial", 10, "italic")).pack()
        self.history_box = tk.Listbox(self.root, width=50, height=6)
        self.history_box.pack(pady=10, padx=20)

    def update_flags(self):
        f_code = self.from_currency.get()
        t_code = self.to_currency.get()
        if f_code in self.flag_images:
            self.from_flag_label.config(image=self.flag_images[f_code])
        if t_code in self.flag_images:
            self.to_flag_label.config(image=self.flag_images[t_code])

    def convert(self):
        try:
            amount = float(self.amount_var.get())
            base = self.from_currency.get()
            target = self.to_currency.get()
            
            rate = self.api.get_exchange_rate(base, target)
            result = amount * rate
            
            res_str = f"{amount:,.2f} {base} = {result:,.2f} {target}"
            self.result_var.set(res_str)

            # Add to history
            time_now = datetime.now().strftime("%H:%M")
            self.history_box.insert(0, f"[{time_now}] {res_str}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the amount.")
        except Exception as e:
            messagebox.showerror("API Error", str(e))

    def swap_currencies(self):
        f, t = self.from_currency.get(), self.to_currency.get()
        self.from_currency.set(t)
        self.to_currency.set(f)
        self.update_flags()

    def filter_currencies(self, event):
        query = self.search_var.get().upper()
        filtered = [c for c in self.currencies if query in c]
        self.from_currency["values"] = filtered
        self.to_currency["values"] = filtered

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()