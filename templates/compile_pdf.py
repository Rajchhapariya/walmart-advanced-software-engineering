"""
Unified PDF & Diagram Compiler Utility
Compiles Typst documents and HTML ERD templates into agency-grade vector PDFs and PNGs.
Usage:
    python compile_pdf.py --typst report_template.typ --out output.pdf
    python compile_pdf.py --html erd_visual_paradigm_template.html --out diagram.pdf --png diagram.png
"""

import sys
import os
import subprocess
import argparse

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

def find_chrome():
    for p in CHROME_PATHS:
        if os.path.exists(p):
            return p
    return None

def compile_typst(src_path: str, out_path: str):
    print(f"[TYPST] Compiling '{src_path}' -> '{out_path}'...")
    cmd = ["typst", "compile", src_path, out_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[SUCCESS] Typst compiled: {out_path} ({os.path.getsize(out_path)} bytes)")
    else:
        print(f"[ERROR] Typst compilation failed:\n{res.stderr}", file=sys.stderr)

def compile_html(src_path: str, out_pdf: str = None, out_png: str = None):
    chrome = find_chrome()
    if not chrome:
        print("[ERROR] Chrome not found in standard paths for headless rendering.", file=sys.stderr)
        return

    abs_src = os.path.abspath(src_path)
    file_url = f"file:///{abs_src.replace(os.sep, '/')}"

    if out_pdf:
        print(f"[CHROME] Exporting PDF '{file_url}' -> '{out_pdf}'...")
        cmd = [chrome, "--headless", "--disable-gpu", f"--print-to-pdf={out_pdf}", file_url]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if os.path.exists(out_pdf):
            print(f"[SUCCESS] PDF generated: {out_pdf} ({os.path.getsize(out_pdf)} bytes)")

    if out_png:
        print(f"[CHROME] Capturing PNG screenshot '{file_url}' -> '{out_png}'...")
        cmd = [chrome, "--headless", "--disable-gpu", "--window-size=1200,800", f"--screenshot={out_png}", file_url]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if os.path.exists(out_png):
            print(f"[SUCCESS] PNG screenshot saved: {out_png} ({os.path.getsize(out_png)} bytes)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unified PDF & Diagram Compiler")
    parser.add_argument("--typst", help="Path to .typ file")
    parser.add_argument("--html", help="Path to .html file")
    parser.add_argument("--out", help="Output PDF file path")
    parser.add_argument("--png", help="Output PNG file path (for HTML)")

    args = parser.parse_args()

    if args.typst:
        out = args.out or args.typst.replace(".typ", ".pdf")
        compile_typst(args.typst, out)
    elif args.html:
        out_pdf = args.out or args.html.replace(".html", ".pdf")
        compile_html(args.html, out_pdf=out_pdf, out_png=args.png)
    else:
        parser.print_help()
