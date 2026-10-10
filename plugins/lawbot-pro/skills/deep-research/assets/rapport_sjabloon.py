# -*- coding: utf-8 -*-
"""
rapport_sjabloon.py - LawBot Pro-rapportsjabloon voor deep research (ReportLab, geen internet nodig).

Gebruik in de code-tool van de agent:

    import sys; sys.path.insert(0, "/pad/naar/deep-research/assets")
    from rapport_sjabloon import maak_rapport
    info = maak_rapport(spec, "rapport.pdf")        # info: pagina's, fontbron, logo's, waarschuwingen

Is het bestand niet importeerbaar, plak dan de inhoud in de code-tool en roep
maak_rapport(spec, pad, assets_dir="/pad/naar/assets") aan. Ontbreken fonts of logo's op die plek, dan
probeert de sjabloon ze één keer op te halen uit de publieke LawBot Pro-marketplace op GitHub (alleen als
er netwerk is; uit te zetten met download=False) en bewaart ze in een cachemap. Lukt ook dat niet, dan
valt hij terug op DejaVu of de ingebouwde fonts en een getekend woordmerk; opbouw en kleuren blijven gelijk.

De spec is een dict (zie VOORBEELD onderaan). Tekst mag een kleine markdown-subset bevatten:
**vet**, *cursief*, [tekst](url), [n] voor een nootverwijzing, en de tags <b> <i> <a href> <sup>.
"""
import os
import re
import datetime
import shutil
import urllib.request
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib import utils as rl_utils
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, NextPageTemplate, KeepTogether, Flowable,
                                CondPageBreak, Image)
from reportlab.platypus.tableofcontents import TableOfContents

SJABLOON_VERSIE = "2.1 (2026-10-10)"
ASSETS_URL = "https://raw.githubusercontent.com/anthonyloeff/lawbot-pro-marketplace/main/plugins/lawbot-pro/skills/deep-research/assets/"
ASSET_BESTANDEN = ["fonts/PlusJakartaSans-Regular.ttf", "fonts/PlusJakartaSans-SemiBold.ttf", "fonts/PlusJakartaSans-Bold.ttf",
                   "fonts/PlusJakartaSans-Italic.ttf", "fonts/SourceSerif4-Regular.ttf", "fonts/SourceSerif4-It.ttf",
                   "fonts/SourceSerif4-Semibold.ttf", "fonts/SourceSerif4-Bold.ttf", "logo-lawbot.png", "logo-litic-light.png", "logo-litic-dark.png"]


def assets_compleet(d):
    d = Path(d)
    return all((d / b).exists() for b in ASSET_BESTANDEN)


def haal_assets_op(doel=None, basis_url=ASSETS_URL, timeout=20):
    """Haalt fonts en logo's op uit de publieke marketplace (alleen wat ontbreekt). Geeft de map terug, of None
    als het netwerk ontbreekt. Gebruikt een cachemap onder HOME zodat het per machine één keer gebeurt."""
    doel = Path(doel) if doel else Path(os.environ.get("LAWBOT_ASSETS_CACHE") or Path.home() / ".cache" / "lawbot-pro" / "deep-research-assets")
    try:
        (doel / "fonts").mkdir(parents=True, exist_ok=True)
        for b in ASSET_BESTANDEN:
            pad = doel / b
            if pad.exists() and pad.stat().st_size > 0:
                continue
            with urllib.request.urlopen(basis_url + b, timeout=timeout) as r, open(pad, "wb") as f:
                shutil.copyfileobj(r, f)
        return doel if assets_compleet(doel) else None
    except Exception:
        return None

# ── Ontwerpsysteem: tokens (stijlgids.md) ───────────────────────────────────────────────────────
K = {
    "papier": HexColor("#f5f0e8"), "kaart": HexColor("#fdfbf7"), "inkt": HexColor("#54483f"),
    "inkt_zacht": HexColor("#6f6155"), "lijn": HexColor("#ddd5c9"), "lijn_zacht": HexColor("#e9e2d6"),
    "salie": HexColor("#9b9a86"), "groen": HexColor("#5f6f62"), "groen_donker": HexColor("#4c5a50"),
    "groen_tint": HexColor("#eaece7"), "oker": HexColor("#b07d1e"), "oker_donker": HexColor("#8a6217"),
    "oker_tint": HexColor("#f2e7cd"), "fout": HexColor("#a4453b"), "grijs_tint": HexColor("#ebe8e2"),
    "cover_tekst": HexColor("#f5f0e8"), "cover_zacht": HexColor("#c9cfc4"), "wit": white,
}
STATUSSEN = {
    "officieel": ("officieel", K["groen_tint"], K["groen_donker"]),
    "web": ("web, geciteerd", K["oker_tint"], K["oker_donker"]),
    "niet_gevonden": ("niet gevonden", K["fout"], K["wit"]),
    "niet_open": ("niet open toegankelijk", K["grijs_tint"], K["inkt_zacht"]),
}
MAANDEN = ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september",
           "oktober", "november", "december"]
PAGINA_B, PAGINA_H = A4
MARGE = 22 * mm
LEESBREEDTE = PAGINA_B - 2 * MARGE


def datum_nl(s):
    """'2026-10-10' -> '10 oktober 2026'; andere tekst blijft staan."""
    if not s:
        return ""
    try:
        d = datetime.date.fromisoformat(str(s)[:10])
        return f"{d.day} {MAANDEN[d.month - 1]} {d.year}"
    except ValueError:
        return str(s)


def status_sleutel(s):
    s = (s or "").strip().lower()
    if s.startswith("officieel"):
        return "officieel"
    if s.startswith("web"):
        return "web"
    if "niet open" in s or "toegank" in s or "login" in s or "paywall" in s or "betaalmuur" in s:
        return "niet_open"
    if "niet gevonden" in s or s.startswith("niet"):
        return "niet_gevonden"
    return "niet_open"


# ── Fonts ────────────────────────────────────────────────────────────────────────────────────────
def _probeer_ttf(naam, pad):
    try:
        pdfmetrics.registerFont(TTFont(naam, str(pad)))
        return True
    except Exception:
        return False


