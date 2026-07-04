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
- **Nevenbetrekkingen:** de tool haalt hoofdfunctie én actuele nevenbetrekkingen live uit
  het officiële rechtersregister (namenlijst.rechtspraak.nl) op; ze staan in
  `nevenbetrekkingen_register`. Dit zijn feitelijke, volledige registergegevens (in
  tegenstelling tot het uitsprakenbeeld). Toon ze zoals aangeleverd, met de ingangsdatum en
  of de functie bezoldigd is. Regels:
  - `gevonden: true` → toon hoofdfunctie(s) en de nevenbetrekkingen. Is
    `geen_opgave_nevenbetrekkingen: true` of de lijst leeg, meld dan "geen nevenbetrekkingen
    opgegeven in het register".
  - Ontbreekt `gevonden` en staat er een `status` met `kandidaten` → er zijn naamgenoten en
    geen eenduidige match; toon de kandidatenlijst en vraag de gebruiker te preciseren
    (volledige voorletters), gok nooit zelf een persoon.
  - Ontbreekt `gevonden` zonder kandidaten → register even niet bereikbaar of niet gevonden;
    verwijs naar de `register_url`. Haal nevenbetrekkingen nooit uit webresultaten of geruchten.

## Outputformat

```
## <Naam>
**Hoofdfunctie (register):** <functie> @ <instantie> (sinds <datum>)
**Uitsprakenbeeld (eigen index):** <aantal> gepubliceerde uitspraken · per instantie: <verdeling>
**Recente uitspraken:**
1. <ECLI> — <datum> · <rol> · [bekijk →](<bron_url>)
…
**Nevenbetrekkingen (officieel register):**
- <functie> — <organisatie> · <bezoldigd?> · sinds <datum>
…
**Kanttekening:** <de fairness-kanttekening uit de tool-output>
_Bron nevenbetrekkingen: officieel rechtersregister (<register_url>)._
```

Geen match? Meld dat de index dagelijks groeit en vraag om de notatie voorletters +
achternaam. Sluit af met de standaarddisclaimer.
