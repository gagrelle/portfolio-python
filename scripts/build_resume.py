"""Gera a versão visual do currículo de João Gilbert Agrelle em PDF."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"
OUTPUT_FILE = OUTPUT_DIR / "Curriculo_Joao_Gilbert_Agrelle_Atualizado.pdf"

INK = HexColor("#10201B")
FOREST = HexColor("#07120F")
ACID = HexColor("#B7F34B")
MINT = HexColor("#62DDB7")
PAPER = HexColor("#F5F7F2")
MUTED = HexColor("#60716A")
LIGHT = HexColor("#D9E1DC")
RULE = HexColor("#CCD6D0")


def register_fonts() -> tuple[str, str]:
    """Usa Segoe UI quando disponível e mantém fallback portável."""
    font_dir = Path("C:/Windows/Fonts")
    regular = font_dir / "segoeui.ttf"
    semibold = font_dir / "seguisb.ttf"
    if regular.exists() and semibold.exists():
        pdfmetrics.registerFont(TTFont("ResumeRegular", regular))
        pdfmetrics.registerFont(TTFont("ResumeBold", semibold))
        return "ResumeRegular", "ResumeBold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = register_fonts()


def style(name: str, *, size: float, leading: float, color=INK, bold=False) -> ParagraphStyle:
    return ParagraphStyle(
        name,
        fontName=FONT_BOLD if bold else FONT,
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=TA_LEFT,
        allowWidows=0,
        allowOrphans=0,
    )


BODY = style("body", size=7.75, leading=10.5, color=MUTED)
BODY_DARK = style("body_dark", size=7.2, leading=10.2, color=LIGHT)
BODY_WHITE = style("body_white", size=7.5, leading=10, color=PAPER)
SMALL = style("small", size=6.35, leading=8.2, color=MUTED)
SMALL_LIGHT = style("small_light", size=6.4, leading=8.6, color=LIGHT)
COMPANY = style("company", size=6.5, leading=8, color=MUTED, bold=True)


def draw_paragraph(c: canvas.Canvas, text: str, paragraph_style: ParagraphStyle, x: float, top: float, width: float) -> float:
    paragraph = Paragraph(text, paragraph_style)
    _, paragraph_height = paragraph.wrap(width, 500)
    paragraph.drawOn(c, x, top - paragraph_height)
    return top - paragraph_height


def section_title(c: canvas.Canvas, text: str, x: float, top: float, width: float, *, light=False) -> float:
    c.setFont(FONT_BOLD, 7.1)
    c.setFillColor(ACID if light else INK)
    c.drawString(x, top - 7, text.upper())
    c.setStrokeColor(HexColor("#385047") if light else RULE)
    c.setLineWidth(0.55)
    c.line(x, top - 13, x + width, top - 13)
    return top - 22


def bullet(c: canvas.Canvas, text: str, x: float, top: float, width: float) -> float:
    c.setFillColor(ACID)
    c.circle(x + 2, top - 4.1, 1.2, fill=1, stroke=0)
    return draw_paragraph(c, text, BODY, x + 10, top, width - 10) - 3


def sidebar_bullet(c: canvas.Canvas, text: str, x: float, top: float, width: float) -> float:
    c.setFillColor(MINT)
    c.rect(x, top - 5, 3, 3, fill=1, stroke=0)
    return draw_paragraph(c, text, BODY_DARK, x + 9, top, width - 9) - 3


def draw_resume() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    page_width, page_height = A4
    c = canvas.Canvas(str(OUTPUT_FILE), pagesize=A4, pageCompression=1)
    c.setTitle("Currículo - João Gilbert Agrelle")
    c.setAuthor("João Gilbert Agrelle")
    c.setSubject("Currículo para estágio em Python, Backend e IA Generativa")
    c.setKeywords("Python, Java, Backend, Automação, IA Generativa, Estágio")

    sidebar_width = 165
    main_x = 190
    main_width = page_width - main_x - 26

    c.setFillColor(PAPER)
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)
    c.setFillColor(FOREST)
    c.rect(0, 0, sidebar_width, page_height, fill=1, stroke=0)
    c.setFillColor(ACID)
    c.rect(0, page_height - 9, sidebar_width, 9, fill=1, stroke=0)

    c.setStrokeColor(HexColor("#345047"))
    c.setLineWidth(1)
    c.circle(30 * mm, page_height - 33 * mm, 15 * mm, fill=0, stroke=1)
    c.setFillColor(ACID)
    c.setFont(FONT_BOLD, 23)
    c.drawCentredString(30 * mm, page_height - 37 * mm, "JGA")
    c.setFillColor(MINT)
    c.rect(42 * mm, page_height - 20 * mm, 3.5 * mm, 3.5 * mm, fill=1, stroke=0)

    sidebar_x = 18
    sidebar_inner_width = sidebar_width - 36
    sidebar_top = page_height - 175

    sidebar_top = section_title(c, "Contato", sidebar_x, sidebar_top, sidebar_inner_width, light=True)
    contact_style = style("contact", size=6.6, leading=10.5, color=PAPER)
    sidebar_top = draw_paragraph(c, "<b>Recife, PE</b><br/>+55 (81) 99677-5491<br/><a href='mailto:joaogilbert795@gmail.com' color='#F5F7F2'>joaogilbert795@gmail.com</a>", contact_style, sidebar_x, sidebar_top, sidebar_inner_width) - 6
    linkedin_style = style("linkedin", size=5.9, leading=8.2, color=MINT)
    sidebar_top = draw_paragraph(c, "linkedin.com/in/<br/>joao-gilbert-agrelle-990378262", linkedin_style, sidebar_x, sidebar_top, sidebar_inner_width) - 16

    sidebar_top = section_title(c, "Competências", sidebar_x, sidebar_top, sidebar_inner_width, light=True)
    for item in [
        "Python, Java e Backend",
        "HTML5 e CSS3",
        "Automação de processos",
        "Excel Avançado",
        "Google Sheets",
        "Análise e gestão de dados",
        "IA Generativa",
        "Engenharia de Prompt",
    ]:
        sidebar_top = sidebar_bullet(c, item, sidebar_x, sidebar_top, sidebar_inner_width)
    sidebar_top -= 10

    sidebar_top = section_title(c, "Diferenciais", sidebar_x, sidebar_top, sidebar_inner_width, light=True)
    sidebar_top = draw_paragraph(
        c,
        "Visão de processos<br/>Operação + tecnologia<br/>Análise e organização<br/>Aprendizado orientado a projetos",
        SMALL_LIGHT,
        sidebar_x,
        sidebar_top,
        sidebar_inner_width,
    ) - 14

    sidebar_top = section_title(c, "Objetivo", sidebar_x, sidebar_top, sidebar_inner_width, light=True)
    draw_paragraph(c, "Estágio em tecnologia com foco em <b>Python, Backend e aplicações de IA Generativa.</b>", BODY_WHITE, sidebar_x, sidebar_top, sidebar_inner_width)

    c.setFillColor(HexColor("#142A23"))
    c.setFont(FONT_BOLD, 63)
    c.drawString(19, 41, "</>")
    c.setFillColor(HexColor("#345047"))
    c.setFont(FONT, 5.6)
    c.drawString(20, 28, "PROCESSOS  /  DADOS  /  C\u00d3DIGO")


    top = page_height - 48
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 25)
    c.drawString(main_x, top, "João Gilbert Agrelle")
    top -= 22
    c.setFillColor(HexColor("#3B554A"))
    c.setFont(FONT_BOLD, 8.1)
    c.drawString(main_x, top, "DESENVOLVEDOR PYTHON EM FORMAÇÃO")
    c.setFillColor(ACID)
    c.rect(main_x, top - 12, 52, 3, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont(FONT, 6.4)
    c.drawString(main_x + 61, top - 12, "BACKEND  /  AUTOMAÇÃO  /  IA GENERATIVA")
    top -= 35

    top = section_title(c, "Resumo profissional", main_x, top, main_width)
    summary = (
        "Estudante de <b>Análise e Desenvolvimento de Sistemas</b>, com formação técnica em Desenvolvimento de Sistemas e experiência em ambientes operacionais. "
        "Aplica controles e análise para reduzir trabalho manual, investigar divergências e melhorar processos. Desenvolve projetos em Python e web, unindo visão prática, dados e tecnologia."
    )
    top = draw_paragraph(c, summary, BODY, main_x, top, main_width) - 15

    top = section_title(c, "Experiência profissional", main_x, top, main_width)
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 9.1)
    c.drawString(main_x, top - 1, "Estagiário em Análise de Estoque")
    c.setFillColor(ACID)
    c.roundRect(page_width - 91, top - 7, 65, 14, 3, fill=1, stroke=0)
    c.setFillColor(FOREST)
    c.setFont(FONT_BOLD, 5.8)
    c.drawCentredString(page_width - 58.5, top - 2.3, "AGO 2025 - ATUAL")
    top -= 14
    top = draw_paragraph(c, "VULP AIR  |  Jaboatão dos Guararapes, PE", COMPANY, main_x, top, main_width) - 4
    top = bullet(c, "Gerencia informações de estoque, conciliando registros físicos e digitais e analisando divergências.", main_x, top, main_width)
    top = bullet(c, "Desenvolve controles, fórmulas e pequenas automações para reduzir tarefas manuais e aumentar a confiabilidade das informações.", main_x, top, main_width)
    top = bullet(c, "Estrutura processos e identifica oportunidades de melhoria contínua na operação.", main_x, top, main_width) - 8

    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 9.1)
    c.drawString(main_x, top - 1, "Estagiário em Departamento Pessoal")
    c.setFillColor(HexColor("#E2E8E3"))
    c.roundRect(page_width - 95, top - 7, 69, 14, 3, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont(FONT_BOLD, 5.8)
    c.drawCentredString(page_width - 60.5, top - 2.3, "MAR 2023 - DEZ 2023")
    top -= 14
    top = draw_paragraph(c, "CW CONSULTORES  |  Pernambuco, Brasil", COMPANY, main_x, top, main_width) - 4
    top = bullet(c, "Apoiou admissões, desligamentos, eSocial, conferência documental e organização de prontuários digitais.", main_x, top, main_width)
    top = bullet(c, "Coletou e validou dados para relatórios e conferiu folha, ponto eletrônico e faturas de benefícios.", main_x, top, main_width) - 12

    top = section_title(c, "Projetos selecionados", main_x, top, main_width)
    projects = [
        ("Dashboard em Python", "Painel para organizar e visualizar informações, apoiando análises e decisões.", "PYTHON / DADOS"),
        ("Controle de Devoluções", "Projeto web para estruturar o fluxo e acompanhar devoluções de materiais.", "HTML / CSS"),
        ("Landing Pages", "Interfaces para projetos próprios e iniciativas comerciais.", "WEB / UI"),
    ]
    card_gap = 7
    card_width = (main_width - 2 * card_gap) / 3
    card_height = 67
    for index, (title, description, tag) in enumerate(projects):
        x = main_x + index * (card_width + card_gap)
        c.setFillColor(colors.white)
        c.setStrokeColor(RULE)
        c.roundRect(x, top - card_height, card_width, card_height, 5, fill=1, stroke=1)
        c.setFillColor(ACID)
        c.roundRect(x + 8, top - 14, 39, 10, 2, fill=1, stroke=0)
        c.setFillColor(FOREST)
        c.setFont(FONT_BOLD, 4.8)
        c.drawCentredString(x + 27.5, top - 10.5, tag)
        c.setFillColor(INK)
        c.setFont(FONT_BOLD, 7.2)
        c.drawString(x + 8, top - 27, title)
        draw_paragraph(c, description, SMALL, x + 8, top - 34, card_width - 16)
    top -= card_height + 16

    top = section_title(c, "Formação e certificações", main_x, top, main_width)
    column_gap = 22
    column_width = (main_width - column_gap) / 2
    left = (
        "<b>UNINASSAU</b><br/>CST em Análise e Desenvolvimento de Sistemas<br/>"
        "<font color='#60716A'>Ago 2026 - Dez 2028 (previsão)</font><br/><br/>"
        "<b>ETE Porto Digital</b><br/>Técnico em Desenvolvimento de Sistemas<br/>"
        "<font color='#60716A'>Fev 2020 - Dez 2022</font>"
    )
    right = "<b>CURSOS E CERTIFICAÇÕES</b><br/>Engenharia de Prompt<br/>Excel Avançado - Udemy<br/>Google Sheets - Udemy"
    education_left_bottom = draw_paragraph(c, left, SMALL, main_x, top, column_width)
    education_right_bottom = draw_paragraph(c, right, SMALL, main_x + column_width + column_gap, top, column_width)

    top = min(education_left_bottom, education_right_bottom) - 20
    top = section_title(c, "Forma de trabalhar", main_x, top, main_width)
    work_items = [
        ("01  ANALISAR", "Entender o processo e investigar diverg\u00eancias."),
        ("02  ESTRUTURAR", "Organizar dados, controles e informa\u00e7\u00f5es."),
        ("03  MELHORAR", "Aplicar tecnologia para reduzir trabalho manual."),
    ]
    work_gap = 7
    work_width = (main_width - 2 * work_gap) / 3
    work_height = 72
    for index, (label, description) in enumerate(work_items):
        x = main_x + index * (work_width + work_gap)
        c.setFillColor(HexColor("#E9EFEA"))
        c.roundRect(x, top - work_height, work_width, work_height, 5, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont(FONT_BOLD, 6.2)
        c.drawString(x + 9, top - 16, label)
        c.setFillColor(ACID)
        c.rect(x + 9, top - 26, 22, 2.5, fill=1, stroke=0)
        draw_paragraph(c, description, SMALL, x + 9, top - 35, work_width - 18)

    c.setStrokeColor(RULE)
    c.line(main_x, 26, page_width - 26, 26)
    c.setFillColor(MUTED)
    c.setFont(FONT, 5.5)
    c.drawString(main_x, 16, "Portfólio desenvolvido em Python e Flask")
    c.drawRightString(page_width - 26, 16, "Recife, PE  |  2026")

    c.showPage()
    c.save()
    return OUTPUT_FILE


if __name__ == "__main__":
    print(draw_resume())