def laad_fonts(assets_dir):
    """Registreert de huisstijlfonts; valt terug op DejaVu en daarna op de ingebouwde fonts.
    Geeft (fontmap, bron) terug; bron in {'huisstijl', 'dejavu', 'ingebouwd'}."""
    fd = Path(assets_dir) / "fonts"
    huisstijl = {
        "serif": ("SourceSerif4", "SourceSerif4-Regular.ttf"), "serif_it": ("SourceSerif4-It", "SourceSerif4-It.ttf"),
        "serif_sb": ("SourceSerif4-Semibold", "SourceSerif4-Semibold.ttf"), "serif_b": ("SourceSerif4-Bold", "SourceSerif4-Bold.ttf"),
        "sans": ("PlusJakartaSans", "PlusJakartaSans-Regular.ttf"), "sans_sb": ("PlusJakartaSans-SemiBold", "PlusJakartaSans-SemiBold.ttf"),
        "sans_b": ("PlusJakartaSans-Bold", "PlusJakartaSans-Bold.ttf"), "sans_it": ("PlusJakartaSans-Italic", "PlusJakartaSans-Italic.ttf"),
    }
    if all(_probeer_ttf(n, fd / f) for n, f in huisstijl.values()):
        F = {k: v[0] for k, v in huisstijl.items()}
        pdfmetrics.registerFontFamily("SourceSerif4", normal=F["serif"], bold=F["serif_sb"], italic=F["serif_it"], boldItalic=F["serif_b"])
        pdfmetrics.registerFontFamily("PlusJakartaSans", normal=F["sans"], bold=F["sans_sb"], italic=F["sans_it"], boldItalic=F["sans_b"])
        return F, "huisstijl"
    zoekpaden = [Path(p) for p in ["/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/dejavu", "/usr/share/fonts/TTF",
                                   "/usr/local/share/fonts", "/Library/Fonts", Path.home() / "Library/Fonts", "/System/Library/Fonts/Supplemental"]]
    dejavu = {"serif": "DejaVuSerif.ttf", "serif_it": "DejaVuSerif-Italic.ttf", "serif_sb": "DejaVuSerif-Bold.ttf", "serif_b": "DejaVuSerif-Bold.ttf",
              "sans": "DejaVuSans.ttf", "sans_sb": "DejaVuSans-Bold.ttf", "sans_b": "DejaVuSans-Bold.ttf", "sans_it": "DejaVuSans-Oblique.ttf"}
    F = {}
    for k, bestand in dejavu.items():
        naam = bestand[:-4]
        if naam in pdfmetrics.getRegisteredFontNames():
            F[k] = naam
            continue
        for zp in zoekpaden:
            if (zp / bestand).exists() and _probeer_ttf(naam, zp / bestand):
                F[k] = naam
                break
    if len(F) == len(dejavu):
        pdfmetrics.registerFontFamily("DejaVuSerif", normal=F["serif"], bold=F["serif_sb"], italic=F["serif_it"], boldItalic=F["serif_b"])
        pdfmetrics.registerFontFamily("DejaVuSans", normal=F["sans"], bold=F["sans_sb"], italic=F["sans_it"], boldItalic=F["sans_b"])
        return F, "dejavu"
    return {"serif": "Times-Roman", "serif_it": "Times-Italic", "serif_sb": "Times-Bold", "serif_b": "Times-Bold",
            "sans": "Helvetica", "sans_sb": "Helvetica-Bold", "sans_b": "Helvetica-Bold", "sans_it": "Helvetica-Oblique"}, "ingebouwd"


# ── Tekst: kleine markdown-subset naar ReportLab-markup ─────────────────────────────────────────
_TAGS = r"(?:/?(?:b|i|u|a|sup|super|sub|font|br)\b)"


