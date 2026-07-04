---
name: uitspraak-analyse
description: Eén rechterlijke uitspraak volledig analyseren en samenvatten. MOET actief worden bij het tekstcommando "S:" gevolgd door een ECLI (bijv. "S: ECLI:NL:HR:2023:1371"), /lawbot-pro:uitspraak, een geplakte rechtspraak.nl-link, of "vat dit arrest samen", "analyseer deze uitspraak", een los ECLI of oud LJN.
---

# Uitspraakanalyse (S:)

## Werkwijze

1. Haal de **volledige tekst** op met `haal_uitspraak` (accepteert ECLI's, rechtspraak-links
   en oude LJN's). Bij `paginas_totaal > 1`: haal álle pagina's op vóór je samenvat.
2. Is er alleen metadata (`alleen_metadata: true`)? Meld dat eerlijk en geef de
   inhoudsindicatie + deeplink; verzin geen tekst.
3. Samenvatten doe je **op basis van de volledige tekst** — nooit alleen op de
   inhoudsindicatie.
4. **Verrijk uit de metadata:** formele relaties (conclusie A-G, eerdere aanleg — bied aan
   die óók op te halen), vindplaatsen (NJ/AB/NTFR), wetsverwijzingen (met jci-links).

## Outputformat (vaste kopjes)

```
## <ECLI> — <instantie>, <datum>
[Volledige uitspraak →](<bron_url>)

**Kern in 3 zinnen:** <de essentie voor een haastige advocaat>

**Partijen & procesverloop:** <incl. eerdere aanleg met ECLI-links uit formele_relaties>
**Feiten:** <kort>
**Rechtsvraag:** <de kernvraag(en), met relevante artikelen>
**Standpunten partijen:** <eis/verweer>
**Oordeel & dragende overwegingen:** <analyse; citeer de dragende overweging LETTERLIJK
  met het r.o.-nummer — parafrase mag aanvullend, maar de kernoverweging altijd als citaat>
**Dictum:** <letterlijk>
**Betekenis voor de praktijk:** <plaatsing in de lijn van de rechtspraak>
**Metadata:** zaaknummer · proceduresoort · rechtsgebied · vindplaatsen · wetsverwijzingen (met links)
```

Vervolgsuggesties: conclusie A-G of eerdere aanleg analyseren, vergelijkbare rechtspraak
zoeken, het centrale wetsartikel opvragen. Sluit af met de standaarddisclaimer.
