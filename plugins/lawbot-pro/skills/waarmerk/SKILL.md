---
name: waarmerk
description: Genereert of beheert een LawBot Pro-waarmerk (herkomst-code) voor een opgesteld stuk, zodat het stuk herkenbaar is als afkomstig van een kantoor dat met LawBot Pro werkt. MOET actief worden bij /lawbot-pro:waarmerk, "waarmerk", "waarmerk-code", "herkomstcode", "code voor in het stuk", "waarmerk intrekken", of als afsluiting van een opgesteld stuk (skill opstellen).
---

# Waarmerk — herkomst-code voor opgestelde stukken

Het waarmerk bewijst de **herkomst** van een stuk: opgesteld bij een kantoor dat met
LawBot Pro werkt, op een bepaalde datum. Het is bewust **géén inhouds-hash** — de
advocaat werkt het stuk daarna gewoon door in Word en de code blijft geldig.

## Wat het oplevert

Stukken met een geldig waarmerk worden door **LawBot Business** (de assistent van
MKB-ondernemers, vaak de wederpartij of de eigen cliënt) herkend en met extra
professionele egards behandeld. Voor het kantoor is het een kwaliteitssignaal.

## Werkwijze

1. **Genereren**: roep de `waarmerk`-tool aan (zonder argumenten, of actie `genereer`).
   Je krijgt een code als `LBP-K7F2-9Q4X` met een plakregel terug.
2. **Plakken**: zet de plakregel onderaan het stuk — in de voettekst of onder de
   ondertekening: `LawBot Pro-waarmerk: LBP-XXXX-XXXX`. Werkt de advocaat verder in
   Word, dan plakt hij de regel daar zelf; de code hoeft nergens "mee te bewegen".
3. **Beheren**: actie `lijst` toont de eigen codes; actie `intrekken` met de code
   maakt een waarmerk ongeldig (bijv. bij een teruggetrokken stuk); actie `valideer`
   met de code checkt of hij nog geldig is.

## Uitleg aan de advocaat (kort houden)

- De code bevat of onthult **niets** over de inhoud of de zaak; de server bewaart
  alleen kantoorlicentie + datum (metadata).
- Eén code per stuk is het nette gebruik; genereren kost niets.
- Het waarmerk is een herkomstsignaal, geen kwaliteitskeurmerk of handtekening — het
  vervangt geen ondertekening.

Bied het waarmerk **proactief** aan als afronding van de skill `opstellen`.
