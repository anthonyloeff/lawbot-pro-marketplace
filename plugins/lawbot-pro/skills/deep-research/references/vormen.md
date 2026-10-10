# De tien rapportvormen van deep research

Elke vorm heeft altijd: cover, inhoudsopgave met colofon (incl. LawBot Pro-waarmerk), bronnenlijst met
verificatiestatus per bron, zoeklog als bijlage, standaarddisclaimer. Uitvoer: PDF (standaard) via
`assets/rapport_sjabloon.py`; Word (.docx) of Markdown alleen op verzoek, met dezelfde opbouw.
Verificatiestatus per bron: **officieel** (opgehaald met een officiële tool) · **web, geciteerd** (gelezen;
letterlijk citaat, url, ophaaldatum) · **niet gevonden** (gezocht; routes vermeld) · **niet open
toegankelijk** (login, betaalmuur, blokkade; nooit omzeild).

| # | Vorm | Perspectief | Kies deze vorm als |
|---|---|---|---|
| 1 | Onderzoeksmemo | neutraal | de advocaat een volledige analyse met conclusie wil |
| 2 | Adviesnotitie | voor de advocaat | er snel een onderbouwd advies in één pagina nodig is |
| 3 | Bronnenoverzicht | neutraal | de advocaat zelf wil lezen en alleen de bronnen geordend wil |
| 4 | Wetenschappelijk onderzoek | neutraal, dogmatisch | het stuk publiceerbaar of toetsbaar moet zijn (artikel, intern onderzoek, scriptiebegeleiding) |
| 5 | Processtuk-onderbouwing | partijdig | de tekst in een conclusie, pleitnota of verzoekschrift gaat |
| 6 | Cliëntbrief | voor de cliënt | de advocaat de cliënt wil informeren in gewone taal |
| 7 | Rechtspraakkaart | neutraal | overzicht over veel uitspraken nodig is (instanties, uitkomsten, tijd) |
| 8 | Tegenlezing | kritisch | de advocaat een conceptstuk aanlevert ter toetsing |
| 9 | Monitorrapport | neutraal, headless | een geplande run alleen het nieuwe sinds een peildatum moet melden |
| 10 | Dossiernotitie | intern | het onderzoek in het dossier moet landen voor collega's |

## 1 Onderzoeksmemo
Rechtsvraag en aannames · Conclusie vooraf · Juridisch kader (wet en geschiedenis; dragende artikelen
integraal) · Rechtspraak naar hiërarchie (kernoverwegingen letterlijk met r.o.) · Literatuur en praktijk
(letterlijke citaten) · Tegenargumenten en risico's · Conclusie en vervolgstappen · Bronnen · Zoeklog.

## 2 Adviesnotitie
Vraag · Advies in vijf zinnen · Onderbouwing (puntsgewijs, met noten) · Risico's en tegenargumenten ·
Vervolgstappen · Bronnen · Zoeklog (bijlage).

## 3 Bronnenoverzicht
Per bron: nummer, titel of ECLI (link), instantie of auteur, datum, status, één zin relevantie, letterlijk
citaat (web) of kernoverweging met r.o. (officieel). Gegroepeerd: wet · rechtspraak · literatuur · overig.
Zoeklog (bijlage).

## 4 Wetenschappelijk onderzoek
Samenvatting met trefwoorden · 1 Inleiding (aanleiding, hoofdvraag, deelvragen, afbakening) · 2 Methode
(zoekstrategie, inclusie en exclusie, analysematrix, bronkritiek, reproduceerbaarheid, beperkingen) ·
3 Juridisch kader · 4 Resultaten per thema, elk met een alinea "Interpretatie" · 5 Discussie (wat de selectie
wel en niet kan dragen) · 6 Conclusie (antwoord op de hoofdvraag, vervolgonderzoek, transparantie) ·
Bijlage A Analysematrix (tabel: nr, ECLI, instantie, datum, uitkomst, thema, r.o.; vooraf een telling per
instantie en uitkomst) · Bronnenlijst met status · Bijlage B Zoeklog · Bijlage C Kernwetgeving (integraal).
Citeerstijl: Leidraad voor juridische auteurs (ECLI met r.o.; literatuur: auteur, titel, tijdschrift jaar/nr,
pagina). Neutraal, geen advies; beperkingen expliciet; nooit "peer-reviewed" claimen.

## 5 Processtuk-onderbouwing
Partij en processuele positie · Per stelling (genummerd): de stelling, juridische grondslag (artikelen
integraal waar dragend), dragende bronnen met r.o. en letterlijk citaat, te verwachten tegenargumenten en
weerlegging, benodigde bewijspunten · Zwakke plekken (eerlijk) · Bronnen · Zoeklog. Toon: zakelijk, geschikt
om over te nemen; geen beloftes over de uitkomst.

## 6 Cliëntbrief
Kantoorbriefstijl (aanhef, onderwerp, datum): wat de vraag was · wat de regels zeggen in gewone taal ·
wat dat voor de cliënt betekent · opties met voor- en nadelen · voorgesteld vervolg · voorbehoud · bijlage
met bronnen (korte lijst, status) · disclaimer in de bijlage. Geen ECLI-jargon in de brief zelf; de advocaat
ondertekent.

## 7 Rechtspraakkaart
Samenvattende tabellen (per instantie, per uitkomst, per jaar) · Chronologie (tabel: datum, ECLI, instantie,
uitkomst, thema, één zin) · Thematische clusters · Opvallende lijnen en breuken (feitelijk, geen voorspelling)
· Bronnen · Zoeklog. Daarnaast dezelfde matrix als CSV-bestand.

## 8 Tegenlezing
Samenvatting van het conceptstuk · Per juridische stelling uit het stuk: citaat van de stelling, status
(gedragen · deels gedragen · niet gedragen · onjuist), dragende of weerleggende bron met r.o., voorgestelde
correctie · Ontbrekende bronnen die het stuk zouden versterken · Bronnen · Zoeklog. Het conceptstuk zelf
wordt niet als zoekterm meegestuurd; abstraheer naar rechtsbegrippen.

## 9 Monitorrapport
Peildatum en venster · Nieuw sinds de peildatum (per bron: link, datum, kern, waarom relevant) · Verschillen
met de vorige run (indien bekend) · Signalen om op te letten · Bronnen · Zoeklog. Compact; headless.

## 10 Dossiernotitie
Zaakkenmerk (geabstraheerd) · Feiten (geabstraheerd, geen namen of bedragen) · Rechtsvragen · Stand van het
recht per rechtsvraag met bronnen · Vervolgstappen en termijnen · Open punten · Bronnen · Zoeklog.
