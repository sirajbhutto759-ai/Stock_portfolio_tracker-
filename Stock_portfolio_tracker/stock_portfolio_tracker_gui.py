# ============================================================
#         STOCK PORTFOLIO TRACKER  —  GUI Version
#         CodeAlpha Internship Project
#         Author: Siraj  |  Date: October 2026
#         Built with Tkinter (Python's built-in GUI library)
#         No external libraries required!
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog


# -------------------------------------------------------
# HARDCODED STOCK DATA
# Dictionary: symbol -> (company name, price in USD)
# -------------------------------------------------------
STOCKS = {
    "AAPL":  ("Apple Inc.",         189.30),
    "TSLA":  ("Tesla Inc.",         177.82),
    "MSFT":  ("Microsoft Corp.",    415.50),
    "GOOGL": ("Alphabet (Google)",  175.98),
    "AMZN":  ("Amazon.com Inc.",    196.45),
    "NVDA":  ("NVIDIA Corp.",       875.40),
    "META":  ("Meta Platforms",     527.10),
    "NFLX":  ("Netflix Inc.",       638.29),
}

# -------------------------------------------------------
# COLOUR & FONT CONSTANTS  (dark-theme design system)
# -------------------------------------------------------
BG_DARK     = "#0D1117"   # Main background  (very dark navy)
BG_CARD     = "#161B22"   # Card / panel background
BG_HEADER   = "#1F2937"   # Table header background
ACCENT      = "#58A6FF"   # Primary accent blue
ACCENT2     = "#3FB950"   # Green for positive values
ACCENT3     = "#F78166"   # Red / warning colour
GOLD        = "#E3B341"   # Gold for totals
TEXT_MAIN   = "#E6EDF3"   # Main readable text
TEXT_DIM    = "#8B949E"   # Dimmed / secondary text
BORDER      = "#30363D"   # Subtle border lines

