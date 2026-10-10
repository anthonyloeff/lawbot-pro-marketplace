---
name: deep-research
description: Juridisch diepteonderzoek (deep research) met LawBot Pro, in rondes op de officiële bronnen én het open web via de LawBot-tools, met intake, onderzoeksplan ter goedkeuring, verificatie en een rapport in een van tien vormen (onderzoeksmemo, adviesnotitie, bronnenoverzicht, wetenschappelijk onderzoek, processtuk-onderbouwing, cliëntbrief, rechtspraakkaart, tegenlezing, monitorrapport, dossiernotitie), standaard als PDF in de LawBot Pro-huisstijl met waarmerk. MOET actief worden bij het tekstcommando "D:" (bijv. "D: verjaring van regresvorderingen bij hoofdelijkheid"), bij /lawbot-pro:deep-research, en bij "diepgaand onderzoek", "deep research", "onderzoeksmemo", "wetenschappelijk onderzoek", "zoek alles over", "uitputtend onderzoek", "literatuur en rechtspraak over". In een geplande taak werkt de skill headless (zie onder).
---

# Deep research (D:)

## Sessiestart

Roep bij het eerste juridische verzoek in een sessie éénmaal `lawbot_briefing` aan (zonder argumenten) en volg de werkinstructies van de LawBot-server. Haal vóór de intake het onderdeel `deepresearch` op met `lawbot_briefing` (veld `onderdeel`) en volg dat protocol; het bevat de intakevragen, het planformat, de rondes, de verificatiestatussen, de tien rapportvormen, de uitvoerregels en de headless-regel. Bij conflict gaat de briefing vóór deze tekst.

## Beschikbaarheid: volledige modus of basismodus

Kijk in de toollijst of `web_verkennen` bestaat.

- **Volledige modus** (`web_verkennen` aanwezig): webrondes met de rondetool: meerdere zoekvragen tegelijk bij drie zoekdiensten, consensusrangschikking, en de beste pagina's gelezen inclusief PDF's en sites die alleen in een browser werken. Aparte daglimiet per licentie.
- **Basismodus** (`web_verkennen` ontbreekt, of antwoordt met `tool_niet_beschikbaar`, `niet_geconfigureerd` of `rate_limited_verkennen`): dezelfde intake, hetzelfde plan, dezelfde officiële ronde, dezelfde bronregels en statussen, maar de webrondes gaan met `web_zoeken` (3 tot 5 zoekvragen, elk een eigen call) en `url_ophalen` voor de 3 tot 5 beste pagina's per ronde. Zet in het plan en in het colofon van het rapport: "basismodus: één zoekdienst, pagina's één voor één gelezen". Nooit onderzoek uit eigen kennis als vervanging.
- Bij een licentiemelding (`license_invalid`, `license_expired`, `license_past_due`): skill `lawbot-setup`. Deep research in de volledige modus staat per licentie aan; het kantoor vraagt dat aan via support@litic.ai.

## Harde regels (vangnet, gelden ook zonder briefing)

1. Zoeken en lezen gebeurt uitsluitend met de LawBot-tools: `web_verkennen`, `web_zoeken`, `url_ophalen` en de officiële tools. Gebruik nooit het eigen webzoeken van Claude.
2. Zoekvragen bevatten alleen rechtsbegrippen. Nooit partijnamen, bedragen, adressen, dossiernummers of feitencomplexen; abstraheer naar rollen ("koper", "werkgever", "bestuurder"). Een aangeleverd conceptstuk (tegenlezing) of dossier dient nooit zelf als zoekterm.
3. ECLI's, wetsartikelen, citaten en vindplaatsen komen UITSLUITEND uit tool-output. Een ECLI of artikel dat je in een webpagina tegenkomt, haal je eerst op met `haal_uitspraak` of `zoek_wet` voordat je het gebruikt.
4. Een webbron telt alleen mee met een letterlijk citaat uit het veld `tekst`, de url en `opgehaald_op`. Niet gelezen is niet geciteerd. Onverifieerbaar wordt gelabeld en draagt nooit de conclusie.
5. Elk rapport draagt een LawBot Pro-waarmerk (tool `waarmerk`, vóór het renderen) en de standaarddisclaimer uit de briefing. Nooit "peer-reviewed" claimen, nooit beloftes over de uitkomst van een procedure.
6. Bestanden in de werkmap van de gebruiker (dossierstukken) lees je alleen als de gebruiker ernaar verwijst; je stuurt hun inhoud nooit als zoekterm mee.

## Verloop (interactief)