def par(tekst, link_kleur="#5f6f62"):
    """Maakt vrije tekst veilig voor Paragraph en vertaalt **vet**, *cursief*, [tekst](url) en [n]."""
    if tekst is None:
        return ""
    t = str(tekst).replace("\r", "").strip()
    t = re.sub(r"&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)", "&amp;", t)
    t = re.sub(r"<(?!%s)" % _TAGS, "&lt;", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", lambda m: f'<a href="{m.group(2)}" color="{link_kleur}">{m.group(1)}</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    t = re.sub(r"\s*\[(\d{1,3})\]", r'<super><font size="6.5" color="#5f6f62">\1</font></super>', t)
    t = t.replace("\n\n", "<br/><br/>").replace("\n", " ")
    return t


# ── Stijlen ──────────────────────────────────────────────────────────────────────────────────────
def maak_stijlen(F):
    S = {}
    S["tekst"] = ParagraphStyle("tekst", fontName=F["serif"], fontSize=10.5, leading=15, textColor=K["inkt"],
                                spaceAfter=6, alignment=TA_LEFT, splitLongWords=1)
    S["tekst_klein"] = ParagraphStyle("tekst_klein", parent=S["tekst"], fontSize=9.5, leading=13.5)
    S["lijst"] = ParagraphStyle("lijst", parent=S["tekst"], leftIndent=6 * mm, bulletIndent=1 * mm, spaceAfter=3)
    S["kop1"] = ParagraphStyle("kop1", fontName=F["serif_sb"], fontSize=18, leading=22, textColor=K["groen_donker"],
                               spaceBefore=2, spaceAfter=8, keepWithNext=1)
    S["kop2"] = ParagraphStyle("kop2", fontName=F["sans_sb"], fontSize=11.5, leading=15, textColor=K["groen_donker"],
                               spaceBefore=10, spaceAfter=4, keepWithNext=1)
    S["kop3"] = ParagraphStyle("kop3", fontName=F["sans_sb"], fontSize=9.5, leading=13, textColor=K["inkt_zacht"],
                               spaceBefore=6, spaceAfter=2, keepWithNext=1)
    S["ondertitel"] = ParagraphStyle("ondertitel", fontName=F["serif_it"], fontSize=12, leading=16, textColor=K["inkt_zacht"], spaceAfter=10)
    S["citaat"] = ParagraphStyle("citaat", fontName=F["serif_it"], fontSize=10, leading=14.5, textColor=K["inkt"], spaceAfter=2)
    S["citaat_bron"] = ParagraphStyle("citaat_bron", fontName=F["sans"], fontSize=7.5, leading=10, textColor=K["inkt_zacht"])
    S["tabel"] = ParagraphStyle("tabel", fontName=F["sans"], fontSize=8.8, leading=11.5, textColor=K["inkt"], splitLongWords=1)
    S["tabel_r"] = ParagraphStyle("tabel_r", parent=S["tabel"], alignment=TA_RIGHT)
    S["tabel_c"] = ParagraphStyle("tabel_c", parent=S["tabel"], alignment=TA_CENTER)
    S["tabel_kop"] = ParagraphStyle("tabel_kop", fontName=F["sans_sb"], fontSize=7.5, leading=10, textColor=K["inkt_zacht"])
    S["tabel_kop_r"] = ParagraphStyle("tabel_kop_r", parent=S["tabel_kop"], alignment=TA_RIGHT)
    S["tabel_kop_c"] = ParagraphStyle("tabel_kop_c", parent=S["tabel_kop"], alignment=TA_CENTER)
    S["bijschrift"] = ParagraphStyle("bijschrift", fontName=F["sans"], fontSize=7.5, leading=10, textColor=K["inkt_zacht"], spaceBefore=3, spaceAfter=8)
    S["noot"] = ParagraphStyle("noot", fontName=F["sans"], fontSize=8, leading=10.5, textColor=K["inkt_zacht"], leftIndent=5 * mm,
                               firstLineIndent=-5 * mm, spaceAfter=1.5)
    S["colofon_label"] = ParagraphStyle("colofon_label", fontName=F["sans_sb"], fontSize=7.5, leading=10, textColor=K["inkt_zacht"])
    S["colofon"] = ParagraphStyle("colofon", fontName=F["sans"], fontSize=8, leading=11, textColor=K["inkt"])
    S["kader_tekst"] = ParagraphStyle("kader_tekst", fontName=F["serif"], fontSize=10, leading=14, textColor=K["inkt"])
    S["bron_titel"] = ParagraphStyle("bron_titel", fontName=F["sans_sb"], fontSize=8.8, leading=11.5, textColor=K["inkt"], splitLongWords=1)
    S["bron_meta"] = ParagraphStyle("bron_meta", fontName=F["sans"], fontSize=7.5, leading=10, textColor=K["inkt_zacht"], splitLongWords=1)
    S["bron_toelichting"] = ParagraphStyle("bron_toelichting", fontName=F["serif_it"], fontSize=8.8, leading=11.5, textColor=K["inkt"], spaceBefore=1.5)
    S["toc0"] = ParagraphStyle("toc0", fontName=F["serif"], fontSize=10.5, leading=16, textColor=K["inkt"])
    S["toc1"] = ParagraphStyle("toc1", fontName=F["sans"], fontSize=8.8, leading=13, textColor=K["inkt_zacht"], leftIndent=7 * mm)
    S["cover_titel"] = ParagraphStyle("cover_titel", fontName=F["serif_sb"], fontSize=28, leading=34, textColor=K["cover_tekst"])
    S["cover_ondertitel"] = ParagraphStyle("cover_ondertitel", fontName=F["serif_it"], fontSize=13, leading=18, textColor=K["cover_zacht"])
    S["cover_meta"] = ParagraphStyle("cover_meta", fontName=F["sans"], fontSize=8, leading=13, textColor=K["cover_zacht"])
    return S


# ── Eigen flowables ──────────────────────────────────────────────────────────────────────────────
class Kaderlabel(Flowable):
    """Eén regel kapitalen met letterspatiëring (sectienummer, kaderkop)."""

    def __init__(self, tekst, font, kleur=None, size=7.5, spatie=1.1, ruimte_onder=3, kleur_nummer=None):
        super().__init__()
        self.tekst, self.font, self.size, self.spatie = str(tekst).upper(), font, size, spatie
        self.kleur = kleur or K["oker"]
        self.ruimte_onder = ruimte_onder
        self.keepWithNext = 1

    def wrap(self, aw, ah):
        self.w = pdfmetrics.stringWidth(self.tekst, self.font, self.size) + self.spatie * len(self.tekst)
        self.h = self.size * 1.3 + self.ruimte_onder
        return min(self.w, aw), self.h

    def draw(self):
        t = self.canv.beginText(0, self.ruimte_onder + self.size * 0.3)
        t.setFont(self.font, self.size)
        t.setCharSpace(self.spatie)
        t.setFillColor(self.kleur)
        t.textOut(self.tekst)
        t.setCharSpace(0)
        self.canv.drawText(t)


class Badge(Flowable):
    """Afgeronde statuspil."""

    def __init__(self, status, font, size=7.3):
        super().__init__()
        self.label, self.bg, self.fg = STATUSSEN[status_sleutel(status)]
        self.font, self.size = font, size

    def wrap(self, aw, ah):
        self.w = pdfmetrics.stringWidth(self.label, self.font, self.size) + 9
        self.h = self.size + 6.5
        return self.w, self.h

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.roundRect(0, 0, self.w, self.h, self.h / 2, stroke=0, fill=1)
        c.setFillColor(self.fg)
        c.setFont(self.font, self.size)
        c.drawCentredString(self.w / 2, (self.h - self.size) / 2 + 1.1, self.label)


class Haarlijn(Flowable):
    def __init__(self, breedte=None, kleur=None, dikte=0.5, boven=4, onder=6):
        super().__init__()
        self.breedte, self.kleur, self.dikte, self.boven, self.onder = breedte, kleur or K["lijn"], dikte, boven, onder

    def wrap(self, aw, ah):
        self.w = self.breedte or aw
        return self.w, self.boven + self.onder + self.dikte

    def draw(self):
        self.canv.setStrokeColor(self.kleur)
        self.canv.setLineWidth(self.dikte)
        self.canv.line(0, self.onder, self.w, self.onder)


class Citaat(Flowable):
    """Citaat met een oker-streep links; splitst mee over pagina's."""

    def __init__(self, alinea, inspringing=8 * mm):
        super().__init__()
        self.p, self.ins = alinea, inspringing

    def wrap(self, aw, ah):
        self.pw, self.ph = self.p.wrap(aw - self.ins, ah)
        self.w, self.h = aw, self.ph
        return self.w, self.h

    def split(self, aw, ah):
        delen = self.p.split(aw - self.ins, ah)
        if len(delen) < 2:
            return []
        return [Citaat(d, self.ins) for d in delen]

    def draw(self):
        c = self.canv
        c.setStrokeColor(K["oker"])
        c.setLineWidth(1.4)
        c.line(1, 0, 1, self.h)
        self.p.drawOn(c, self.ins, 0)


class Logo(Image):
    """Afbeelding met bewaarde verhouding op een opgegeven breedte."""

    def __init__(self, pad, breedte):
        b, h = rl_utils.ImageReader(str(pad)).getSize()
        super().__init__(str(pad), width=breedte, height=breedte * h / b)


# ── Canvas met 'pagina / totaal' en kop- en voetregels ───────────────────────────────────────────
class GenummerdCanvas(rl_canvas.Canvas):
    teken_voet = None  # wordt bij build gezet: functie(canvas, pagina, totaal)

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._staten = []

    def showPage(self):
        self._staten.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        totaal = len(self._staten)
        for staat in self._staten:
            self.__dict__.update(staat)
            if self.teken_voet and not getattr(self, "_is_cover", False):
                self.teken_voet(self, self._pageNumber, totaal)
            super().showPage()
        super().save()


class RapportDoc(BaseDocTemplate):
    def __init__(self, pad, spec, F, S, assets_dir, **kw):
        super().__init__(pad, pagesize=A4, leftMargin=MARGE, rightMargin=MARGE, topMargin=25 * mm, bottomMargin=22 * mm,
                         title=spec.get("titel", "LawBot Pro-rapport"), author="LawBot Pro (Litic)",
                         subject=spec.get("vorm", ""), creator=f"LawBot Pro rapportsjabloon {SJABLOON_VERSIE}", **kw)
        self.spec, self.F, self.S, self.assets_dir = spec, F, S, Path(assets_dir)
        self.logo_lawbot = self.assets_dir / "logo-lawbot.png"
        self.logo_litic_licht = self.assets_dir / "logo-litic-light.png"
        self.logo_litic_donker = self.assets_dir / "logo-litic-dark.png"
        frame = Frame(MARGE, 22 * mm, LEESBREEDTE, PAGINA_H - 25 * mm - 22 * mm, id="tekst", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        cover = Frame(0, 0, PAGINA_B, PAGINA_H, id="cover", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id="cover", frames=[cover], onPage=self._teken_cover),
                               PageTemplate(id="normaal", frames=[frame], onPage=self._teken_kop)])

    # Inhoudsopgave en bladwijzers
    def afterFlowable(self, flowable):
        toc = getattr(flowable, "_toc", None)
        if toc:
            niveau, tekst, sleutel = toc
            self.canv.bookmarkPage(sleutel)
            self.canv.addOutlineEntry(tekst, sleutel, niveau, 0)
            self.notify("TOCEntry", (niveau, tekst, self.page, sleutel))

    def _label(self, c, x, y, tekst, kleur, size=7, spatie=1.0, rechts=False):
        tekst = tekst.upper()
        w = pdfmetrics.stringWidth(tekst, self.F["sans"], size) + spatie * len(tekst)
        t = c.beginText(x - w if rechts else x, y)
        t.setFont(self.F["sans"], size)
        t.setCharSpace(spatie)
        t.setFillColor(kleur)
        t.textOut(tekst)
        t.setCharSpace(0)
        c.drawText(t)

    def _teken_cover(self, c, doc):
        sp, S = self.spec, self.S
        c._is_cover = True
        c.saveState()
        c.setFillColor(K["groen_donker"])
        c.rect(0, 0, PAGINA_B, PAGINA_H, stroke=0, fill=1)
        # Kaderlabel en accentstreep
        label = " · ".join(x for x in ["Juridisch onderzoek", sp.get("rechtsgebied", "")] if x)
        self._label(c, MARGE, PAGINA_H - 42 * mm, label, K["oker"], size=8, spatie=1.6)
        c.setStrokeColor(K["oker"])
        c.setLineWidth(1.4)
        c.line(MARGE, PAGINA_H - 47 * mm, MARGE + 22 * mm, PAGINA_H - 47 * mm)
        # Titel en ondertitel
        y = PAGINA_H - 66 * mm
        for tekst, stijl in [(sp.get("titel", ""), S["cover_titel"]), (sp.get("ondertitel", ""), S["cover_ondertitel"])]:
            if not tekst:
                continue
            p = Paragraph(par(tekst), stijl)
            w, h = p.wrap(LEESBREEDTE - 10 * mm, 200 * mm)
            p.drawOn(c, MARGE, y - h)
            y -= h + 6 * mm
        # Metadata
        regels = [("Vorm", sp.get("vorm")), ("Perspectief", sp.get("perspectief")), ("Diepte", sp.get("diepte")),
                  ("Bronnen", sp.get("bronnen_samenvatting") or (f"{len(sp.get('bronnen', []))} bronnen" if sp.get("bronnen") else None)),
                  ("Peildatum", datum_nl(sp.get("peildatum"))), ("Waarmerk", sp.get("waarmerk"))]
        y = 98 * mm
        for lab, waarde in regels:
            if not waarde:
                continue
            self._label(c, MARGE, y, lab, K["cover_zacht"], size=6.5, spatie=1.3)
            c.setFont(self.F["sans"], 8.5)
            c.setFillColor(K["cover_tekst"])
            c.drawString(MARGE + 30 * mm, y, str(waarde))
            y -= 6.2 * mm
        # Onderaan: LawBot-mark en Litic-woordmerk
        yb = 20 * mm
        if self.logo_lawbot.exists():
            c.drawImage(str(self.logo_lawbot), MARGE, yb, 13 * mm, 13 * mm, mask="auto")
            xt = MARGE + 17 * mm
        else:
            xt = MARGE
        c.setFillColor(K["cover_tekst"])
        c.setFont(self.F["serif_sb"], 12.5)
        c.drawString(xt, yb + 7.5 * mm, "LawBot Pro")
        c.setFont(self.F["sans"], 7.2)
        c.setFillColor(K["cover_zacht"])
        c.drawString(xt, yb + 3 * mm, "Onderzoeksassistent van Litic")
        if self.logo_litic_licht.exists():
            b, h = rl_utils.ImageReader(str(self.logo_litic_licht)).getSize()
            lw = 34 * mm
            c.drawImage(str(self.logo_litic_licht), PAGINA_B - MARGE - lw, yb + 1.5 * mm, lw, lw * h / b, mask="auto")
        else:
            c.setFont(self.F["sans_b"], 11)
            c.drawRightString(PAGINA_B - MARGE, yb + 5 * mm, "LITIC.AI")
        c.restoreState()

    def _teken_kop(self, c, doc):
        sp = self.spec
        c._is_cover = False
        c.saveState()
        kop = " · ".join(x for x in ["LawBot Pro", sp.get("vorm", "")] if x)
        self._label(c, MARGE, PAGINA_H - 14 * mm, kop, K["inkt_zacht"], size=6.8, spatie=1.2)
        c.setFont(self.F["sans"], 7)
        c.setFillColor(K["salie"])
        c.drawRightString(PAGINA_B - MARGE, PAGINA_H - 14 * mm, datum_nl(sp.get("datum")))
        c.setStrokeColor(K["lijn"])
        c.setLineWidth(0.5)
        c.line(MARGE, PAGINA_H - 17.5 * mm, PAGINA_B - MARGE, PAGINA_H - 17.5 * mm)
        c.restoreState()

    def teken_voet(self, c, pagina, totaal):
        c.saveState()
        c.setStrokeColor(K["lijn_zacht"])
        c.setLineWidth(0.5)
        c.line(MARGE, 16.5 * mm, PAGINA_B - MARGE, 16.5 * mm)
        titel = str(self.spec.get("titel", "")).upper()
        c.setFont(self.F["sans"], 6.5)
        c.setFillColor(K["salie"])
        maxw = LEESBREEDTE - 30 * mm
        while titel and pdfmetrics.stringWidth(titel, self.F["sans"], 6.5) > maxw:
            titel = titel[:-4].rstrip() + "…"
        c.drawString(MARGE, 12 * mm, titel)
        c.setFont(self.F["sans"], 7)
        c.drawRightString(PAGINA_B - MARGE, 12 * mm, f"{pagina} / {totaal}")
        c.restoreState()