FONT_TITLE  = ("Segoe UI", 20, "bold")
FONT_SUB    = ("Segoe UI", 11)
FONT_LABEL  = ("Segoe UI", 10, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_MONO   = ("Consolas", 10)
FONT_TOTAL  = ("Segoe UI", 13, "bold")


# ============================================================
#  MAIN APPLICATION CLASS
# ============================================================
class StockPortfolioApp(tk.Tk):
    """Root window for the Stock Portfolio Tracker GUI."""

    def __init__(self):
        super().__init__()

        # ---- Window setup ----
        self.title("Stock Portfolio Tracker — CodeAlpha")
        self.geometry("1000x700")
        self.minsize(900, 620)
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        # ---- Portfolio data: symbol -> quantity ----
        self.portfolio = {}

        # ---- Build the UI ----
        self._build_header()
        self._build_main_area()
        self._build_status_bar()

        # ---- Centre the window on screen ----
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ----------------------------------------------------------
    #  HEADER BAR
    # ----------------------------------------------------------
    def _build_header(self):
        """Top gradient-like header with title and subtitle."""
        header = tk.Frame(self, bg=BG_CARD, pady=18)
        header.pack(fill="x", side="top")

        # Coloured left accent bar
        accent_bar = tk.Frame(header, bg=ACCENT, width=5)
        accent_bar.pack(side="left", fill="y", padx=(0, 18))

        # Title block
        title_block = tk.Frame(header, bg=BG_CARD)
        title_block.pack(side="left")

        tk.Label(title_block, text="Stock Portfolio Tracker",
                 font=FONT_TITLE, fg=TEXT_MAIN, bg=BG_CARD).pack(anchor="w")
        tk.Label(title_block, text="CodeAlpha Internship Project  |  Prices are hardcoded for demo",
                 font=FONT_BODY, fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w")

        # Save button (top-right)
        btn_save = tk.Button(header, text="  Save Portfolio  ", font=FONT_LABEL,
                             bg=ACCENT, fg="#000000", activebackground="#79C0FF",
                             activeforeground="#000000", relief="flat", cursor="hand2",
                             padx=10, pady=6, command=self._save_to_file)
        btn_save.pack(side="right", padx=20)

    # ----------------------------------------------------------
    #  MAIN TWO-COLUMN AREA
    # ----------------------------------------------------------
    def _build_main_area(self):
        """Left panel = inputs; Right panel = portfolio table."""
        container = tk.Frame(self, bg=BG_DARK)
        container.pack(fill="both", expand=True, padx=16, pady=12)

        # LEFT panel (fixed width)
        self._build_left_panel(container)

        # Vertical separator
        sep = tk.Frame(container, bg=BORDER, width=1)
        sep.pack(side="left", fill="y", padx=12)

        # RIGHT panel (expands)
        self._build_right_panel(container)

    # ----------------------------------------------------------
    #  LEFT PANEL  —  Stock selector + Add form
    # ----------------------------------------------------------
    def _build_left_panel(self, parent):
        left = tk.Frame(parent, bg=BG_DARK, width=310)
        left.pack(side="left", fill="y", padx=(0, 0))
        left.pack_propagate(False)   # Keep fixed width

        # ---- Section: Add Stock ----
        self._section_label(left, "Add a Stock")

        card = tk.Frame(left, bg=BG_CARD, pady=16, padx=16,
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x", pady=(0, 16))

        # Stock symbol label + dropdown
        tk.Label(card, text="Stock Symbol", font=FONT_LABEL,
                 fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w")

        self.symbol_var = tk.StringVar(value="AAPL")
        symbol_menu = ttk.Combobox(card, textvariable=self.symbol_var,
                                   values=list(STOCKS.keys()),
                                   font=FONT_MONO, state="readonly", width=26)
        symbol_menu.pack(fill="x", pady=(4, 12))
        symbol_menu.bind("<<ComboboxSelected>>", self._on_symbol_change)

        # Company + price preview
        self.preview_var = tk.StringVar()
        self._update_preview("AAPL")
        tk.Label(card, textvariable=self.preview_var, font=FONT_BODY,
                 fg=ACCENT, bg=BG_CARD, anchor="w").pack(fill="x", pady=(0, 12))

        # Quantity
        tk.Label(card, text="Number of Shares", font=FONT_LABEL,
                 fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w")

        self.qty_var = tk.StringVar(value="1")
        qty_entry = tk.Entry(card, textvariable=self.qty_var, font=FONT_MONO,
                             bg=BG_HEADER, fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
                             relief="flat", bd=6, width=28)
        qty_entry.pack(fill="x", pady=(4, 4))

        # Calculated value preview
        self.calc_var = tk.StringVar(value="Value:  $0.00")
        tk.Label(card, textvariable=self.calc_var, font=FONT_BODY,
                 fg=ACCENT2, bg=BG_CARD, anchor="w").pack(fill="x", pady=(0, 14))

        # Trace qty changes for live calculation
        self.qty_var.trace_add("write", self._update_calc)
        self.symbol_var.trace_add("write", self._update_calc)

        # ADD button
        btn_add = tk.Button(card, text="+ Add to Portfolio", font=FONT_LABEL,
                            bg=ACCENT2, fg="#000000", activebackground="#56D364",
                            activeforeground="#000000", relief="flat", cursor="hand2",
                            padx=10, pady=8, command=self._add_stock)
        btn_add.pack(fill="x")

        # ---- Section: Available Stocks ----
        self._section_label(left, "Available Stocks")

        stocks_card = tk.Frame(left, bg=BG_CARD,
                               highlightbackground=BORDER, highlightthickness=1)
        stocks_card.pack(fill="both", expand=True, pady=(0, 4))

        # Scrollable list of stocks
        canvas   = tk.Canvas(stocks_card, bg=BG_CARD, highlightthickness=0)
        scrollbar = ttk.Scrollbar(stocks_card, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG_CARD)

        scroll_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Header row
        hdr = tk.Frame(scroll_frame, bg=BG_HEADER, pady=6)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"  {'SYM':<6} {'PRICE':>10}",
                 font=FONT_LABEL, fg=TEXT_DIM, bg=BG_HEADER).pack(anchor="w")

        # One row per stock
        for i, (sym, (company, price)) in enumerate(STOCKS.items()):
            row_bg = BG_CARD if i % 2 == 0 else "#1A2030"
            row = tk.Frame(scroll_frame, bg=row_bg, pady=5, padx=6)
            row.pack(fill="x")
            tk.Label(row, text=f"{sym:<6}", font=FONT_MONO,
                     fg=ACCENT, bg=row_bg).pack(side="left")
            tk.Label(row, text=f"${price:>8.2f}", font=FONT_MONO,
                     fg=ACCENT2, bg=row_bg).pack(side="right")
            tk.Label(row, text=company, font=FONT_BODY,
                     fg=TEXT_DIM, bg=row_bg).pack(side="left", padx=6)

    # ----------------------------------------------------------
    #  RIGHT PANEL  —  Portfolio table + totals
    # ----------------------------------------------------------
    def _build_right_panel(self, parent):
        right = tk.Frame(parent, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True)

        self._section_label(right, "Your Portfolio")

        # ---- Treeview table ----
        cols = ("Symbol", "Company", "Shares", "Price (USD)", "Value (USD)")
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Portfolio.Treeview",
                        background=BG_CARD,
                        foreground=TEXT_MAIN,
                        fieldbackground=BG_CARD,
                        rowheight=32,
                        font=FONT_MONO,
                        borderwidth=0)
        style.configure("Portfolio.Treeview.Heading",
                        background=BG_HEADER,
                        foreground=TEXT_DIM,
                        font=FONT_LABEL,
                        borderwidth=0)
        style.map("Portfolio.Treeview",
                  background=[("selected", "#1C3A5F")],
                  foreground=[("selected", TEXT_MAIN)])

        tree_frame = tk.Frame(right, bg=BG_DARK)
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings",
                                 style="Portfolio.Treeview", selectmode="browse")

        # Column config
        col_widths = {"Symbol": 80, "Company": 180, "Shares": 80,
                      "Price (USD)": 120, "Value (USD)": 130}
        col_anchors = {"Symbol": "center", "Company": "w", "Shares": "center",
                       "Price (USD)": "e", "Value (USD)": "e"}
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths[col], anchor=col_anchors[col])

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Tag colours for alternating rows
        self.tree.tag_configure("odd",  background=BG_CARD)
        self.tree.tag_configure("even", background="#1A2030")

        # ---- Remove selected row button ----
        btn_remove = tk.Button(right, text="Remove Selected Row", font=FONT_BODY,
                               bg=ACCENT3, fg="#000000", activebackground="#FF9492",
                               activeforeground="#000000", relief="flat", cursor="hand2",
                               padx=8, pady=5, command=self._remove_selected)
        btn_remove.pack(anchor="e", pady=(6, 0))

        # ---- Totals bar ----
        totals_frame = tk.Frame(right, bg=BG_HEADER, pady=14, padx=16,
                                highlightbackground=GOLD, highlightthickness=1)
        totals_frame.pack(fill="x", pady=(12, 0))

        tk.Label(totals_frame, text="TOTAL PORTFOLIO VALUE",
                 font=FONT_TOTAL, fg=TEXT_DIM, bg=BG_HEADER).pack(side="left")

        self.total_var = tk.StringVar(value="$0.00")
        tk.Label(totals_frame, textvariable=self.total_var,
                 font=FONT_TOTAL, fg=GOLD, bg=BG_HEADER).pack(side="right")

        # Holdings count
        self.count_var = tk.StringVar(value="0 holdings")
        tk.Label(totals_frame, textvariable=self.count_var,
                 font=FONT_BODY, fg=TEXT_DIM, bg=BG_HEADER).pack(side="right", padx=20)

    # ----------------------------------------------------------
    #  STATUS BAR
    # ----------------------------------------------------------
    def _build_status_bar(self):
        """Thin status message bar at the bottom."""
        bar = tk.Frame(self, bg=BG_HEADER, pady=5)
        bar.pack(fill="x", side="bottom")
        self.status_var = tk.StringVar(value="Ready  —  Select a stock and enter a quantity to begin.")
        tk.Label(bar, textvariable=self.status_var, font=FONT_BODY,
                 fg=TEXT_DIM, bg=BG_HEADER, anchor="w", padx=14).pack(fill="x")

    # ----------------------------------------------------------
    #  HELPER: section heading label
    # ----------------------------------------------------------
    def _section_label(self, parent, text):
        row = tk.Frame(parent, bg=BG_DARK)
        row.pack(fill="x", pady=(8, 4))
        tk.Label(row, text=text.upper(), font=("Segoe UI", 9, "bold"),
                 fg=TEXT_DIM, bg=BG_DARK).pack(side="left")
        tk.Frame(row, bg=BORDER, height=1).pack(side="left", fill="x", expand=True, padx=8, pady=6)

    # ----------------------------------------------------------
    #  EVENT: symbol dropdown changed
    # ----------------------------------------------------------
    def _on_symbol_change(self, event=None):
        self._update_preview(self.symbol_var.get())
        self._update_calc()

    def _update_preview(self, sym):
        company, price = STOCKS.get(sym, ("Unknown", 0.0))
        self.preview_var.set(f"{company}  —  ${price:.2f} per share")

    # ----------------------------------------------------------
    #  EVENT: live calculation of value = qty * price
    # ----------------------------------------------------------
    def _update_calc(self, *args):
        sym = self.symbol_var.get()
        try:
            qty   = int(self.qty_var.get())
            price = STOCKS[sym][1]
            value = qty * price
            self.calc_var.set(f"Value:  ${value:,.2f}")
        except (ValueError, KeyError):
            self.calc_var.set("Value:  —")

    # ----------------------------------------------------------
    #  ACTION: Add stock to portfolio
    # ----------------------------------------------------------
    def _add_stock(self):
        sym = self.symbol_var.get()

        # Validate quantity
        try:
            qty = int(self.qty_var.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Quantity",
                                 "Please enter a positive whole number for shares.")
            return

        # Add or update portfolio dict
        if sym in self.portfolio:
            self.portfolio[sym] += qty
        else:
            self.portfolio[sym] = qty

        self._refresh_table()
        self._set_status(f"[OK]  {sym} x{qty} shares added. Portfolio updated.")

    # ----------------------------------------------------------
    #  ACTION: Remove selected row
    # ----------------------------------------------------------
    def _remove_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Nothing Selected", "Click a row in the table to select it first.")
            return
        item = self.tree.item(selected[0])
        sym  = item["values"][0]
        if sym in self.portfolio:
            del self.portfolio[sym]
        self._refresh_table()
        self._set_status(f"Removed {sym} from portfolio.")

    # ----------------------------------------------------------
    #  Refresh the Treeview table & totals
    # ----------------------------------------------------------
    def _refresh_table(self):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        total = 0.0
        for i, (sym, qty) in enumerate(self.portfolio.items()):
            company, price = STOCKS[sym]
            value = qty * price
            total += value
            tag   = "odd" if i % 2 == 0 else "even"
            self.tree.insert("", "end", values=(
                sym, company, qty, f"${price:,.2f}", f"${value:,.2f}"
            ), tags=(tag,))

        self.total_var.set(f"${total:,.2f}")
        count = len(self.portfolio)
        self.count_var.set(f"{count} holding{'s' if count != 1 else ''}")

    # ----------------------------------------------------------
    #  ACTION: Save portfolio to .txt file
    # ----------------------------------------------------------
    def _save_to_file(self):
        if not self.portfolio:
            messagebox.showinfo("Empty Portfolio", "Add some stocks before saving.")
            return

        # Let user choose save location
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="portfolio_summary.txt",
            title="Save Portfolio Summary"
        )
        if not filepath:
            return   # User cancelled

        total = 0.0
        lines = []
        lines.append("=" * 58)
        lines.append("         STOCK PORTFOLIO SUMMARY")
        lines.append("         Generated by Stock Portfolio Tracker (GUI)")
        lines.append("=" * 58)
        lines.append(f"  {'SYMBOL':<8} {'COMPANY':<22} {'SHARES':>6} {'PRICE':>10} {'VALUE':>12}")
        lines.append("-" * 58)

        for sym, qty in self.portfolio.items():
            company, price = STOCKS[sym]
            value  = qty * price
            total += value
            lines.append(
                f"  {sym:<8} {company:<22} {qty:>6} ${price:>9.2f} ${value:>11.2f}"
            )

        lines.append("-" * 58)
        lines.append(f"  {'TOTAL PORTFOLIO VALUE':<40} ${total:>13.2f}")
        lines.append("=" * 58)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        self._set_status(f"Portfolio saved to: {filepath}")
        messagebox.showinfo("Saved!", f"Portfolio summary saved to:\n{filepath}")

    # ----------------------------------------------------------
    #  Update status bar message
    # ----------------------------------------------------------
    def _set_status(self, msg):
        self.status_var.set(msg)


# ============================================================
#  ENTRY POINT
# ============================================================
if __name__ == "__main__":
    app = StockPortfolioApp()
    app.mainloop()
