#!/usr/bin/env python3
"""Export the Vietnamese Markdown report to a readable PDF with embedded fonts.

Install python3-reportlab, then run this script. The PDF remains a draft until
the student fills personal details, links and the missing assignment questions.
"""
import re
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether


ROOT = Path(__file__).resolve().parents[1]
pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuBold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DejaVu', normal='DejaVu', bold='DejaVuBold', italic='DejaVu', boldItalic='DejaVuBold')
styles = getSampleStyleSheet()
for key in styles.byName:
    styles[key].fontName = 'DejaVu'
styles['Normal'].fontSize = 9
styles['Normal'].leading = 13
styles['Normal'].spaceAfter = 5
styles['Title'].fontName = 'DejaVuBold'
styles['Title'].fontSize = 16
styles['Title'].leading = 21
styles['Heading2'].fontName = 'DejaVuBold'
styles['Heading2'].fontSize = 11
styles['Heading2'].leading = 16
small = ParagraphStyle('TableCell', parent=styles['Normal'], fontSize=7.5, leading=10, spaceAfter=0)


def inline(text):
    text = escape(text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'`([^`]+)`', r'<font color="#215080">\1</font>', text)
    text = re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)', r'<link href="\2" color="#215080">\1</link>', text)
    text = re.sub(r'\[([^]]+)\]\(([^)]+)\)', r'\1', text)
    return text


def parse(path):
    lines=path.read_text().splitlines(); output=[]; paragraph=[]; i=0
    def flush():
        if paragraph:
            output.append(Paragraph(inline(' '.join(paragraph)), styles['Normal']));paragraph.clear()
    while i < len(lines):
        line=lines[i]
        if line.startswith('|'):
            flush(); rows=[]
            while i < len(lines) and lines[i].startswith('|'):
                cells=[c.strip() for c in lines[i].strip('|').split('|')]
                if not all(re.fullmatch(r'[:\- ]+',c) for c in cells):
                    rows.append([Paragraph(inline(c),small) for c in cells])
                i+=1
            table=Table(rows,repeatRows=1,hAlign='LEFT',colWidths=[(A4[0]-80)/len(rows[0])]*len(rows[0]))
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E8EDF3')),
                ('GRID',(0,0),(-1,-1),.3,colors.HexColor('#BBBBBB')),('VALIGN',(0,0),(-1,-1),'TOP'),
                ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
            output.extend([table,Spacer(1,8)]);continue
        if line.startswith('# '):flush();output.append(Paragraph(inline(line[2:]),styles['Title']))
        elif line.startswith('## '):flush();output.append(Paragraph(inline(line[3:]),styles['Heading2']))
        elif line.startswith('- '):
            flush();paragraph.append('• '+line[2:])
        elif not line.strip():flush()
        else:paragraph.append(line.strip())
        i+=1
    flush()
    return output


def footer(canvas, doc):
    canvas.setFont('DejaVu',7)
    canvas.drawString(40,24,'TurtleBot 4 • Báo cáo nháp: cần hoàn thiện bằng chứng và link nộp bài')
    canvas.drawRightString(A4[0]-40,24,str(doc.page))


def main():
    output = ROOT/'docs/REPORT_DRAFT.pdf'
    content=parse(ROOT/'docs/REPORT.md')
    validation=ROOT/'artifacts/VALIDATION.md'
    if validation.exists():
        content.append(Paragraph('Phụ lục: kiểm chứng thực tế',styles['Heading2']))
        content.extend(parse(validation))
    image_path=ROOT/'artifacts/map_preview.png'
    if image_path.exists():
        from PIL import Image as PILImage
        w,h=PILImage.open(image_path).size
        content.append(KeepTogether([
            Paragraph('Occupancy map và đường đi Nav2 trong lần kiểm thử',styles['Heading2']),
            Image(str(image_path),width=340,height=340*h/w),
        ]))
    SimpleDocTemplate(str(output),pagesize=A4,leftMargin=40,rightMargin=40,topMargin=35,bottomMargin=40,
                      title='TurtleBot 4 — SLAM, AMCL và Nav2 (bản nháp)').build(content,onFirstPage=footer,onLaterPages=footer)
    print(output)


if __name__=='__main__':main()
