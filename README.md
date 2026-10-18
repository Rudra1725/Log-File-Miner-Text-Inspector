<div align="center">

# 🔍 Log File Miner & Text Inspector

An automated, high-performance log inspection and keyword extraction tool built with Python and CustomTkinter. Quickly parse single logs or traverse entire directory trees to isolate errors, track exact line occurrences, and export structured audit reports.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blue?style=for-the-badge)
![Threading](https://img.shields.io/badge/Engine-Multithreaded-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

---

## ⚡ Key Highlights

- **Dual Inspection Modes**: Target individual `.log`/`.txt` files or perform recursive scans across deeply nested project directories.
- **Asynchronous Worker Threading**: UI never hangs or freezes during heavy scans on large log files.
- **Precision Matching**: Supports both case-insensitive searches and exact case-matching logic.
- **Clean Monospace Audit View**: Outputs structured results indexed with right-aligned line numbers and clear source indicators.
- **One-Click Export**: Save filtered results directly to clean `.txt` or `.log` reports with metadata headers.

---

## 🛠️ Tech Stack & Concepts

- **Language**: Python 3.8+
- **GUI Engine**: CustomTkinter
- **File I/O**: Native `open()` streaming, UTF-8 character fallback parsing
- **Directory Walking**: Recursive `os.walk()` path normalization
- **Concurrency**: `threading.Thread` with daemon workers to ensure responsive event loops

---

## 🚀 Quick Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/log-file-miner.git](https://github.com/your-username/log-file-miner.git)
cd log-file-miner
