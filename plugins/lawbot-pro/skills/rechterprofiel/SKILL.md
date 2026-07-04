---
name: rechterprofiel
description: Feitelijk profiel van een Nederlandse rechter of raadsheer. MOET actief worden bij het tekstcommando "R:" (bijv. "R: mr. J. de Groot"), /lawbot-pro:rechter, of "wie is rechter …", "wat weet je over raadsheer …".
---

# Rechterprofiel (R:)

## Werkwijze

Roep `rechter_profiel` aan met voorletters + achternaam (zoals in uitspraken gebruikelijk;
strip aanhef zoals "mr."). Bij naamgenoten: disambigueer via gerecht of periode voordat
je rapporteert.

## Fairness-regels (essentieel voor een professioneel product)

- Het profiel is **beschrijvend, niet voorspellend**. Nooit uitspraken als "deze rechter
  wijst vaak af" — ook niet met cijfers erbij: zaakstoedeling en zaakzwaarte maken zulke
  vergelijkingen ondeugdelijk. Neem de kanttekening uit de tool-output altijd over.
- De index bevat alleen GEPUBLICEERDE uitspraken — een fractie van iemands werk. Benoem dat.
- **Nevenbetrekkingen:** deze worden bewust **niet automatisch opgehaald**. Het officiële
  register (namenlijst.rechtspraak.nl) staat geautomatiseerde toegang niet toe en heeft geen
  open data-API; wij scrapen geen bronnen die dat verbieden. Presenteer dit als een
  weloverwogen keuze, geen gemis: geef de gebruiker de directe zoeklink naar het register —
  `https://namenlijst.rechtspraak.nl/#/result?q=<achternaam>` — zodat hij het gezaghebbende
  overzicht met één klik in zijn browser opent. Haal nevenbetrekkingen nooit uit
  webresultaten of geruchten.

## Outputformat

```
## <Naam>
**Uitsprakenbeeld (eigen index):** <aantal> gepubliceerde uitspraken · per instantie: <verdeling>
**Recente uitspraken:**
1. <ECLI> — <datum> · <rol> · [bekijk →](<bron_url>)
…
**Nevenbetrekkingen:** het officiële register (bewust niet automatisch opgehaald) — open met één klik: https://namenlijst.rechtspraak.nl/#/result?q=<achternaam>
**Kanttekening:** <de fairness-kanttekening uit de tool-output>
```

Geen match? Meld dat de index dagelijks groeit en vraag om de notatie voorletters +
achternaam. Sluit af met de standaarddisclaimer.
