import os
import threading
import webbrowser
import customtkinter as ctk
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("dark")

class InfoModal(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("System Specs & Developer Profile")
        self.geometry("540x580")
        self.resizable(False, False)
        self.configure(fg_color="#101116")
        self.transient(parent)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        container = ctk.CTkFrame(
            self,
            fg_color="#171821",
            border_color="#2A2C3D",
            border_width=1,
            corner_radius=16
        )
        container.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            container,
            text="DEVELOPER PROFILE",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color="#818CF8",
            fg_color="#1E2038",
            corner_radius=6,
            padx=8,
            pady=3
        ).pack(anchor="w", padx=20, pady=(20, 4))

        ctk.CTkLabel(
            container,
            text="Rudra Wagh",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color="#F3F4F6"
        ).pack(anchor="w", padx=20)

        ctk.CTkLabel(
            container,
            text="AI & Data Science Engineer",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#9CA3AF"
        ).pack(anchor="w", padx=20, pady=(2, 16))

        links_frame = ctk.CTkFrame(container, fg_color="transparent")
        links_frame.pack(fill="x", padx=20, pady=(0, 16))

        ctk.CTkButton(
            links_frame,
            text="GitHub ↗",
            width=100,
            height=32,
            corner_radius=8,
            fg_color="#222436",
            hover_color="#2D304A",
            border_color="#3B3E5C",
            border_width=1,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=lambda: webbrowser.open("https://github.com/rudra1725")
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            links_frame,
            text="LinkedIn ↗",
            width=100,
            height=32,
            corner_radius=8,
            fg_color="#222436",
            hover_color="#2D304A",
            border_color="#3B3E5C",
            border_width=1,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=lambda: webbrowser.open("https://linkedin.com")
        ).pack(side="left")

        separator = ctk.CTkFrame(container, height=1, fg_color="#2A2C3D")
        separator.pack(fill="x", padx=20, pady=(0, 16))

        ctk.CTkLabel(
            container,
            text="HOW THE MINER WORKS",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#818CF8"
        ).pack(anchor="w", padx=20, pady=(0, 8))

        guide_box = ctk.CTkTextbox(
            container,
            fg_color="#0F1015",
            border_color="#222433",
            border_width=1,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#D1D5DB",
            wrap="word",
            height=220
        )
        guide_box.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        guide_content = (
            "1. Target Ingestion\n"
            "   Select a single file or a directory. The miner uses Python's os.walk "
            "   to isolate matching .log and .txt targets down nested folder trees.\n\n"
            "2. Non-Blocking Concurrency\n"
            "   Analysis runs on a detached daemon thread. This ensures the main UI "
            "   event loop never stutters, freezes, or locks under multi-megabyte log files.\n\n"
            "3. Memory-Safe Stream Search\n"
            "   Logs are parsed line-by-line using UTF-8 with automatic fallback handling, "
            "   indexing each target occurrence with exact line offsets.\n\n"
            "4. Report Generation\n"
            "   Export isolated lines to a structured audit report with standardized headers "
            "   and metadata indicators."
        )
        guide_box.insert("1.0", guide_content)
        guide_box.configure(state="disabled")

        ctk.CTkButton(
            container,
            text="Close",
            height=34,
            corner_radius=8,
            fg_color="#6366F1",
            hover_color="#4F46E5",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self.destroy
        ).pack(fill="x", padx=20, pady=(0, 18))