# ── Bouwstenen ───────────────────────────────────────────────────────────────────────────────────
class Bouwer:
    def __init__(self, spec, F, S):
        self.spec, self.F, self.S = spec, F, S
        self._n = 0
        self.waarschuwingen = []

    def sleutel(self):
        self._n += 1
        return f"sec{self._n}"

    def kop(self, tekst, nummer=None, niveau=0, label=None, toc_tekst=None):
        """Hoofdstukkop (niveau 0: kaderlabel + serif) of paragraafkop (niveau 1/2: sans)."""
        uit = []
        if niveau == 0:
            uit.append(CondPageBreak(50 * mm))
            lab = label or (f"{nummer}  |  {tekst}" if nummer else tekst)
            uit.append(Kaderlabel(lab, self.F["sans_sb"], K["oker"]))
            p = Paragraph(par(tekst), self.S["kop1"])
            p._toc = (0, toc_tekst or (f"{nummer}  {tekst}" if nummer else tekst), self.sleutel())
            uit.append(p)
        else:
            stijl = self.S["kop2"] if niveau == 1 else self.S["kop3"]
            volledig = f"{nummer}  {tekst}" if nummer else tekst
            p = Paragraph(par(volledig), stijl)
            if niveau == 1:
                p._toc = (1, volledig, self.sleutel())
            uit.append(p)
        return uit

    def alinea(self, tekst, stijl="tekst"):
        return [Paragraph(par(tekst), self.S[stijl])]

    def lijst(self, items, genummerd=False):
        uit = []
        for i, item in enumerate(items, 1):
            bullet = f"{i}." if genummerd else "•"
            uit.append(Paragraph(par(item), self.S["lijst"], bulletText=bullet))
        uit.append(Spacer(1, 3))
        return uit

    def citaat(self, tekst, bron=None):
        delen = [Citaat(Paragraph(par(tekst), self.S["citaat"]))]
        if bron:
            delen.append(Paragraph(par(bron), ParagraphStyle("cb", parent=self.S["citaat_bron"], leftIndent=8 * mm)))
        delen.append(Spacer(1, 7))
        return delen

    def kader(self, label, tekst, kleur=None):
        """Kader op papier met oker-streep links: conclusie vooraf, samenvatting, advies."""
        teksten = list(tekst) if isinstance(tekst, (list, tuple)) else [tekst]
        rijen = [[Kaderlabel(label, self.F["sans_sb"], kleur or K["oker"], ruimte_onder=0)]]
        rijen += [[Paragraph(par(t), self.S["kader_tekst"])] for t in teksten]
        t = Table(rijen, colWidths=[LEESBREEDTE])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), K["papier"]), ("LINEBEFORE", (0, 0), (0, -1), 2, K["oker"]),
                               ("LEFTPADDING", (0, 0), (-1, -1), 6 * mm), ("RIGHTPADDING", (0, 0), (-1, -1), 5 * mm),
                               ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                               ("TOPPADDING", (0, 0), (-1, 0), 4 * mm), ("BOTTOMPADDING", (0, -1), (-1, -1), 4 * mm)]))
        # Korte kaders blijven bijeen (verhuizen desnoods naar de volgende pagina); lange kaders splitsen per alinea.
        return [KeepTogether([t]) if len(rijen) <= 5 else t, Spacer(1, 9)]

    def tabel(self, kop, rijen, kolombreedtes=None, uitlijning=None, titel=None, bijschrift=None, badge_kolom=None, repeat=1):
        """Tabel met kopregel in groen-tint, zebra in papier, alleen horizontale haarlijnen."""
        n = len(kop)
        uitl = list(uitlijning or ["l"] * n) + ["l"] * n
        stijl_cel = {"l": "tabel", "r": "tabel_r", "c": "tabel_c"}
        stijl_kop = {"l": "tabel_kop", "r": "tabel_kop_r", "c": "tabel_kop_c"}
        data = [[Paragraph(par(str(k)), self.S[stijl_kop[uitl[i]]]) for i, k in enumerate(kop)]]
        for rij in rijen:
            cellen = []
            for i in range(n):
                cel = rij[i] if i < len(rij) else ""
                if badge_kolom is not None and i == badge_kolom and isinstance(cel, str):
                    cellen.append(Badge(cel, self.F["sans_sb"]))
                elif isinstance(cel, (Flowable, list, tuple)):
                    cellen.append(cel)
                else:
                    cellen.append(Paragraph(par("" if cel is None else str(cel)), self.S[stijl_cel[uitl[i]]]))
            data.append(cellen)
        if kolombreedtes:
            if all(isinstance(b, (int, float)) and b <= 1 for b in kolombreedtes):
                breedtes = [LEESBREEDTE * b for b in kolombreedtes]
            else:
                breedtes = [b * mm for b in kolombreedtes]
        else:
            lengtes = []
            for i in range(n):
                mx = max([len(str(kop[i]))] + [len(str(r[i])) if i < len(r) and r[i] is not None else 0 for r in rijen])
                lengtes.append(max(6, min(mx, 60)) ** 0.7)
            tot = sum(lengtes)
            breedtes = [max(14 * mm, LEESBREEDTE * l / tot) for l in lengtes]
            schaal = LEESBREEDTE / sum(breedtes)
            breedtes = [b * schaal for b in breedtes]
        t = Table(data, colWidths=breedtes, repeatRows=repeat)
        ts = [("BACKGROUND", (0, 0), (-1, 0), K["groen_tint"]), ("LINEBELOW", (0, 0), (-1, 0), 0.6, K["lijn"]),
              ("LINEBELOW", (0, 1), (-1, -1), 0.4, K["lijn_zacht"]), ("VALIGN", (0, 0), (-1, -1), "TOP"),
              ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
              ("TOPPADDING", (0, 0), (-1, -1), 3.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5)]
        for r in range(2, len(data), 2):
            ts.append(("BACKGROUND", (0, r), (-1, r), K["papier"]))
        t.setStyle(TableStyle(ts))
        uit = []
        if titel:
            uit.append(Paragraph(par(titel), self.S["kop3"]))
        uit.append(t)
        uit.append(Paragraph(par(bijschrift), self.S["bijschrift"]) if bijschrift else Spacer(1, 9))
        return uit

    def noten(self, noten):
        if not noten:
            return []
        uit = [Spacer(1, 4), Haarlijn(breedte=40 * mm, boven=2, onder=4), Kaderlabel("Noten", self.F["sans_sb"], K["groen"], size=6.8, ruimte_onder=2)]
        for i, n in enumerate(noten, 1):
            uit.append(Paragraph(f'<font color="#5f6f62">{i}</font>&nbsp;&nbsp;{par(n)}', self.S["noot"]))
        uit.append(Spacer(1, 8))
        return uit

    def blokken(self, blokken):
        uit = []
        for b in blokken or []:
            if isinstance(b, str):
                uit += self.alinea(b)
                continue
            soort = b.get("type", "alinea")
            if soort == "alinea":
                uit += self.alinea(b.get("tekst", ""))
            elif soort == "subkop":
                uit += self.kop(b.get("tekst", ""), b.get("nummer"), niveau=b.get("niveau", 1))
            elif soort == "lijst":
                uit += self.lijst(b.get("items", []), b.get("genummerd", False))
            elif soort == "citaat":
                uit += self.citaat(b.get("tekst", ""), b.get("bron"))
            elif soort == "kader":
                uit += self.kader(b.get("label", "Kern"), b.get("tekst", ""))
            elif soort == "tabel":
                uit += self.tabel(b.get("kop", []), b.get("rijen", []), b.get("kolombreedtes"), b.get("uitlijning"), b.get("titel"),
                                  b.get("bijschrift"), b.get("badge_kolom"))
            elif soort == "pagina":
                uit.append(PageBreak())
            elif soort == "ruimte":
                uit.append(Spacer(1, b.get("hoogte", 6)))
            else:
                self.waarschuwingen.append(f"onbekend bloktype '{soort}' overgeslagen")
        return uit

    def sectie(self, s, nummer=None, label=None, toc_tekst=None):
        uit = []
        if s.get("nieuwe_pagina"):
            uit.append(PageBreak())
        uit += self.kop(s.get("kop", ""), s.get("nummer", nummer), niveau=0, label=label, toc_tekst=toc_tekst)
        uit += self.blokken(s.get("blokken", []))
        uit += self.noten(s.get("noten"))
        return uit

    def bronnen(self, bronnen):
        """Bronnenlijst: nr · bron (titel/link, instantie, datum, vindplaats, toelichting) · status."""
        if not bronnen:
            return []
        uit = []
        groepen = {}
        volgorde = ["wet", "rechtspraak", "literatuur", "overig"]
        for b in bronnen:
            groepen.setdefault((b.get("soort") or "overig").lower(), []).append(b)
        if len(groepen) == 1:
            groepen = {"": bronnen}
        namen = {"wet": "Wet- en regelgeving", "rechtspraak": "Rechtspraak", "literatuur": "Literatuur en praktijk", "overig": "Overige bronnen"}
        sleutels = [g for g in volgorde if g in groepen] + [g for g in groepen if g not in volgorde]
        telling = {}
        for b in bronnen:
            k = status_sleutel(b.get("status"))
            telling[k] = telling.get(k, 0) + 1
        samen = " · ".join(f"{STATUSSEN[k][0]} {telling[k]}" for k in ["officieel", "web", "niet_gevonden", "niet_open"] if k in telling)
        uit.append(Paragraph(par(f"{len(bronnen)} bronnen: {samen}."), self.S["tekst_klein"]))
        uit.append(Spacer(1, 4))
        for g in sleutels:
            rijen = []
            for b in groepen[g]:
                titel = b.get("titel") or b.get("ecli") or b.get("url") or ""
                url = b.get("url") or b.get("bron_url")
                kop = f"[{titel}]({url})" if url else titel
                meta = " · ".join(str(x) for x in [b.get("instantie") or b.get("auteur"), b.get("ecli") if b.get("titel") and b.get("ecli") else None,
                                                   datum_nl(b.get("datum")), b.get("vindplaats")] if x)
                if status_sleutel(b.get("status")) == "web" and b.get("opgehaald_op"):
                    meta += f" · opgehaald {datum_nl(b['opgehaald_op'])}"
                cel = [Paragraph(par(kop), self.S["bron_titel"])]
                if meta:
                    cel.append(Paragraph(par(meta), self.S["bron_meta"]))
                if url and status_sleutel(b.get("status")) == "web":
                    cel.append(Paragraph(par(url), self.S["bron_meta"]))
                if b.get("toelichting") or b.get("citaat"):
                    tekst = b.get("toelichting") or ""
                    if b.get("citaat"):
                        tekst = (tekst + " " if tekst else "") + f"“{b['citaat']}”"
                    cel.append(Paragraph(par(tekst), self.S["bron_toelichting"]))
                rijen.append([str(b.get("nr", len(rijen) + 1)), cel, b.get("status", "")])
            if g:
                uit += self.kop(namen.get(g, g.capitalize()), niveau=1)
            uit += self.tabel(["Nr", "Bron", "Status"], rijen, kolombreedtes=[0.06, 0.74, 0.20], uitlijning=["r", "l", "l"], badge_kolom=2)
        return uit

    def zoeklog(self, log):
        if not log:
            return []
        rijen = [[str(r.get("ronde", "")), r.get("tool", ""), r.get("vraag") or r.get("zoekvraag") or r.get("parameters", ""), r.get("resultaat", "")] for r in log]
        return self.tabel(["Ronde", "Tool", "Zoekvraag of parameters", "Resultaat"], rijen, kolombreedtes=[0.08, 0.17, 0.40, 0.35], uitlijning=["c", "l", "l", "l"])

    def colofon(self):
        sp = self.spec
        regels = [("Opdrachtgever", sp.get("kantoor")), ("Verantwoordelijk", sp.get("advocaat")),
                  ("Auteur", sp.get("auteur") or "LawBot Pro-agent (Litic), onder verantwoordelijkheid van de advocaat"),
                  ("Vorm", sp.get("vorm")), ("Diepte", sp.get("diepte")), ("Perspectief", sp.get("perspectief")),
                  ("Peildatum", datum_nl(sp.get("peildatum"))), ("Datum rapport", datum_nl(sp.get("datum"))), ("Versie", sp.get("versie", "1.0")),
                  ("Waarmerk", f"**{sp['waarmerk']}**" if sp.get("waarmerk") else "geen waarmerk gegenereerd"),
                  ("Bronroutes", sp.get("bronroutes") or "Officiële bronnen via de LawBot-tools (wetten.overheid.nl, rechtspraak.nl, tuchtrecht, EUR-Lex); "
                                                      "open web via de rondetool web_verkennen (Browserless, Brave, Perplexity). Zie de zoeklog."),
                  ("Disclaimer", sp.get("disclaimer") or "Dit rapport is met behulp van LawBot Pro samengesteld uit officiële bronnen en gelezen webpagina's. "
                                                       "Het is geen juridisch advies; de verantwoordelijk advocaat beoordeelt de bronnen en de conclusies.")]
        kort = [(lab, w) for lab, w in regels[:-2] if w]
        lang = [(lab, w) for lab, w in regels[-2:] if w]
        L, Wd = self.S["colofon_label"], self.S["colofon"]
        kolom = 26 * mm
        waarde = LEESBREEDTE / 2 - kolom
        data, stijl = [], [("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 6)]
        for i in range(0, len(kort), 2):
            links = kort[i]
            rechts = kort[i + 1] if i + 1 < len(kort) else ("", "")
            data.append([Paragraph(links[0], L), Paragraph(par(links[1]), Wd), Paragraph(rechts[0], L), Paragraph(par(rechts[1]), Wd)])
        for lab, w in lang:
            data.append([Paragraph(lab, L), Paragraph(par(w), Wd), "", ""])
            stijl.append(("SPAN", (1, len(data) - 1), (3, len(data) - 1)))
        stijl.append(("LINEBELOW", (0, 0), (-1, -2), 0.3, K["lijn_zacht"]))
        t = Table(data, colWidths=[kolom, waarde, kolom, waarde])
        t.setStyle(TableStyle(stijl))
        return [Kaderlabel("Colofon", self.F["sans_sb"], K["oker"]), t]


def bouw_story(spec, F, S, bouwer):
    sp = spec
    story = [NextPageTemplate("normaal"), PageBreak()]
    # Inhoud + colofon
    story += [Kaderlabel("Inhoud", bouwer.F["sans_sb"], K["oker"]), Paragraph("Inhoudsopgave", S["kop1"])]
    toc = TableOfContents()
    toc.levelStyles = [S["toc0"], S["toc1"]]
    toc.dotsMinLevel = 99
    story += [toc, Spacer(1, 14)]
    story += bouwer.colofon()
    story.append(PageBreak())
    # Samenvatting (wetenschappelijk onderzoek, adviesnotitie)
    if sp.get("samenvatting"):
        story += bouwer.kader(sp.get("samenvatting_label", "Samenvatting"), sp["samenvatting"])
        if sp.get("trefwoorden"):
            story.append(Paragraph(par("**Trefwoorden:** " + " · ".join(sp["trefwoorden"])), S["tekst_klein"]))
            story.append(Spacer(1, 10))
    # Hoofdstukken
    for i, s in enumerate(sp.get("secties", []), 1):
        story += bouwer.sectie(s, nummer=s.get("nummer", str(i)) if sp.get("nummering", True) else None)
    if sp.get("vervolg"):
        story += bouwer.kader("Vervolgsuggesties", sp["vervolg"] if isinstance(sp["vervolg"], list) else [sp["vervolg"]], K["groen"])
    # Bijlagen
    letters = "ABCDEFGHIJKLMNOP"
    bijlagen = list(sp.get("bijlagen", []))
    for i, b in enumerate(bijlagen):
        letter = b.get("letter", letters[i])
        story.append(PageBreak())
        story += bouwer.sectie(dict(b, nieuwe_pagina=False), nummer=None, label=f"Bijlage {letter}  |  {b.get('kop', '')}",
                               toc_tekst=f"Bijlage {letter}  {b.get('kop', '')}")
    # Bronnen
    if sp.get("bronnen"):
        story.append(PageBreak())
        story += bouwer.kop("Bronnen", niveau=0, label="Bronnenlijst met verificatiestatus")
        story += bouwer.bronnen(sp["bronnen"])
    # Zoeklog
    if sp.get("zoeklog"):
        story.append(PageBreak())
        story += bouwer.kop("Zoeklog", niveau=0, label=f"Bijlage {letters[len(bijlagen)]}  |  Zoeklog", toc_tekst=f"Bijlage {letters[len(bijlagen)]}  Zoeklog")
        if sp.get("zoeklog_toelichting"):
            story += bouwer.alinea(sp["zoeklog_toelichting"], "tekst_klein")
        story += bouwer.zoeklog(sp["zoeklog"])
    # Afsluiting
    story.append(Spacer(1, 10))
    story.append(Haarlijn(breedte=40 * mm))
    afsl = sp.get("afsluiting") or (f"LawBot Pro-waarmerk: {sp['waarmerk']}. " if sp.get("waarmerk") else "") + \
        "Samengesteld met LawBot Pro, de onderzoeksassistent van Litic. De bronnen zijn controleerbaar via de links in de bronnenlijst."
    story.append(Paragraph(par(afsl), S["bijschrift"]))
    return story


def maak_rapport(spec, pad="rapport.pdf", assets_dir=None, download=True):
    """Rendert de spec naar een PDF. Geeft een dict met pagina's, fontbron, logo's en waarschuwingen.
    assets_dir: map met fonts/ en logo's (standaard de map van dit bestand). Ontbreken ze daar en is
    download True, dan worden ze één keer uit de publieke marketplace gehaald (cachemap onder HOME)."""
    if assets_dir is None:
        try:
            assets_dir = Path(__file__).resolve().parent
        except NameError:
            assets_dir = Path(os.environ.get("LAWBOT_ASSETS", "."))
    assets_dir = Path(assets_dir)
    assets_bron = "skill"
    if not assets_compleet(assets_dir):
        cache = haal_assets_op() if download else None
        if cache:
            assets_dir, assets_bron = cache, "gedownload"
        else:
            assets_bron = "onvolledig"
    F, fontbron = laad_fonts(assets_dir)
    S = maak_stijlen(F)
    spec = dict(spec)
    spec.setdefault("datum", datetime.date.today().isoformat())
    bouwer = Bouwer(spec, F, S)
    doc = RapportDoc(str(pad), spec, F, S, assets_dir)
    story = bouw_story(spec, F, S, bouwer)
    GenummerdCanvas.teken_voet = staticmethod(doc.teken_voet)
    doc.multiBuild(story, canvasmaker=GenummerdCanvas)
    waarsch = list(bouwer.waarschuwingen)
    if fontbron != "huisstijl":
        waarsch.append(f"huisstijlfonts niet gevonden in {assets_dir / 'fonts'}; terugval op {fontbron}")
    logos = {"lawbot": doc.logo_lawbot.exists(), "litic": doc.logo_litic_licht.exists()}
    if not all(logos.values()):
        waarsch.append("een of meer logo's ontbreken; woordmerk getekend in tekst")
    return {"pad": str(pad), "paginas": doc.page, "fonts": fontbron, "logos": logos, "assets": assets_bron, "waarschuwingen": waarsch, "sjabloon": SJABLOON_VERSIE}


# ── Voorbeeldspec (ook de referentie voor de veldnamen) ─────────────────────────────────────────
VOORBEELD = {
    "titel": "De klachtplicht van art. 6:89 BW bij non-conformiteit",
    "ondertitel": "Verkennend onderzoek naar termijn, stelplicht en bewijslast in de rechtspraak sinds 2013",
    "vorm": "Wetenschappelijk onderzoek", "rechtsgebied": "Verbintenissenrecht", "perspectief": "neutraal", "diepte": "verkennend",
    "peildatum": "2026-10-10", "datum": "2026-10-10", "kantoor": "Voorbeeldkantoor", "advocaat": "mr. A. Voorbeeld",
    "waarmerk": "LBP-0000-0000", "versie": "1.0",
    "samenvatting": "Korte samenvatting van de bevindingen in drie tot vijf zinnen.",
    "trefwoorden": ["klachtplicht", "art. 6:89 BW", "non-conformiteit"],
    "secties": [
        {"kop": "Inleiding", "blokken": [
            {"type": "alinea", "tekst": "Aanleiding, hoofdvraag en deelvragen. Zie noot [1]."},
            {"type": "subkop", "tekst": "Afbakening", "nummer": "1.1"},
            {"type": "lijst", "items": ["Peildatum 10 oktober 2026.", "Alleen Nederlandse rechtspraak."]},
            {"type": "citaat", "tekst": "Letterlijk citaat uit tool-output.", "bron": "HR 8 februari 2013, ECLI:NL:HR:2013:BY4600, r.o. 4.2.2"},
            {"type": "kader", "label": "Conclusie vooraf", "tekst": "De kern in drie zinnen."},
            {"type": "tabel", "titel": "Tabel 1. Telling per instantie", "kop": ["Instantie", "Aantal"], "rijen": [["Hoge Raad", "3"], ["Hoven", "12"]],
             "kolombreedtes": [0.7, 0.3], "uitlijning": ["l", "r"], "bijschrift": "Bron: analysematrix, bijlage A."},
        ], "noten": ["Eerste noot met [link](https://wetten.overheid.nl/BWBR0005289/2026-01-01#Boek6_Titeldeel1_Afdeling9_Artikel89)."]},
    ],
    "vervolg": ["J: jurisprudentie_bij_artikel 6:89 BW, hoven 2024-2026.", "W: wet_versies 7:23 BW peildatum."],
    "bijlagen": [{"kop": "Analysematrix", "blokken": [{"type": "tabel", "kop": ["Nr", "ECLI", "Instantie", "Datum", "Uitkomst"],
                                                        "rijen": [["1", "ECLI:NL:HR:2013:BY4600", "Hoge Raad", "2013-02-08", "klacht tijdig"]],
                                                        "uitlijning": ["r", "l", "l", "l", "l"]}]}],
    "bronnen": [
        {"nr": 1, "soort": "wet", "titel": "Art. 6:89 BW", "url": "https://wetten.overheid.nl/BWBR0005289/2026-01-01", "instantie": "wetten.overheid.nl",
         "datum": "2026-01-01", "status": "officieel", "toelichting": "Geldende tekst op de peildatum."},
        {"nr": 2, "soort": "rechtspraak", "titel": "HR 8 februari 2013", "ecli": "ECLI:NL:HR:2013:BY4600", "url": "https://uitspraken.rechtspraak.nl/details?id=ECLI:NL:HR:2013:BY4600",
         "instantie": "Hoge Raad", "datum": "2013-02-08", "vindplaats": "r.o. 4.2.2", "status": "officieel", "citaat": "kernoverweging letterlijk"},
        {"nr": 3, "soort": "literatuur", "titel": "Blog over klachtplicht", "url": "https://voorbeeld.nl/klachtplicht", "auteur": "Kantoor X",
         "datum": "2025-03-01", "status": "web, geciteerd", "opgehaald_op": "2026-10-10", "citaat": "letterlijk citaat uit het veld tekst"},
        {"nr": 4, "soort": "literatuur", "titel": "Tijdschriftartikel achter betaalmuur", "url": "https://voorbeeld.nl/artikel", "status": "niet open toegankelijk"},
    ],
    "zoeklog": [{"ronde": 1, "tool": "zoek_wet", "vraag": "6:89 BW", "resultaat": "artikel opgehaald"},
                {"ronde": 2, "tool": "web_verkennen", "vraag": "klachtplicht 6:89 BW termijn · klachtplicht non-conformiteit annotatie", "resultaat": "12 kandidaten, 5 gelezen"}],
}

if __name__ == "__main__":
    import json
    import sys
    uit = sys.argv[1] if len(sys.argv) > 1 else "voorbeeld_rapport.pdf"
    print(json.dumps(maak_rapport(VOORBEELD, uit), ensure_ascii=False, indent=1))
