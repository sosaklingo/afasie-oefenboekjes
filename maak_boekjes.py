#!/usr/bin/env python3
"""Genereer vijf A4-afasieboekjes met ingebedde lettertypen en grote letters."""

from __future__ import annotations

from pathlib import Path
import json
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).parent
OUTPUT = ROOT / "pdf"
OUTPUT.mkdir(exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
pdfmetrics.registerFont(TTFont("DV", FONT))
pdfmetrics.registerFont(TTFont("DV-Bold", BOLD))

W, H = A4
M = 52
INK = colors.HexColor("#173d36")
GREEN = colors.HexColor("#216b64")
MUTED = colors.HexColor("#4b675e")
CREAM = colors.HexColor("#fbfaf6")
PALE = colors.HexColor("#e8f2eb")
PALEBLUE = colors.HexColor("#e8eff5")
PALEGOLD = colors.HexColor("#fbf1d7")
OUTLINE = colors.HexColor("#d4e2d8")


def para(c, text, x, top, width, size=16, leading=None, bold=False, color=INK, align=TA_LEFT):
    """Teken een omlooptekst onder een topcoördinaat; retourneer nieuwe top."""
    style = ParagraphStyle("p", fontName="DV-Bold" if bold else "DV", fontSize=size,
                           leading=leading or size * 1.56, textColor=color, alignment=align,
                           allowWidows=0, allowOrphans=0, spaceAfter=0)
    content = escape(text).replace("\n", "<br/>")
    p = Paragraph(content, style)
    _, h = p.wrap(width, 900)
    p.drawOn(c, x, top - h)
    return top - h


class Book:
    def __init__(self, filename, booknum, name, subtitle, tint=PALE):
        self.c = canvas.Canvas(str(OUTPUT / filename), pagesize=A4, pageCompression=1)
        self.c.setTitle(name + " - Stap voor stap weer praten")
        self.c.setAuthor("Marco Beenen en ChatGPT (OpenAI)")
        self.booknum = booknum
        self.name = name
        self.subtitle = subtitle
        self.tint = tint
        self.number = 0

    def base(self, title, section="OEFENEN"):
        self.number += 1
        c = self.c
        c.setFillColor(CREAM)
        c.rect(0, 0, W, H, stroke=0, fill=1)
        c.setFillColor(self.tint)
        c.roundRect(M, H-85, W-2*M, 35, 10, stroke=0, fill=1)
        c.setFont("DV-Bold", 10)
        c.setFillColor(GREEN)
        c.drawString(M+15, H-71, "STAP VOOR STAP WEER PRATEN")
        c.drawRightString(W-M-15, H-71, f"BOEK {self.booknum}")
        c.setFillColor(MUTED)
        c.setFont("DV-Bold", 11)
        c.drawString(M, H-117, section)
        top = para(c, title, M, H-136, W-2*M, size=26, leading=34, bold=True)
        c.setStrokeColor(OUTLINE)
        c.line(M, 54, W-M, 54)
        c.setFont("DV", 9)
        c.setFillColor(MUTED)
        c.drawString(M, 37, "Aanwijzen, tekenen, schrijven of praten: alles mag.")
        c.drawRightString(W-M, 37, str(self.number))
        return top - 22

    def cover(self, label, short_description):
        self.number += 1
        c = self.c
        c.setFillColor(self.tint)
        c.rect(0, 0, W, H, stroke=0, fill=1)
        c.setFillColor(GREEN)
        c.circle(W-50, H-100, 150, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#c9e2d2"))
        c.circle(-42, 102, 120, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.roundRect(W-258, H-223, 158, 117, 29, stroke=0, fill=1)
        c.setFillColor(GREEN)
        for pos in (W-216, W-179, W-142):
            c.circle(pos, H-164, 10, stroke=0, fill=1)
        c.setFillColor(MUTED)
        c.setFont("DV-Bold", 11)
        c.drawString(M, H-105, "STAP VOOR STAP WEER PRATEN")
        c.setFillColor(GREEN)
        c.setFont("DV-Bold", 12)
        c.drawString(M, H-265, label)
        top = para(c, self.name, M, H-290, W-2*M, size=37, leading=47, bold=True)
        top = para(c, self.subtitle, M, top-27, W-2*M-30, size=20, leading=32, color=MUTED)
        para(c, short_description, M, min(top-70,220), W-2*M, size=16, leading=26)
        c.setFillColor(GREEN)
        c.setFont("DV-Bold", 11)
        c.drawString(M, 65, "MARCO BEENEN · NOVEMBER 2026")
        c.showPage()

    def page_done(self):
        self.c.showPage()

    def close(self):
        self.c.save()
        return OUTPUT / (self.c._filename.split("/")[-1])


def callout(book, top, message, shade=PALE, size=15):
    c = book.c
    width = W - 2*M
    style = ParagraphStyle("callout", fontName="DV", fontSize=size,
                           leading=size * 1.6, textColor=INK)
    p = Paragraph(escape(message), style)
    _, height = p.wrap(width-32, 500)
    h = height+25
    c.setFillColor(shade)
    c.roundRect(M, top-h, width, h, 13, fill=1, stroke=0)
    p.drawOn(c, M+16, top-h+13)
    return top-h-24


def write_lines(book, top, count=3):
    c = book.c
    c.setStrokeColor(colors.HexColor("#a9beb1"))
    for i in range(count):
        y = top-i*50
        c.line(M+8, y, W-M-8, y)
    return top-count*50


def choice_boxes(book, choices, top):
    c = book.c
    colw = (W-2*M-12)/2
    rowh = 107
    for i, value in enumerate(choices):
        col = i % 2
        row = i // 2
        x = M+col*(colw+12)
        y = top-row*(rowh+14)-rowh
        c.setFillColor(colors.white)
        c.setStrokeColor(OUTLINE)
        c.setLineWidth(1.3)
        c.roundRect(x,y,colw,rowh,16,stroke=1,fill=1)
        c.setFillColor(self_color := GREEN)
        c.circle(x+22,y+rowh-24,8,fill=0,stroke=1)
        para(c,value,x+17,y+rowh-45,colw-34,size=16,bold=True,align=TA_CENTER)
    return top-((len(choices)+1)//2)*(rowh+14)


EASY = [
 ("Een woord kiezen","Waarmee kun je iemand bellen?",["Boek","Telefoon","Sleutel","Kopje"],"Telefoon","Je houdt het in je hand en hoort het soms rinkelen."),
 ("In de keuken","Waaruit drink je koffie of thee?",["Stoel","Sleutel","Kopje","Schoen"],"Kopje","Je kunt het op tafel zetten."),
 ("Groeten","Wat zeg je meestal als je iemand ziet?",["Tot morgen","Hallo","Welterusten","Dank je"],"Hallo","Je begint er vaak een gesprek mee."),
 ("Woorden lezen","Lees of wijs de woorden aan. Zeg er één hardop als je wilt.",None,None,"water · huis · stoel · brood · telefoon"),
 ("Aanvullen","Ik slaap in een ...",["bed","trein","tuin","glas"],"bed","Waar ligt een kussen?"),
 ("Ja of nee","Een fiets heeft meestal twee wielen.",["Ja","Nee"],"Ja","Denk aan een gewone fiets."),
 ("Tegenstellingen","Wat is het tegenovergestelde van KOUD?",["Warm","Blauw","Kort","Zacht"],"Warm","Hoe noem je iets dat veel warmte heeft?"),
 ("Wat hoort erbij?","Welk woord hoort bij eten?",["Lepel","Kussen","Jas","Telefoon"],"Lepel","Waarmee kun je soep eten?"),
 ("Een zin maken","Maak of wijs een zin met deze woorden.",None,None,"Ik · wil · graag · water"),
 ("De dag","Welke dag komt na maandag?",["Vrijdag","Dinsdag","Zondag","Zaterdag"],"Dinsdag","Denk aan het begin van de week."),
 ("Hulp vragen","Wat kun je zeggen als je hulp wilt?",["Ik wil hulp","Ik ga weg","Ik ben laat","Tot morgen"],"Ik wil hulp","Het begint met: Ik wil ..."),
 ("Mijn eigen woorden","Noem, schrijf of teken drie dingen die voor jou belangrijk zijn.",None,None,"Een persoon · een plek · iets wat je graag doet")
]

MEDIUM = [
 ("Een zin aanvullen","Morgen heb ik een afspraak. Ik zet de tijd in mijn ...",["agenda","schoen","pan","tuin"],"agenda","Waar kun je afspraken opschrijven?",None),
 ("De juiste volgorde","Welke zin klopt het best?",["Ik koffie drink in de ochtend.","In ochtend ik drink koffie.","Ik drink 's ochtends koffie."],"Ik drink 's ochtends koffie.","Denk aan: wie - doet wat - wanneer.",None),
 ("Wat past niet?","Drie woorden zijn kleding. Welk woord hoort er niet bij?",["jas","broek","fiets","trui"],"fiets","Wat kun je aantrekken?",None),
 ("Een verband zoeken","Sleutel hoort bij deur, zoals wachtwoord hoort bij ...",["account","bord","fiets","bloem"],"account","Waarmee log je in?",None),
 ("Een kort bericht","Op welke dag heeft Noor een afspraak?",["maandag","woensdag","vrijdag"],"woensdag","Lees de eerste zin nog een keer.","Noor heeft woensdag om twee uur een afspraak bij de logopedist. Ze gaat met de bus en neemt haar agenda mee."),
 ("Nog een vraag","Hoe reist Noor?",["met de fiets","met de auto","met de bus"],"met de bus","Lees de tweede zin nog een keer.","Noor heeft woensdag om twee uur een afspraak bij de logopedist. Ze gaat met de bus en neemt haar agenda mee."),
 ("De eerste stap","Je wilt een afspraak maken. Wat is een logische eerste stap?",["De praktijk bellen","Alvast afscheid nemen","Je jas ophangen"],"De praktijk bellen","Hoe neem je contact op?",None),
 ("Een zin afmaken","Ik was mijn handen met water en ...",["zeep","papier","zand","melk"],"zeep","Wat maakt je handen schoon?",None),
 ("Betekenis","Welk woord betekent ongeveer hetzelfde als blij?",["boos","vrolijk","moe","stil"],"vrolijk","Je voelt je goed en lacht misschien.",None),
 ("Een verhaal begrijpen","Wie bezoekt Sam?",["een collega","zijn zus","een buurman"],"zijn zus","Zoek de zin waarin 'bezoekt' staat.","Sam neemt om half elf de trein naar Utrecht. Hij bezoekt zijn zus. Daarna gaat hij weer naar huis."),
 ("Een gesprek oefenen","Stel jezelf voor aan iemand die je nog niet kent.",None,None,"Mijn naam is ... · Ik woon in ... · Ik houd van ...",None),
 ("Een verhaal vertellen","Vertel, schrijf of teken wat jij graag doet op een fijne dag.",None,None,"Eerst ... · Daarna ... · Tot slot ...",None),
]

BOARD = [
 ("Snel zeggen",["Ja","Nee","Ik weet het niet","Stop alsjeblieft","Praat langzamer","Schrijf het op","Geef me tijd","Nog een keer","Ik heb hulp nodig"]),
 ("Ik heb iets nodig",["Ik wil wat drinken","Ik moet naar het toilet","Ik wil rusten","Ik heb het koud","Ik heb het warm","Ik wil mijn telefoon","Ik wil bezoek","Ik wil stilte","Ik wil een verpleegkundige spreken"]),
 ("Hoe ik me voel",["Ik voel me goed","Ik ben verdrietig","Ik ben moe","Ik ben bang","Ik ben gefrustreerd","Ik ben rustig","Ik ben blij je te zien","Ik begrijp het niet","Ik wil praten"]),
 ("Mijn lichaam",["Ik heb pijn","Ik heb hoofdpijn","Ik ben duizelig","Ik ben misselijk","Ik ben benauwd","Ik zie niet goed","Ik hoor je niet goed","Hier doet het pijn","Ik voel me plotseling slechter"]),
 ("Mensen",["Mijn familie","Mijn vriend of vriendin","De arts","De logopedist","De therapeut","Ikzelf","Ik wil iemand bellen","Ik wil naar huis","Blijf even bij me"]),
 ("Mijn dag",["Eten","Wassen","Aankleden","Wandelen","Zitten","Televisie","Muziek","Lezen","Hoe laat is het?"]),
 ("Vragen stellen",["Wat bedoel je?","Welke dag is het?","Waar zijn we?","Wie komt er?","Wanneer?","Wat gaan we doen?","Wil je het herhalen?","Mag ik even nadenken?","Dat klopt"]),
]

# De moeilijkere opdrachten komen uit dezelfde bron als de interactieve website.
EXTRA_DATA = ROOT / "levels-extra.json"


def extra_levels():
    if not EXTRA_DATA.is_file():
        raise FileNotFoundError("levels-extra.json ontbreekt. Draai eerst exporteer_extra_niveaus.mjs.")
    data = json.loads(EXTRA_DATA.read_text(encoding="utf-8"))
    for key in ("advanced3", "advanced4"):
        if len(data.get(key, [])) != 12:
            raise ValueError(f"{key} moet 12 opdrachten bevatten")
    return data


def intro(book, level):
    y=book.base("Zo gebruik je dit boekje",section="VOOR JE BEGINT")
    for title,description in [
        ("1. Kies zelf", "Kies een pagina die je prettig vindt. Je hoeft niet bij de eerste opdracht te beginnen."),
        ("2. Antwoord op jouw manier", "Praat, wijs aan, maak een gebaar, teken of schrijf. Ook een gedeeltelijk antwoord is waardevol."),
        ("3. Doe het rustig", "Neem de tijd. Stop of pauzeer als je moe of gefrustreerd raakt."),
        ("4. Vraag hulp", "Een begeleider kan een vraag voorlezen, een hint geven of twee keuzes aanwijzen.")
    ]:
        y=para(book.c,title,M,y,W-2*M,size=18,bold=True)-8
        y=para(book.c,description,M,y,W-2*M,size=14,leading=22)-24
    callout(book,y-4,"Dit is geen toets. De juiste ondersteuning verschilt per persoon. Stem oefeningen af met een logopedist.",book.tint,14)
    book.page_done()


def exercise(book,index,exercise,level):
    if level=="easy":
        title,prompt,options,answer,hint=exercise
        story=None
    else:
        title,prompt,options,answer,hint,story=exercise
    y=book.base(title,section=f"OPDRACHT {index:02d} VAN 12")
    if story:
        y=callout(book,y,"LEES OF LUISTER: " + story,book.tint,15)
    y=para(book.c,prompt,M,y,W-2*M,size=19,leading=30,bold=True)-25
    if options:
        y=choice_boxes(book,options,y)
        para(book.c,"Wijs een antwoord aan of zet er een rondje omheen.",M,y-10,W-2*M,size=13,color=MUTED)
        write_lines(book,y-96,2)
    else:
        y=callout(book,y,"Woorden om te proberen: " + hint,book.tint,16)
        write_lines(book,y-20,5)
    if options:
        para(book.c,"HINT: " + hint,M,160,W-2*M,size=12,leading=19,color=MUTED)
    book.page_done()


def longer_text_exercise(book, index, task):
    """Gebruik voor langere teksten een leespagina en een aparte vraagpagina."""
    y = book.base(task["title"], section=f"TEKST {index:02d} VAN 12")
    y = para(book.c, "Lees rustig. Of laat iemand de tekst voorlezen.", M, y, W-2*M,
             size=15, leading=24, color=MUTED) - 22
    y = callout(book, y, task["story"], book.tint, size=15)
    para(book.c, "Je mag de tekst zo vaak teruglezen als je wilt. Op de volgende pagina staat een vraag.",
         M, max(125, y-22), W-2*M, size=13, leading=21, color=MUTED)
    book.page_done()

    y = book.base(task["title"], section=f"VRAAG {index:02d} VAN 12")
    y = para(book.c, task["prompt"], M, y, W-2*M, size=19, leading=30, bold=True) - 26
    options = task.get("options")
    if options:
        y = choice_boxes(book, options, y)
        y = para(book.c, "Wijs een antwoord aan of zet er een rondje omheen.", M, y-12,
                 W-2*M, size=13, color=MUTED) - 35
        write_lines(book, y, 2)
    else:
        words = " · ".join(task.get("words", []))
        y = callout(book, y, "Zinnen om je op weg te helpen: " + words, book.tint, size=14)
        write_lines(book, y-15, 6)
    para(book.c, "HINT: " + task["hint"], M, 154, W-2*M, size=12, leading=19, color=MUTED)
    book.page_done()


def answers(book,exercises):
    y=book.base("Voorbeeldantwoorden",section="ACHTER IN HET BOEK")
    y=callout(book,y,"Kijk samen naar antwoorden als dat helpt. Bij persoonlijke opdrachten is er niet één goed antwoord.",book.tint,14)
    for i,item in enumerate(exercises):
        if isinstance(item, dict):
            title=item["title"]
            answer=item.get("sample") or (item["options"][item["answer"]] if item.get("options") else None)
        elif len(item)==5:
            title,prompt,opts,answer,hint=item
        else:
            title,prompt,opts,answer,hint,story=item
        text=(answer or "Eigen woorden, gebaren, tekening of aanwijzen")
        y=para(book.c,f"{i+1}. {title}",M,y,W-2*M,size=14,bold=True)-2
        y=para(book.c,f"Voorbeeld: {text}",M+17,y,W-2*M-17,size=13,leading=19)-10
        if y<90:
            book.page_done()
            y=book.base("Voorbeeldantwoorden vervolg",section="ACHTER IN HET BOEK")
    book.page_done()


def reflection(book):
    y=book.base("Mijn volgende stap",section="MIJN NOTITIES")
    y=para(book.c,"Wat ging vandaag prettig?",M,y,W-2*M,size=19,bold=True)-35
    y=write_lines(book,y,3)-28
    y=para(book.c,"Welke woorden of zinnen wil ik nog oefenen?",M,y,W-2*M,size=19,bold=True)-35
    y=write_lines(book,y,3)-20
    callout(book,y,"Alles wat lukt, hoe klein ook, is een manier om contact te maken.",book.tint,15)
    book.page_done()


def resources(book):
    y=book.base("Uitleg voor de begeleider",section="SAMEN OEFENEN")
    for sentence in [
        "Vraag eerst of de persoon wil oefenen. Praat op een normale, respectvolle manier.",
        "Gebruik korte zinnen. Geef tijd. Schrijf sleutelwoorden op en gebruik gebaren of aanwijzen.",
        "Verander een opdracht als hij niet past. De logopedist kan helpen bij het kiezen van geschikte oefeningen.",
        "Moeheid of frustratie is een goed moment om te stoppen. Het doel is communicatie, niet een hoge score."
    ]:
        y=para(book.c,"• "+sentence,M,y,W-2*M,size=14,leading=24)-21
    y=callout(book,y,"Dit boekje is aanvullend oefenmateriaal. Het is niet onderzocht als diagnostische of therapeutische methode.",book.tint,13)
    y=para(book.c,"Meer informatie",M,y-7,W-2*M,size=16,bold=True)-12
    y=para(book.c,"thuisarts.nl/beroerte  |  afasie.nl  |  asha.org/practice-portal/clinical-topics/aphasia/",M,y,W-2*M,size=10,leading=17,color=MUTED)
    book.page_done()


def make_learning_books():
    specs=[("01-woorden-terugvinden.pdf","01","Woorden terugvinden","Eenvoudige oefeningen voor woorden, keuzes en korte zinnen",PALE,EASY,"NIVEAU 1"),
           ("02-zinnen-en-verhalen.pdf","02","Zinnen en verhalen","Meer uitdaging met zinnen, verbanden en korte teksten",PALEBLUE,MEDIUM,"NIVEAU 2")]
    results=[]
    for filename,num,title,subtitle,tint,tasks,level in specs:
        b=Book(filename,num,title,subtitle,tint)
        b.cover(level,"Oefen op jouw tempo. Laat woorden zien, schrijf iets op of laat iemand je helpen. Niets hoeft in één keer te lukken.")
        intro(b,level)
        for i,task in enumerate(tasks,1):
            exercise(b,i,task,"easy" if num=="01" else "medium")
        answers(b,tasks)
        reflection(b)
        resources(b)
        results.append((b.close(),b.number))
    extra = extra_levels()
    advanced_specs = [
        ("niveau-3-teksten-begrijpen.pdf", "N3", "Teksten begrijpen",
         "Langere teksten en vragen over de betekenis", PALEBLUE, extra["advanced3"], "NIVEAU 3"),
        ("niveau-4-denken-en-verwoorden.pdf", "N4", "Denken en verwoorden",
         "Moeilijkere teksten, verbanden en een eigen mening", PALEGOLD, extra["advanced4"], "NIVEAU 4"),
    ]
    for filename,num,title,subtitle,tint,tasks,level in advanced_specs:
        b=Book(filename,num,title,subtitle,tint)
        b.cover(level,"Lees of luister op jouw tempo. Een tekst heeft een eigen pagina en de vraag komt daarna. Aanwijzen, schrijven en pauzeren mag altijd.")
        intro(b,level)
        for i,task in enumerate(tasks,1):
            longer_text_exercise(b,i,task)
        answers(b,tasks)
        reflection(b)
        resources(b)
        results.append((b.close(),b.number))
    return results


def draw_board_grid(book,top,phrases):
    c=book.c
    gap=12
    cw=(W-2*M-2*gap)/3
    rh=156
    for i,p in enumerate(phrases):
        x=M+(i%3)*(cw+gap)
        y=top-(i//3)*(rh+gap)-rh
        c.setFillColor(colors.white)
        c.setStrokeColor(OUTLINE)
        c.setLineWidth(1.4)
        c.roundRect(x,y,cw,rh,15,fill=1,stroke=1)
        c.setFillColor(GREEN)
        c.circle(x+cw/2,y+rh-33,13,fill=0,stroke=1)
        para(c,p,x+9,y+rh-62,cw-18,size=13,leading=20,bold=True,align=TA_CENTER)


def make_communication_book():
    b=Book("03-ik-wil-iets-vertellen.pdf","03","Ik wil iets vertellen","Grote aanwijskaarten voor dagelijkse gesprekken",PALEGOLD)
    b.cover("COMMUNICATIEBOEKJE","Wijs een woord of zin aan. Als praten moeilijk is, kan iemand anders lezen wat je aanwijst.")
    y=b.base("Samen praten met dit boekje",section="EERST EVEN LEZEN")
    y=para(b.c,"Dit is een communicatiehulpmiddel, geen toets.",M,y,W-2*M,size=20,bold=True)-27
    for text in ["Vraag of iemand de kaart wil gebruiken en leg hem binnen bereik.",
                 "Laat de persoon zelf kiezen. Wijs niet meteen een antwoord aan.",
                 "Gebruik zo nodig ja/nee-vragen, schrijven, tekenen of gebaren.",
                 "Controleer of je elkaar goed hebt begrepen. Geef tijd en neem pauze."]:
        y=para(b.c,"• "+text,M,y,W-2*M,size=15,leading=24)-21
    callout(b,y-8,"Bij nieuwe, plotselinge spraakuitval, scheve mond, krachtsverlies of andere ernstige nieuwe klachten: vraag meteen medische spoedhulp (in Nederland 112).",PALEGOLD,14)
    b.page_done()
    for section,phrases in BOARD:
        y=b.base(section,section="AANWIJSKAART")
        y=para(b.c,"Wijs aan wat je wilt zeggen. Een ander kan het voorlezen.",M,y,W-2*M,size=15,color=MUTED)-24
        draw_board_grid(b,y,phrases)
        b.page_done()
    y=b.base("Letters aanwijzen",section="LETTERKAART")
    y=para(b.c,"Wijs letters aan om een woord te maken, als dat voor jou werkt.",M,y,W-2*M,size=15)-30
    abc=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    cols=6
    gap=10
    cw=(W-2*M-(cols-1)*gap)/cols
    for i,ch in enumerate(abc):
        x=M+(i%cols)*(cw+gap)
        iy=i//cols
        yp=y-iy*94-80
        b.c.setFillColor(colors.white)
        b.c.setStrokeColor(OUTLINE)
        b.c.roundRect(x,yp,cw,80,12,stroke=1,fill=1)
        para(b.c,ch,x,yp+67,cw,size=23,bold=True,align=TA_CENTER)
    b.page_done()
    y=b.base("Getallen aanwijzen",section="GETALLENKAART")
    y=para(b.c,"Wijs een getal aan. Je kunt ook een tijd of datum schrijven.",M,y,W-2*M,size=15)-30
    digits=list("0123456789")
    cols=5
    cw=(W-2*M-4*12)/5
    for i,ch in enumerate(digits):
        x=M+(i%5)*(cw+12)
        yp=y-(i//5)*111-95
        b.c.setFillColor(colors.white)
        b.c.setStrokeColor(OUTLINE)
        b.c.roundRect(x,yp,cw,95,14,fill=1,stroke=1)
        para(b.c,ch,x,yp+78,cw,size=29,bold=True,align=TA_CENTER)
    y=y-275
    para(b.c,"Vandaag is het: __________________________",M,y,W-2*M,size=17)
    para(b.c,"Mijn afspraak is om: ______________________",M,y-70,W-2*M,size=17)
    b.page_done()
    y=b.base("Woorden die bij mij passen",section="PERSOONLIJK MAKEN")
    for t in ["Mijn naam is:","Belangrijke mensen voor mij:","Mijn favoriete bezigheid:","Woorden die ik vaak nodig heb:"]:
        y=para(b.c,t,M,y,W-2*M,size=16,bold=True)-31
        y=write_lines(b,y,1)-14
    b.page_done()
    y=b.base("Mijn eigen zinnen",section="ZELF INVULLEN")
    y=para(b.c,"Schrijf hier samen woorden of zinnen die handig zijn.",M,y,W-2*M,size=16)-35
    write_lines(b,y,9)
    b.page_done()
    resources(b)
    return b.close(),b.number


if __name__ == "__main__":
    all_files = make_learning_books()
    all_files.append(make_communication_book())
    for path, pages in all_files:
        print(f"{path}: {pages} pagina's")
