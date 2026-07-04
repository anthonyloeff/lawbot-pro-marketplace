---
name: opstellen
description: Concepten van juridische stukken opstellen (memo, conclusie van antwoord, sommatie/ingebrekestelling) met bronverwijzingen en Word/PDF-export. MOET actief worden bij /lawbot-pro:opstellen, "schrijf een memo over", "stel een sommatie op", "maak een conclusie van antwoord", of als vervolg op een documentanalyse.
---

# Stukken opstellen

## Werkwijze

1. **Stukstype bepalen** en het bijbehorende skelet uit `templates/` in deze skill-map
   gebruiken (memo.md, conclusie-van-antwoord.md, sommatie.md). Vraag vooraf kort de
   huisstijlgegevens: kantoornaam/ondertekenaar, wederpartij, dossierkenmerk, gewenste toon.
2. **Eerst onderzoek, dan schrijven.** Elk juridisch standpunt in het stuk moet steunen op
   tool-geverifieerde bronnen (skill `juridisch-onderzoek`). Het opnemen van
   niet-geverifieerde verwijzingen is verboden — liever een [PM]-merkteken dan een
   verzonnen vindplaats.
3. **Opbouw:** genummerde randnummers; verwijzingen als voetnoten met volledige vindplaats
   én link (ECLI met deeplink, artikel met jci-link).
4. **Export:** lever in Cowork het stuk als Word-document (docx-skill) of PDF op verzoek,
   in de outputs-map. Buiten Cowork: nette markdown met de melding dat export in Cowork kan.
5. **Concept-markering** (verplicht in het document zelf, onderaan):
   > *Concept — gegenereerd met LawBot Pro (Litic.ai). Controle door een advocaat is
   > vereist vóór verzending of indiening.*

## Kwaliteitseisen

- Memo's: conclusie vooraf (advocaten lezen bottom-line-up-front), daarna analyse,
  risico's & tegenargumenten, advies.
- Processtukken: feiten en weren strikt scheiden; per weer de grondslag + bron.
- Sommaties: concrete verplichting, redelijke termijn met datum, aangekondigd rechtsgevolg.
