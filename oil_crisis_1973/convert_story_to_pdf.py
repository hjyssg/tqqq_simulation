from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import re

def convert_story_to_pdf():
    """将叙事性Markdown文章转换为PDF"""
    
    # 文件路径
    md_file = os.path.join(os.path.dirname(__file__), "石油危机往事：当中东的战火烧到华尔街.md")
    pdf_file = os.path.join(os.path.dirname(__file__), "石油危机往事：当中东的战火烧到华尔街.pdf")
    image_file = os.path.join(os.path.dirname(__file__), "output/oil_spx_dual_axis_1972_1974.png")
    
    # 注册中文字体
    try:
        # 尝试使用微软雅黑
        font_path = "C:\\Windows\\Fonts\\msyh.ttc"
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
            chinese_font = 'ChineseFont'
        else:
            # 尝试使用SimHei
            font_path = "C:\\Windows\\Fonts\\simhei.ttf"
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                chinese_font = 'ChineseFont'
            else:
                print("警告: 未找到中文字体，可能显示乱码")
                chinese_font = 'Helvetica'
    except Exception as e:
        print(f"字体注册失败: {e}")
        chinese_font = 'Helvetica'
    
    # 读取Markdown文件
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建PDF文档
    doc = SimpleDocTemplate(pdf_file, pagesize=A4,
                           rightMargin=2.5*cm, leftMargin=2.5*cm,
                           topMargin=2*cm, bottomMargin=2*cm)
    
    # 内容列表
    story = []
    
    # 样式
    styles = getSampleStyleSheet()
    
    # 标题样式
    title_style = ParagraphStyle(
        'StoryTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=HexColor('#1a1a1a'),
        spaceAfter=40,
        spaceBefore=20,
        alignment=TA_CENTER,
        leading=28,
        fontName=chinese_font
    )
    
    # 一级标题
    h2_style = ParagraphStyle(
        'StoryH2',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=HexColor('#2c3e50'),
        spaceAfter=15,
        spaceBefore=25,
        leading=22,
        fontName=chinese_font
    )
    
    # 二级标题
    h3_style = ParagraphStyle(
        'StoryH3',
        parent=styles['Heading3'],
        fontSize=13,
        textColor=HexColor('#34495e'),
        spaceAfter=12,
        spaceBefore=18,
        leading=18,
        fontName=chinese_font
    )
    
    # 正文样式 - 两端对齐，更适合阅读
    body_style = ParagraphStyle(
        'StoryBody',
        parent=styles['BodyText'],
        fontSize=11,
        leading=18,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        firstLineIndent=0,
        fontName=chinese_font
    )
    
    # 引用样式
    quote_style = ParagraphStyle(
        'Quote',
        parent=body_style,
        fontSize=10,
        textColor=HexColor('#555555'),
        leftIndent=20,
        rightIndent=20,
        spaceAfter=15,
        spaceBefore=15,
        leading=16,
        fontName=chinese_font
    )
    
    # 列表样式
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=20,
        spaceAfter=8,
        bulletIndent=10,
        fontName=chinese_font
    )
    
    # 解析Markdown内容
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # 跳过空行
        if not line:
            i += 1
            continue
        
        # 主标题 (# 开头)
        if line.startswith('# '):
            title_text = line[2:].strip()
            story.append(Paragraph(title_text, title_style))
            story.append(Spacer(1, 0.3*cm))
        
        # 二级标题 (## 开头)
        elif line.startswith('## '):
            h2_text = line[3:].strip()
            story.append(Paragraph(h2_text, h2_style))
        
        # 三级标题 (### 开头)
        elif line.startswith('### '):
            h3_text = line[4:].strip()
            story.append(Paragraph(h3_text, h3_style))
        
        # 图片
        elif line.startswith('!['):
            # 提取图片路径
            match = re.search(r'\!\[.*?\]\((.*?)\)', line)
            if match and os.path.exists(image_file):
                img = Image(image_file, width=15*cm, height=9*cm)
                story.append(Spacer(1, 0.3*cm))
                story.append(img)
        
        # 图片说明
        elif line.startswith('*图：'):
            caption = line.strip('*')
            story.append(Paragraph(f'<i>{caption}</i>', quote_style))
            story.append(Spacer(1, 0.3*cm))
        
        # 列表项
        elif line.startswith('- '):
            bullet_text = line[2:].strip()
            # 处理加粗
            bullet_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', bullet_text)
            story.append(Paragraph(f'• {bullet_text}', bullet_style))
        
        # 分隔线
        elif line.startswith('---'):
            story.append(Spacer(1, 0.5*cm))
        
        # 普通段落
        else:
            # 处理加粗 **text**
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            # 处理斜体 *text*
            line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', line)
            
            story.append(Paragraph(line, body_style))
        
        i += 1
    
    # 生成PDF
    print("正在生成叙事性文章PDF...")
    doc.build(story)
    print(f"PDF文件已生成: {pdf_file}")

if __name__ == "__main__":
    try:
        convert_story_to_pdf()
    except Exception as e:
        print(f"转换失败: {e}")
        import traceback
        traceback.print_exc()