class NeumorphicLogMiner(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Log File Miner & Text Inspector")
        self.geometry("1060x780")
        self.minsize(900, 640)

        self.bg_root = "#0F1015"
        self.card_bg = "#171822"
        self.card_border = "#262838"
        self.surface_inner = "#101117"
        self.accent_glow = "#6366F1"
        self.accent_hover = "#4F46E5"
        self.text_dim = "#737894"
        self.text_light = "#F3F4F6"

        self.configure(fg_color=self.bg_root)

        self.results_data = {}
        self.is_scanning = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_header()
        self._build_controls_card()
        self._build_display_card()
        self._build_footer()

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=28, pady=(22, 12), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        meta_row = ctk.CTkFrame(header, fg_color="transparent")
        meta_row.grid(row=0, column=0, sticky="ew")
        meta_row.grid_columnconfigure(0, weight=1)

        tag_badge = ctk.CTkLabel(
            meta_row,
            text="ENGINE // MULTITHREADED PARSER",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color="#818CF8",
            fg_color="#1E2036",
            corner_radius=6,
            padx=10,
            pady=3
        )
        tag_badge.grid(row=0, column=0, sticky="w")

        info_btn = ctk.CTkButton(
            meta_row,
            text="ⓘ  System Info & Dev",
            width=150,
            height=28,
            corner_radius=8,
            fg_color="#1E2034",
            hover_color="#2A2D4A",
            border_color="#363959",
            border_width=1,
            text_color="#A5B4FC",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            command=self._open_info_modal
        )
        info_btn.grid(row=0, column=1, sticky="e")

        title = ctk.CTkLabel(
            header,
            text="Log File Miner & Text Inspector",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=self.text_light
        )
        title.grid(row=1, column=0, sticky="w", pady=(6, 0))

        dev_caption = ctk.CTkLabel(
            header,
            text="Developed by Rudra Wagh  •  High-throughput log stream parser & keyword isolation",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#818CF8"
        )
        dev_caption.grid(row=2, column=0, sticky="w", pady=(2, 0))

    def _build_controls_card(self):
        card = ctk.CTkFrame(
            self,
            fg_color=self.card_bg,
            border_color=self.card_border,
            border_width=1,
            corner_radius=16
        )
        card.grid(row=1, column=0, padx=28, pady=(0, 14), sticky="ew")
        card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            card,
            text="TARGET SOURCE",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=self.text_dim
        ).grid(row=0, column=0, padx=(20, 12), pady=(18, 6), sticky="w")

        self.path_entry = ctk.CTkEntry(
            card,
            placeholder_text="Enter file path or select directory...",
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color=self.surface_inner,
            border_color=self.card_border,
            border_width=1,
            corner_radius=10,
            height=38,
            text_color=self.text_light
        )
        self.path_entry.grid(row=0, column=1, padx=8, pady=(18, 6), sticky="ew")

        btn_box = ctk.CTkFrame(card, fg_color="transparent")
        btn_box.grid(row=0, column=2, padx=(8, 20), pady=(18, 6), sticky="e")

        ctk.CTkButton(
            btn_box,
            text="File",
            width=65,
            height=34,
            corner_radius=8,
            fg_color="#222434",
            hover_color="#2E3146",
            border_color="#363952",
            border_width=1,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self._browse_file
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            btn_box,
            text="Folder",
            width=65,
            height=34,
            corner_radius=8,
            fg_color="#222434",
            hover_color="#2E3146",
            border_color="#363952",
            border_width=1,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self._browse_folder
        ).pack(side="left", padx=3)

        ctk.CTkLabel(
            card,
            text="QUERY TOKEN",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=self.text_dim
        ).grid(row=1, column=0, padx=(20, 12), pady=(6, 18), sticky="w")

        self.keyword_entry = ctk.CTkEntry(
            card,
            placeholder_text="String literal or pattern to scan (e.g. NullPointerException, 404, ERROR)...",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color=self.surface_inner,
            border_color=self.card_border,
            border_width=1,
            corner_radius=10,
            height=38,
            text_color=self.text_light
        )
        self.keyword_entry.grid(row=1, column=1, padx=8, pady=(6, 18), sticky="ew")
        self.keyword_entry.bind("<Return>", lambda _: self._start_scan_thread())

        action_box = ctk.CTkFrame(card, fg_color="transparent")
        action_box.grid(row=1, column=2, padx=(8, 20), pady=(6, 18), sticky="e")

        self.case_var = ctk.BooleanVar(value=False)
        self.case_cb = ctk.CTkCheckBox(
            action_box,
            text="Match Case",
            variable=self.case_var,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.text_dim,
            border_color="#3D4058",
            fg_color=self.accent_glow,
            hover_color=self.accent_hover,
            corner_radius=5
        )
        self.case_cb.pack(side="left", padx=(0, 14))

        self.scan_btn = ctk.CTkButton(
            action_box,
            text="Execute Scan",
            width=120,
            height=36,
            corner_radius=8,
            fg_color=self.accent_glow,
            hover_color=self.accent_hover,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=self._start_scan_thread
        )
        self.scan_btn.pack(side="left")

    def _build_display_card(self):
        display_frame = ctk.CTkFrame(
            self,
            fg_color=self.card_bg,
            border_color=self.card_border,
            border_width=1,
            corner_radius=16
        )
        display_frame.grid(row=2, column=0, padx=28, pady=0, sticky="nsew")
        display_frame.grid_rowconfigure(1, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)

        panel_bar = ctk.CTkFrame(display_frame, fg_color="transparent")
        panel_bar.grid(row=0, column=0, padx=20, pady=(14, 8), sticky="ew")
        panel_bar.grid_columnconfigure(0, weight=1)

        self.results_title = ctk.CTkLabel(
            panel_bar,
            text="STREAM OUTPUT // AUDIT TRAIL",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=self.text_dim
        )
        self.results_title.grid(row=0, column=0, sticky="w")

        self.export_btn = ctk.CTkButton(
            panel_bar,
            text="Export Report",
            width=120,
            height=32,
            corner_radius=8,
            fg_color="#1E2034",
            hover_color="#282C48",
            border_color="#383D61",
            border_width=1,
            text_color="#A5B4FC",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            state="disabled",
            command=self._export_results
        )
        self.export_btn.grid(row=0, column=1, sticky="e")

        self.textbox = ctk.CTkTextbox(
            display_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="none",
            corner_radius=10,
            fg_color=self.surface_inner,
            border_color=self.card_border,
            border_width=1,
            text_color="#E2E8F0"
        )
        self.textbox.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")

    def _build_footer(self):
        footer = ctk.CTkFrame(self, fg_color="transparent", height=28)
        footer.grid(row=3, column=0, padx=32, pady=(10, 16), sticky="ew")
        footer.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            footer,
            text="System Idle. Ready for stream input.",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.text_dim
        )
        self.status_label.grid(row=0, column=0, sticky="w")

    def _open_info_modal(self):
        InfoModal(self)

    def _browse_file(self):
        chosen = filedialog.askopenfilename(filetypes=[("Log & Text Files", "*.log *.txt"), ("All Files", "*.*")])
        if chosen:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, os.path.normpath(chosen))

    def _browse_folder(self):
        chosen = filedialog.askdirectory()
        if chosen:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, os.path.normpath(chosen))

    def _start_scan_thread(self):
        if self.is_scanning:
            return

        target_path = self.path_entry.get().strip().strip('"').strip("'")
        keyword = self.keyword_entry.get().strip()

        if not target_path or not os.path.exists(target_path):
            messagebox.showwarning("Invalid Path", "Please provide a valid file or directory path.")
            return

        if not keyword:
            messagebox.showwarning("Missing Keyword", "Please specify a search token.")
            return

        self.is_scanning = True
        self.scan_btn.configure(state="disabled", text="Scanning...")
        self.export_btn.configure(state="disabled")
        self.status_label.configure(text=f"Parsing stream for '{keyword}'...")
        self.textbox.delete("1.0", "end")

        thread = threading.Thread(
            target=self._scan_worker,
            args=(target_path, keyword, self.case_var.get()),
            daemon=True
        )
        thread.start()

    def _scan_worker(self, path, keyword, case_sensitive):
        valid_extensions = ('.log', '.txt')
        target_files = []

        if os.path.isfile(path):
            target_files.append(path)
        else:
            for root, _, files in os.walk(path):
                for f in files:
                    if f.lower().endswith(valid_extensions):
                        target_files.append(os.path.join(root, f))

        all_matches = {}
        total_hits = 0
        cmp_keyword = keyword if case_sensitive else keyword.lower()

        for filepath in target_files:
            try:
                with open(filepath, 'r', encoding='utf-8', errors='replace') as file:
                    for line_number, line in enumerate(file, start=1):
                        cmp_line = line if case_sensitive else line.lower()
                        if cmp_keyword in cmp_line:
                            if filepath not in all_matches:
                                all_matches[filepath] = []
                            all_matches[filepath].append((line_number, line.rstrip('\r\n')))
                            total_hits += 1
            except Exception:
                continue

        self.after(0, self._render_results, all_matches, total_hits, len(target_files), keyword)

    def _render_results(self, all_matches, total_hits, scanned_count, keyword):
        self.results_data = all_matches
        self.is_scanning = False
        self.scan_btn.configure(state="normal", text="Execute Scan")

        if total_hits == 0:
            self.textbox.insert("end", f"\n[!] Zero occurrences detected for token '{keyword}' across {scanned_count} inspected file(s).\n")
            self.status_label.configure(text=f"Process terminated: 0 matches found in {scanned_count} files.")
            return

        self.export_btn.configure(state="normal")
        self.status_label.configure(text=f"Inspection complete: {total_hits} occurrences found across {len(all_matches)} file(s).")

        display_text = []
        for filepath, entries in all_matches.items():
            display_text.append(f"┌─ [{filepath}] ── ({len(entries)} matches)")
            for line_no, content in entries:
                display_text.append(f"│  Line {line_no:>5} ┆  {content}")
            display_text.append("└────────────────────────────────────────────────────────────\n")

        self.textbox.insert("end", "\n".join(display_text))

    def _export_results(self):
        if not self.results_data:
            return

        export_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt"), ("Log File", "*.log")],
            initialfile="miner_report.txt"
        )
        if not export_path:
            return

        try:
            with open(export_path, "w", encoding="utf-8") as out:
                out.write("LOG FILE MINER - EXTRACTION REPORT\n")
                out.write(f"Developer: Rudra Wagh\n")
                out.write(f"Target Keyword: {self.keyword_entry.get().strip()}\n")
                out.write("=" * 70 + "\n\n")

                for filepath, entries in self.results_data.items():
                    out.write(f"Source: {filepath}\n")
                    out.write("-" * 50 + "\n")
                    for line_no, content in entries:
                        out.write(f"Line {line_no}: {content}\n")
                    out.write("\n")

            messagebox.showinfo("Export Successful", f"Audit output saved to:\n{export_path}")
        except Exception as error:
            messagebox.showerror("Export Error", f"Unable to generate report: {error}")

if __name__ == "__main__":
    app = NeumorphicLogMiner()
    app.mainloop()
