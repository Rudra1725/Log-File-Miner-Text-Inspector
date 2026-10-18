import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LogMinerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Log File Miner & Text Inspector")
        self.geometry("980x680")
        self.minsize(800, 550)

        self.results_data = {}
        self.is_scanning = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_header()
        self._build_controls()
        self._build_results_view()
        self._build_status_bar()

    def _build_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=24, pady=(20, 10), sticky="ew")

        title = ctk.CTkLabel(
            header_frame,
            text="Log File Miner & Text Inspector",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Inspect logs and text files, isolate target keywords, and export structured matches.",
            font=ctk.CTkFont(size=13),
            text_color="#9CA3AF"
        )
        subtitle.pack(anchor="w", pady=(2, 0))

    def _build_controls(self):
        ctrl_card = ctk.CTkFrame(self, corner_radius=10, fg_color="#1E1E24")
        ctrl_card.grid(row=1, column=0, padx=24, pady=10, sticky="ew")
        ctrl_card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(ctrl_card, text="Target Path:", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=0, column=0, padx=(16, 8), pady=(16, 8), sticky="w"
        )

        self.path_entry = ctk.CTkEntry(ctrl_card, placeholder_text="Select a file or directory...")
        self.path_entry.grid(row=0, column=1, padx=8, pady=(16, 8), sticky="ew")

        btn_row = ctk.CTkFrame(ctrl_card, fg_color="transparent")
        btn_row.grid(row=0, column=2, padx=(8, 16), pady=(16, 8), sticky="e")

        ctk.CTkButton(btn_row, text="File", width=70, command=self._browse_file).pack(side="left", padx=3)
        ctk.CTkButton(btn_row, text="Folder", width=70, command=self._browse_folder).pack(side="left", padx=3)

        ctk.CTkLabel(ctrl_card, text="Search Keyword:", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=1, column=0, padx=(16, 8), pady=(8, 16), sticky="w"
        )

        self.keyword_entry = ctk.CTkEntry(ctrl_card, placeholder_text="e.g. error, timeout, python...")
        self.keyword_entry.grid(row=1, column=1, padx=8, pady=(8, 16), sticky="ew")
        self.keyword_entry.bind("<Return>", lambda _: self._start_scan_thread())

        opts_row = ctk.CTkFrame(ctrl_card, fg_color="transparent")
        opts_row.grid(row=1, column=2, padx=(8, 16), pady=(8, 16), sticky="e")

        self.case_var = ctk.BooleanVar(value=False)
        self.case_cb = ctk.CTkCheckBox(opts_row, text="Match Case", variable=self.case_var)
        self.case_cb.pack(side="left", padx=(0, 12))

        self.scan_btn = ctk.CTkButton(
            opts_row,
            text="Start Scan",
            width=110,
            command=self._start_scan_thread
        )
        self.scan_btn.pack(side="left")

    def _build_results_view(self):
        results_container = ctk.CTkFrame(self, corner_radius=10, fg_color="#1E1E24")
        results_container.grid(row=2, column=0, padx=24, pady=10, sticky="nsew")
        results_container.grid_rowconfigure(1, weight=1)
        results_container.grid_columnconfigure(0, weight=1)

        action_bar = ctk.CTkFrame(results_container, fg_color="transparent")
        action_bar.grid(row=0, column=0, padx=16, pady=(12, 6), sticky="ew")
        action_bar.grid_columnconfigure(0, weight=1)

        self.results_label = ctk.CTkLabel(
            action_bar,
            text="Matches",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.results_label.grid(row=0, column=0, sticky="w")

        self.export_btn = ctk.CTkButton(
            action_bar,
            text="Export to File",
            width=120,
            state="disabled",
            command=self._export_results
        )
        self.export_btn.grid(row=0, column=1, sticky="e")

        self.textbox = ctk.CTkTextbox(
            results_container,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="none",
            corner_radius=6,
            fg_color="#141418"
        )
        self.textbox.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="nsew")

    def _build_status_bar(self):
        status_frame = ctk.CTkFrame(self, fg_color="transparent", height=24)
        status_frame.grid(row=3, column=0, padx=26, pady=(0, 12), sticky="ew")
        status_frame.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        self.status_label.grid(row=0, column=0, sticky="w")

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
            messagebox.showwarning("Invalid Path", "Please select a valid file or folder path.")
            return

        if not keyword:
            messagebox.showwarning("Missing Keyword", "Please specify a search keyword.")
            return

        self.is_scanning = True
        self.scan_btn.configure(state="disabled", text="Scanning...")
        self.export_btn.configure(state="disabled")
        self.status_label.configure(text=f"Scanning target for '{keyword}'...")
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
        self.scan_btn.configure(state="normal", text="Start Scan")

        if total_hits == 0:
            self.textbox.insert("end", f"No matches found for keyword '{keyword}' across {scanned_count} scanned file(s).\n")
            self.status_label.configure(text=f"Completed: 0 matches in {scanned_count} files.")
            return

        self.export_btn.configure(state="normal")
        self.status_label.configure(text=f"Completed: {total_hits} hit(s) across {len(all_matches)} file(s) ({scanned_count} inspected).")

        display_text = []
        for filepath, entries in all_matches.items():
            display_text.append(f"--- File: {filepath} ({len(entries)} matches) ---")
            for line_no, content in entries:
                display_text.append(f"  [{line_no:>5}]  {content}")
            display_text.append("")

        self.textbox.insert("end", "\n".join(display_text))

    def _export_results(self):
        if not self.results_data:
            return

        export_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt"), ("Log File", "*.log")],
            initialfile="extracted_matches.txt"
        )
        if not export_path:
            return

        try:
            with open(export_path, "w", encoding="utf-8") as out:
                out.write("LOG FILE MINER - EXTRACTION REPORT\n")
                out.write(f"Target Keyword: {self.keyword_entry.get().strip()}\n")
                out.write("=" * 70 + "\n\n")

                for filepath, entries in self.results_data.items():
                    out.write(f"Source: {filepath}\n")
                    out.write("-" * 50 + "\n")
                    for line_no, content in entries:
                        out.write(f"Line {line_no}: {content}\n")
                    out.write("\n")

            messagebox.showinfo("Export Complete", f"Report saved to:\n{export_path}")
        except Exception as error:
            messagebox.showerror("Export Failed", f"Could not write file: {error}")

if __name__ == "__main__":
    app = LogMinerApp()
    app.mainloop()
