"""Convert Markdown files to PDF with Chinese font support using fpdf2."""
import os
import re
import sys
from fpdf import FPDF

# Strip emoji and other non-standard characters
def strip_emoji(text):
    """Remove emoji characters that may not be in the font."""
    import unicodedata
    result = []
    for ch in text:
        cat = unicodedata.category(ch)
        cp = ord(ch)
        # Keep: ASCII, CJK, common punctuation, common symbols
        if cp < 0x2000:  # Basic Latin, Latin Supplement, all common
            result.append(ch)
        elif 0x2E80 <= cp <= 0x9FFF:  # CJK
            result.append(ch)
        elif 0x3000 <= cp <= 0x303F:  # CJK Symbols and Punctuation
            result.append(ch)
        elif 0xFF00 <= cp <= 0xFFEF:  # Fullwidth forms
            result.append(ch)
        elif 0xFE30 <= cp <= 0xFE4F:  # CJK Compatibility Forms
            result.append(ch)
        elif 0x2000 <= cp <= 0x206F:  # General Punctuation
            result.append(ch)
        elif 0x2100 <= cp <= 0x214F:  # Letterlike Symbols
            result.append(ch)
        elif 0x2150 <= cp <= 0x218F:  # Number Forms
            result.append(ch)
        elif 0x2190 <= cp <= 0x21FF:  # Arrows
            result.append(ch)
        elif 0x2200 <= cp <= 0x22FF:  # Mathematical Operators
            result.append(ch)
        elif 0x2300 <= cp <= 0x23FF:  # Misc Technical
            result.append(ch)
        elif 0x2460 <= cp <= 0x24FF:  # Enclosed Alphanumerics
            result.append(ch)
        elif 0x2500 <= cp <= 0x257F:  # Box Drawing
            result.append(ch)
        elif 0x2580 <= cp <= 0x259F:  # Block Elements
            result.append(ch)
        elif 0x25A0 <= cp <= 0x25FF:  # Geometric Shapes
            result.append(ch)
        elif 0x2600 <= cp <= 0x26FF:  # Misc Symbols
            # Keep well-known ones like ☀ ☁ ☂ ☃ ☎ ☑ ☒
            # Skip potentially problematic emoji
            if cp in (0x2605, 0x2606):  # star
                result.append(ch)
            elif cp in (0x260E, 0x260F):  # phone
                result.append(ch)
            elif cp in (0x2611, 0x2612):  # ballot box
                result.append(ch)
            elif cp in (0x261C, 0x261D, 0x261E, 0x261F):  # pointing
                result.append(ch)
            elif cp in (0x263A, 0x263B, 0x2639):  # smileys
                result.append(ch)
            elif cp in (0x2660, 0x2663, 0x2665, 0x2666):  # card suits
                result.append(ch)
            elif cp in (0x266A, 0x266B, 0x266C):  # music notes
                result.append(ch)
            elif cp in (0x267B,):  # recycle
                result.append(ch)
            elif cp in (0x2702,):  # scissors
                result.append(ch)
            elif cp in (0x2713, 0x2714):  # check marks
                result.append(ch)
            elif cp in (0x2717, 0x2718):  # cross marks
                result.append(ch)
            elif cp in (0x2728,):  # sparkles
                result.append(ch)
            elif cp in (0x274C, 0x274E):  # cross marks
                result.append(ch)
            elif cp in (0x2753, 0x2754, 0x2755, 0x2757):  # question/exclamation
                result.append(ch)
            elif cp in (0x2795, 0x2796, 0x2797):  # math signs
                result.append(ch)
            elif cp in (0x27A1,):  # arrow
                result.append(ch)
            elif cp in (0x27B0,):  # loop
                result.append(ch)
            # Skip most other emoji
            # else: skip
        elif 0x2700 <= cp <= 0x27BF:  # Dingbats
            # Keep checkmarks, crosses, arrows
            if cp in (0x2702, 0x2713, 0x2714, 0x2717, 0x2718, 0x2728):
                result.append(ch)
            elif cp in (0x274C, 0x274E, 0x2753, 0x2754, 0x2755, 0x2757):
                result.append(ch)
            elif cp in (0x2795, 0x2796, 0x2797, 0x27A1, 0x27B0):
                result.append(ch)
            # else: skip
        # Skip everything else (emoji, etc.)
    return ''.join(result)