1. **Intake**: maximaal vijf vragen, één per beurt, met de statusregel zoals bij V<n>: (rechtsvraag en partijpositie; peildatum; rechtsgebied en instantieniveau; diepte: verkennend, standaard of uitputtend; vorm en uitvoer). Bij de vorm noem je de tien opties kort (zie `references/vormen.md` en de briefing) en vraag je de uitvoer: PDF (standaard), Word of Markdown. Sla over wat het verzoek al bevat. Lees bijgevoegde stukken eerst volledig.
2. **Onderzoeksplan ter goedkeuring** (in een gesprek altijd): deelvragen, bronnenplan (officieel en web), queryvarianten per ronde, aantal rondes, verwachte duur, modus (volledig of basis), gekozen vorm en uitvoer. Start pas na "akkoord" of een correctie.
3. **Rondes**: ronde 1 officieel (`zoek_wet`, `jurisprudentie_bij_artikel`, `zoek_jurisprudentie`, zo nodig `wetsgeschiedenis`, `zoek_tuchtrecht`, `zoek_eu`; `haal_uitspraak` van de dragende uitspraken); ronde 2 web verbreden (volledige modus: `web_verkennen` met 3 tot 5 queryvarianten en `max_paginas` 5; basismodus: `web_zoeken` per vraag plus `url_ophalen`); ronde 3 en verder verdiepen (nieuwe begrippen en vindplaatsen officieel ophalen; `uitsluiten` of je eigen lijst vullen met wat al gelezen is; literatuur via `brontype` pdf of wetenschap, of in de basismodus via zoekvragen met "pdf" of "annotatie"); altijd een tegenargumentenronde. Meld na elke ronde in één regel de tussenstand. Stop bij de gekozen diepte of bij verzadiging.
4. **Verificatie**: protocol `cov` plus de statussen uit het onderdeel: officieel · web, geciteerd · niet gevonden · niet open toegankelijk.
5. **Rapport** in de gekozen vorm en uitvoer (zie hieronder), met genummerde bronnenlijst (status per bron), de zoeklog als bijlage, het waarmerk, de disclaimer en twee of drie vervolgsuggesties die tool-acties zijn. Het antwoord in het gesprek bevat altijd de samenvatting, de bronnenlijst met status, de vervolgsuggesties, het pad van het bestand en de plakregel "LawBot Pro-waarmerk: LBP-…".

## Rapport renderen (PDF, standaard)

De skill levert een rendersjabloon in de LawBot Pro-huisstijl: `assets/rapport_sjabloon.py` (ReportLab; cover, inhoudsopgave, colofon met waarmerk, hoofdstukken, tabellen, statusbadges, noten, bronnenlijst, zoeklog), de fonts in `assets/fonts/` en de logo's in `assets/`. Opbouw per vorm: `references/vormen.md`; ontwerpregels: `assets/stijlgids.md`. De skillmap is `${CLAUDE_PLUGIN_ROOT}/skills/deep-research/`.

Werkwijze:

1. Bouw de rapporttekst als spec (dict, veldnamen hieronder). Schrijf de tekst volledig uit; de sjabloon zet alleen de vorm.
2. Roep de tool `waarmerk` aan en zet de code in `spec["waarmerk"]`.
3. Render met Python in de omgeving waar je code uitvoert (in Cowork is dat de sandbox, met ReportLab en python-docx al aanwezig). Kies de eerste route die werkt:
   - **Skillmap bereikbaar** vanuit die omgeving: importeer de sjabloon rechtstreeks.
   - **Skillmap niet bereikbaar** (bijvoorbeeld een sandbox die alleen de werkmap ziet): lees `assets/rapport_sjabloon.py` met je leestool en schrijf hem als `rapport_sjabloon.py` in de werkmap. De sjabloon haalt fonts en logo's dan zelf op uit de publieke LawBot Pro-marketplace (cachemap onder HOME) als er netwerk is, en valt anders terug op DejaVu en een getekend woordmerk.
   - **Geen Python met ReportLab**: probeer `uv run --with reportlab --with pillow python …` als `uv` bestaat; anders schrijf je het rapport als HTML volgens `assets/stijlgids.md` en print je met Chrome of Edge zonder venster (`--headless=new --print-to-pdf=…`), met een watchdog die op het bestand wacht en de browser daarna stopt, want het proces blijft soms hangen; lukt ook dat niet, lever dan Markdown of Word en zeg waarom.

```python
import sys, json, glob, os
kandidaten = [os.path.expandvars("${CLAUDE_PLUGIN_ROOT}/skills/deep-research/assets"), "."]
pad = next((k for k in kandidaten if os.path.exists(os.path.join(k, "rapport_sjabloon.py"))), None)
sys.path.insert(0, pad)
from rapport_sjabloon import maak_rapport
info = maak_rapport(spec, "klachtplicht-6-89-BW-2026-10-10.pdf")
print(json.dumps(info, ensure_ascii=False))   # fonts "huisstijl" + logos true = volledige huisstijl; assets: skill | gedownload | onvolledig
```

