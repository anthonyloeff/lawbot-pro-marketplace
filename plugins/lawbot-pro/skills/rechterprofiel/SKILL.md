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
- Nevenbetrekkingen: verwijs uitsluitend naar het officiële register
  (https://namenlijst.rechtspraak.nl/), nooit naar geruchten of webresultaten.

## Outputformat

```
## <Naam>
**Uitsprakenbeeld (eigen index):** <aantal> gepubliceerde uitspraken · per instantie: <verdeling>
**Recente uitspraken:**
1. <ECLI> — <datum> · <rol> · [bekijk →](<bron_url>)
…
**Nevenbetrekkingen:** raadpleeg het officiële register: https://namenlijst.rechtspraak.nl/
**Kanttekening:** <de fairness-kanttekening uit de tool-output>
```

Geen match? Meld dat de index dagelijks groeit en vraag om de notatie voorletters +
achternaam. Sluit af met de standaarddisclaimer.
