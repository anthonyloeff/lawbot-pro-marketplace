# Stijlgids LawBot Pro-rapporten ("quiet library")

Alle rapporten van deep research volgen deze gids. De sjabloon `rapport_sjabloon.py` past hem automatisch
toe; deze tekst is de bron van waarheid als je zelf iets moet beslissen.

## Kleuren (tokens)

| Token | Hex | Gebruik |
|---|---|---|
| papier | #f5f0e8 | kaders (samenvatting, conclusie vooraf, vervolg), zebra-rijen in tabellen |
| kaart | #fdfbf7 | lichte kaders |
| inkt | #54483f | lopende tekst |
| inkt-zacht | #6f6155 | bijschriften, kolomkoppen, noten |
| lijn | #ddd5c9 | haarlijnen |
| lijn-zacht | #e9e2d6 | tabelranden |
| salie | #9b9a86 | metadata, paginanummers |
| groen | #5f6f62 | koppen, links, badge "officieel" (tekst) |
| groen-donker | #4c5a50 | cover, kopregels |
| groen-tint | #eaece7 | tabelkop, badge "officieel" (vlak) |
| oker | #b07d1e | sectienummers, kaderlabels, accentstreep |
| oker-tint | #f2e7cd | badge "web, geciteerd" |
| fout | #a4453b | badge "niet gevonden", waarschuwing |
| grijs-tint | #ebe8e2 | badge "niet open toegankelijk" |

## Typografie

- Serif: Source Serif 4 (Regular, Italic, Semibold, Bold) voor titels, lopende tekst en citaten.
- Sans: Plus Jakarta Sans (Regular, SemiBold, Bold, Italic) voor kaderlabels, tabellen, bijschriften,
  noten, colofon, kop- en voetregels.
- Terugval als de fonts niet laden: DejaVu Serif en DejaVu Sans (altijd aanwezig in de sandbox).
- Maten: titel 26 pt; hoofdstukkop 18 pt serif; paragraafkop 11,5 pt sans semibold; lopende tekst 10,5 pt
  serif op 15 pt; tabellen 8,8 pt sans; noten en colofon 8 pt sans; kaderlabel 7,5 pt sans, kapitalen,
  letterspatiëring.

## Pagina en ritme

- A4 staand, marges 22 mm, leesbreedte circa 166 mm.
- Kopregel: links "LAWBOT PRO / [VORM]" in kaderlabel-stijl, rechts de datum; haarlijn eronder.
- Voetregel: links de titel in kapitalen, rechts "pagina / totaal".
- Cover: donkergroen vlak, kaderlabel in oker ("JURIDISCH ONDERZOEK / [RECHTSGEBIED]"), korte oker-streep,
  titel en ondertitel in serif wit, metadata-regels (perspectief, aantal bronnen, peildatum) in sans
  kapitalen, onderaan het LawBot Pro-logo met "Onderzoeksassistent van Litic" en het Litic-logo (licht).
- Pagina 2: inhoudsopgave plus compact colofon in twee kolomparen (opdrachtgever/kantoor, verantwoordelijk
  advocaat, auteur, vorm, diepte, perspectief, peildatum, datum, versie, waarmerk) met bronroutes en disclaimer
  over de volle breedte; past de inhoud niet meer, dan schuift het colofon naar pagina 3.
- Hoofdstukken lopen door op de pagina; alleen cover, inhoud, bijlagen en bronnenlijst beginnen op een
  nieuwe pagina. Geen halflege pagina's door paginaovergangen per paragraaf.
- Sectienummering: "1 | INLEIDING" als kaderlabel in oker boven de hoofdstukkop.
- Tabellen: kopregel in groen-tint, zebra in papier, alleen horizontale haarlijnen in lijn-zacht, tekst 8,8 pt
  sans; getallen rechts uitgelijnd; ECLI's als link in groen.
- Statusbadge per bron: afgeronde pil, tekst in sans 7,5 pt semibold: officieel (groen-tint/groen) ·
  web, geciteerd (oker-tint/oker) · niet gevonden (fout, wit) · niet open toegankelijk (grijs-tint/inkt-zacht).
- Noten: per hoofdstuk onder de tekst ("Noten"), 8 pt sans, nummer in groen; in de tekst als [n].
- Citaten: serif cursief, links een oker-streep, inspringing 8 mm.
- Kaders (samenvatting, conclusie vooraf, vervolgsuggesties): vlak in papier met een oker-streep links van 2 pt,
  kaderlabel in oker, tekst serif 10 pt; korte kaders blijven bijeen, lange splitsen per alinea.
- Nooit em-dashes in de tekst; geen prijzen of verkooptaal; disclaimer letterlijk uit de briefing.