def safe_print(text):
    """Print text safely with GBK encoding."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))

FONT_DIR = r"C:\Windows\Fonts"
FONT = os.path.join(FONT_DIR, "msyh.ttc")      # Microsoft YaHei (body)
FONT_BOLD = os.path.join(FONT_DIR, "msyhbd.ttc") # Microsoft YaHei Bold
PAGE_W, PAGE_H = 210, 297  # A4
MARGIN = 20
CONTENT_W = PAGE_W - 2 * MARGIN

class MD2PDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font("zh", "", FONT)
        self.add_font("zh", "B", FONT_BOLD)
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margin(MARGIN)

    def title_page(self, title, subtitle=""):
        self.add_page()
        self.set_font("zh", "B", 24)
        self.set_y(80)
        self.multi_cell(0, 12, title, align="C")
        if subtitle:
            self.set_font("zh", "", 12)
            self.set_y(self.get_y() + 6)
            self.multi_cell(0, 8, subtitle, align="C")

    def write_heading(self, text, level):
        text = strip_emoji(text)
        sizes = {1: 18, 2: 14, 3: 12, 4: 11}
        bold = {1: True, 2: True, 3: True, 4: False}
        self.ln(4 if level > 2 else 6)
        self.set_font("zh", "B" if bold[level] else "", sizes.get(level, 11))
        # Color for levels 1-2
        if level <= 2:
            self.set_text_color(0x1a, 0x1a, 0x2e)
        else:
            self.set_text_color(0x33, 0x33, 0x33)
        self.multi_cell(0, 7, text)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def write_text(self, text):
        text = strip_emoji(text)
        self.set_font("zh", "", 10)
        # Handle inline bold (**text**)
        parts = re.split(r'(\*\*.*?\*\*)', text)
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                self.set_font("zh", "B", 10)
                self.write(5.5, part[2:-2])
                self.set_font("zh", "", 10)
            else:
                self.write(5.5, part)
        self.ln(5)

    def write_bullet(self, text, indent=5):
        text = strip_emoji(text)
        x = self.get_x()
        self.set_x(x + indent)
        self.set_font("zh", "", 10)
        self.cell(5, 5.5, "• ")
        parts = re.split(r'(\*\*.*?\*\*)', text)
        for p in parts:
            if p.startswith('**') and p.endswith('**'):
                self.set_font("zh", "B", 10)
                self.write(5.5, p[2:-2])
                self.set_font("zh", "", 10)
            else:
                self.write(5.5, p)
        self.ln(5.5)

    def write_table(self, headers, rows):
        """Draw a table with Chinese text support."""
        col_count = len(headers)
        col_w = min(CONTENT_W / col_count, 80)
        row_h = 8
        # Auto-size columns
        col_widths = []
        for i in range(col_count):
            max_w = col_w
            for row in [headers] + rows:
                txt = str(row[i]) if i < len(row) else ""
                # Estimate width: Chinese chars ~2x
                est = len(txt) * 3.5
                if est > max_w:
                    max_w = est
            col_widths.append(min(max_w, 80))
        # Scale to fit CONTENT_W
        total = sum(col_widths)
        if total > CONTENT_W:
            scale = CONTENT_W / total
            col_widths = [w * scale for w in col_widths]
        total_w = sum(col_widths)

        # Check if table fits on current page
        if self.get_y() + row_h * (len(rows) + 1) > PAGE_H - 20:
            self.add_page()

        # Draw header
        x0 = self.get_x()
        y0 = self.get_y()
        self.set_fill_color(0x1a, 0x1a, 0x2e)
        self.set_text_color(255, 255, 255)
        self.set_font("zh", "B", 8)
        x = x0
        for i, h in enumerate(headers):
            self.set_xy(x, y0)
            self.cell(col_widths[i], row_h, str(h), border=1, fill=True, align="C")
            x += col_widths[i]
        self.ln(row_h)

        # Draw rows
        self.set_text_color(0, 0, 0)
        for ri, row in enumerate(rows):
            if self.get_y() + row_h > PAGE_H - 20:
                self.add_page()
            y = self.get_y()
            self.set_font("zh", "", 8)
            fill = ri % 2 == 1
            if fill:
                self.set_fill_color(0xf5, 0xf5, 0xf5)
            x = x0
            max_y = y
            for ci in range(col_count):
                txt = str(row[ci]) if ci < len(row) else ""
                self.set_xy(x, y)
                # Use multi_cell for word wrap
                self.multi_cell(col_widths[ci], 6, txt, border=0, align="L", fill=fill)
                if self.get_y() > max_y:
                    max_y = self.get_y()
                x += col_widths[ci]
            # Draw borders
            self.set_draw_color(0xcc, 0xcc, 0xcc)
            x = x0
            for ci in range(col_count):
                txt = str(row[ci]) if ci < len(row) else ""
                self.rect(x, y, col_widths[ci], max_y - y)
                x += col_widths[ci]
            self.set_y(max_y)
        self.ln(4)

    def write_code(self, text):
        self.set_fill_color(0xf5, 0xf5, 0xf5)
        self.set_font("Courier", "", 8)
        lines = text.strip().split('\n')
        y0 = self.get_y()
        for line in lines:
            self.cell(0, 5, "", border=0)
            x = MARGIN + 5
            self.set_xy(x, self.get_y())
            # Replace Chinese chars with spaces for Courier
            safe = ''.join(c if ord(c) < 128 else ' ' for c in line)
            self.cell(CONTENT_W - 5, 5, safe)
            self.ln(5)

    def write_separator(self):
        y = self.get_y()
        self.set_draw_color(0xcc, 0xcc, 0xcc)
        self.line(MARGIN, y, PAGE_W - MARGIN, y)
        self.ln(6)


def convert_md_to_pdf(md_path, pdf_path):
    """Convert a Markdown file to PDF."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Strip emoji from content
    content = strip_emoji(content)

    pdf = MD2PDF()

    # Add page
    pdf.add_page()
    pdf.set_font("zh", "", 10)

    # Process lines
    lines = content.split('\n')
    i = 0
    in_code = False
    code_buffer = []
    in_table = False
    table_lines = []

    while i < len(lines):
        line = lines[i].strip()

        # Code block
        if line.startswith('```'):
            if in_code:
                pdf.write_code('\n'.join(code_buffer))
                code_buffer = []
                in_code = False
                i += 1
                continue
            else:
                in_code = True
                i += 1
                continue
        if in_code:
            code_buffer.append(line)
            i += 1
            continue

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Table detection
        if line.startswith('|') and line.endswith('|'):
            # Check if it's a table separator row
            if re.match(r'^[\|:\-\s]+$', line):
                i += 1
                continue
            # Collect all table rows
            table_rows = []
            while i < len(lines) and lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
                l = lines[i].strip()
                if not re.match(r'^[\|:\-\s]+$', l):
                    cells = [c.strip() for c in l.split('|')[1:-1]]
                    table_rows.append(cells)
                i += 1
            if table_rows:
                headers = table_rows[0]
                data = table_rows[1:]
                pdf.write_table(headers, data)
            continue

        # Headings
        if line.startswith('# '):
            pdf.write_heading(line[2:], 1)
            i += 1
            continue
        if line.startswith('## '):
            pdf.write_heading(line[3:], 2)
            i += 1
            continue
        if line.startswith('### '):
            pdf.write_heading(line[4:], 3)
            i += 1
            continue
        if line.startswith('#### '):
            pdf.write_heading(line[5:], 4)
            i += 1
            continue

        # Separator
        if line == '---':
            pdf.write_separator()
            i += 1
            continue

        # Blockquote
        if line.startswith('>'):
            quote_text = line[1:].strip()
            # Check for multi-line quote
            quote_lines = [quote_text]
            i += 1
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            pdf.set_fill_color(0xf0, 0xf0, 0xf8)
            pdf.set_font("zh", "", 9)
            pdf.set_x(MARGIN + 3)
            pdf.multi_cell(CONTENT_W - 3, 5.5, "\n".join(quote_lines))
            pdf.set_x(MARGIN)
            pdf.ln(3)
            continue

        # Bullet list
        if line.startswith('- ') or line.startswith('* '):
            bullet_text = line[2:].strip()
            # Handle multi-line bullets / sub-bullets
            bullet_lines = [bullet_text]
            i += 1
            while i < len(lines) and (lines[i].strip().startswith('- ') or lines[i].strip().startswith('* ') or lines[i].strip().startswith('  ') or not lines[i].strip()):
                if lines[i].strip():
                    bullet_lines.append(lines[i].strip())
                else:
                    break
                i += 1
            for bl in bullet_lines:
                pdf.write_bullet(bl)
            continue

        # Regular paragraph text
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('#') and not lines[i].strip().startswith('-') and not lines[i].strip().startswith('*') and not lines[i].strip().startswith('>') and not lines[i].strip().startswith('|') and not lines[i].strip().startswith('```') and lines[i].strip() != '---':
            para_lines.append(lines[i].strip())
            i += 1
        pdf.write_text(" ".join(para_lines))

    pdf.output(pdf_path)
    safe_print(f"+ {os.path.basename(md_path)} -> {os.path.basename(pdf_path)}  ({pdf.pages_count} pages)")


if __name__ == '__main__':
    import sys
    files = sys.argv[1:] if len(sys.argv) > 1 else []
    if not files:
        print("Usage: python md2pdf.py <file1.md> [file2.md ...]")
        sys.exit(1)
    for md_file in files:
        if not os.path.exists(md_file):
            safe_print(f"x File not found: {md_file}")
            continue
        pdf_file = os.path.splitext(md_file)[0] + ".pdf"
        try:
            convert_md_to_pdf(md_file, pdf_file)
        except Exception as e:
            safe_print(f"x Error converting {md_file}: {e}")
            import traceback
            traceback.print_exc()