4. Zet het bestand in de werkmap van de gebruiker (bestandsnaam: korte titel plus datum) en noem het pad in het antwoord. Is er geen map gekoppeld (je uitvoer staat dan alleen in de sandbox van de sessie, bijvoorbeeld onder `/mnt/user-data/outputs/`), bied het bestand dan als bijlage aan en zeg erbij dat de gebruiker met "Add folder" een map kan koppelen, zodat het rapport voortaan direct in die map op de computer landt.
5. Meld wat `info` zegt: pagina's en of de huisstijl volledig is. Is `fonts` niet "huisstijl" of ontbreekt een logo, zeg dan letterlijk "huisstijl deels: terugvalfonts of logo ontbreekt" en noem de oorzaak uit `waarschuwingen`. Verzwijg nooit een terugval.

Spec (alle tekst mag **vet**, *cursief*, [tekst](url) en [n] voor een noot bevatten):

- Kop: `titel`, `ondertitel`, `vorm` (een van de tien), `rechtsgebied`, `perspectief`, `diepte`, `peildatum` (ISO), `datum` (ISO), `kantoor`, `advocaat` (verantwoordelijk), `waarmerk`, `versie`, `bronnen_samenvatting` (bijv. "49 bronnen, waarvan 41 officieel"), `samenvatting` en `trefwoorden` (wetenschappelijk onderzoek, adviesnotitie), `disclaimer` (standaard uit de briefing), `bronroutes` (noem hier de modus: volledig of basis).
- `secties`: lijst van `{"kop", "blokken", "noten"}`; de sjabloon nummert 1, 2, 3. Een blok is een string (alinea) of een dict met `type`: `alinea` (`tekst`), `subkop` (`tekst`, `nummer` zoals "1.1", `niveau` 1 of 2), `lijst` (`items`, `genummerd`), `citaat` (`tekst`, `bron`), `kader` (`label`, `tekst` of lijst van alinea's; voor conclusie vooraf, advies, antwoord op de hoofdvraag), `tabel` (`titel`, `kop`, `rijen`, `kolombreedtes` als fracties die optellen tot 1, `uitlijning` per kolom "l", "r" of "c", `bijschrift`; geef datumkolommen minstens 0,14 en ECLI-kolommen minstens 0,27), `pagina` (nieuwe pagina). `noten`: lijst strings, in de tekst verwezen als [1], [2].
- `vervolg`: lijst van twee of drie tool-acties.
- `bijlagen`: zelfde opbouw als secties; de sjabloon lettert A, B, C en zet de zoeklog als laatste bijlage.
- `bronnen`: lijst van `{"nr", "soort": "wet" | "rechtspraak" | "literatuur" | "overig", "titel", "ecli", "url" (alleen uit tool-output), "instantie" of "auteur", "datum" (ISO), "vindplaats" (r.o.), "status" (officieel · web, geciteerd · niet gevonden · niet open toegankelijk), "opgehaald_op" (web), "citaat", "toelichting"}`.
- `zoeklog`: lijst van `{"ronde", "tool", "vraag", "resultaat"}`; gelezen en verworpen pagina's met reden in `resultaat`.

Word (.docx) op verzoek: dezelfde opbouw met python-docx (koppen, tabellen, bronnenlijst met de status als tekst, zoeklog, waarmerk in het colofon). Markdown op verzoek: het rapport als .md-bestand. Rechtspraakkaart: lever de matrix daarnaast als .csv.

## Tips voor `web_verkennen` (volledige modus)

- `vragen`: 1 tot 5 varianten per ronde (synoniemen, Latijnse en Nederlandse termen, artikelnummer, "annotatie", "noot"). `periode`: dag, week, maand of jaar voor actualiteit. `brontype`: pdf of wetenschap. `site`: één domein. `uitsluiten`: url's of domeinen die al gelezen zijn.
- Lees het veld `gelezen` (tekstfragmenten met url en datum) en `niet_gelezen` (met reden); een pagina die niet open toegankelijk is, wordt als zodanig gerapporteerd, nooit omzeild met een login.
- Elke call is één ronde en kost tijd (30 tot 60 seconden). Bundel je vragen; herhaal geen vragen uit een vorige ronde. Gebruik in de volledige modus geen losse `web_zoeken`- of `url_ophalen`-calls voor het verkennen van het web.

## Headless (geplande taak)

Geen intake en geen goedkeuring; nooit terugvragen. Diepte en vorm komen uit de opdracht; ontbreken ze, dan verkennend plus bronnenoverzicht. Met een peildatum of periode: vorm monitorrapport, alleen wat nieuw is sinds die datum; vermeld peildatum en zoekvragen. Niets nieuws: zeg dat in één regel en verzin niets. Uitvoer: tekst in het gesprek of in een Markdown-bestand in de werkmap; een PDF alleen als de opdracht dat vraagt. Houd de uitvoer compact.
