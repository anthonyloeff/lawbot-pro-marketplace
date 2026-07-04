---
name: wetten
description: Nederlandse wetsartikelen opzoeken (actueel of historisch). MOET actief worden bij het tekstcommando "W:" (bijv. "W: 6:162 BW"), /lawbot-pro:wet, of vragen als "wat zegt artikel 7:658 BW", "tekst van art. 4:81 Awb", "gold dit artikel al in 2019", "welke versie van de wet".
---

# Wetsartikelen (W:)

## Werkwijze

1. **Parseer de aanduiding.** Herkende notaties: `6:162 BW`, `art. 7:658 BW`, `Awb 4:81`,
   `310 Sr`, `artikel 162 boek 6 BW`. Geef bij `zoek_wet` de notatie gewoon door via het
   `artikel`-veld — de server parseert zelf. Nooit een artikeltekst uit eigen kennis geven.
2. **Actuele tekst:** roep `zoek_wet` aan. Toon de artikeltekst **integraal, per lid**
   (blockquote), met citeertitel, geldigheidsdatum en de jci-deeplink als bronlink.
3. **Historische vraag** ("gold dit in 2019?", overgangsrecht): geef `peildatum` mee aan
   `zoek_wet`. Vergelijk bij overgangsrechtvragen de oude en nieuwe tekst naast elkaar,
   elk met eigen deeplink. Gebruik `wet_versies` om de relevante toestanden te vinden.
4. **Ambiguïteit** (meerdere kandidaten in de tool-output): stel één korte
   verduidelijkingsvraag met de kandidaten en hun BWBR-id's.

## Verdieping (op verzoek of bij duidelijke aanleiding)

- **Rechtspraak bij dit artikel** → `jurisprudentie_bij_artikel` (officiële LiDO-citatiegraaf);
  toon de top-5 met hoogste instantie eerst en bied volledige analyse aan via `haal_uitspraak`.
- **Bedoeling van de wetgever** → `wetsgeschiedenis` (memorie van toelichting); vermeld het
  kamerstuknummer met deeplink.

## Outputformat

```
### <Citeertitel> — artikel <nr>
> 1. <tekst lid 1>
> 2. <tekst lid 2>

**Vindplaats:** [<jci of wetten.overheid.nl-link>](<bron_url>) · geldig op <datum>
**Kern in gewone taal:** <2-3 zinnen>
```

Vervolgsuggesties: rechtspraak bij dit artikel, wetsgeschiedenis, historische versies.
Sluit af met de standaarddisclaimer uit de skill `juridisch-onderzoek`.
