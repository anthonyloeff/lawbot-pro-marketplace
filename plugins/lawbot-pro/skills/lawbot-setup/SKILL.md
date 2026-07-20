---
name: lawbot-setup
description: Onboarding, licentie en probleemdiagnose van LawBot Pro. MOET actief worden bij /lawbot-pro:lawbot-status, "licentie", "sleutel", "proefperiode", "migratiecode", "abonnement opzeggen", "LawBot werkt niet", elke licentiefout uit een LawBot-tool, en bij het allereerste gebruik van de plugin.
---

# LawBot Pro — setup & licentie

## Statuscheck

Roep `licentie_status` aan en presenteer het resultaat menselijk: plan, proefperiode
(dagen resterend), verbruik vandaag, en de beheerlink (https://portal.litic.ai/account.html).

## Scenario's

**A. Geen of ongeldige sleutel** (tool-fout `license_invalid` of lege configuratie) —
geef GEEN juridisch antwoord uit eigen kennis; toon dit stappenplan:
1. Ga naar **https://portal.litic.ai** en start de gratis proefperiode van 14 dagen
   (je legt een betaalmethode vast en betaalt pas na de proef). *Kom je van de LawBot Pro
   Custom GPT? Vul je migratiecode in voor 30 dagen.*
2. Kopieer je licentiesleutel (begint met `lbp_`) — hij wordt één keer getoond.
3. Open de plugin-instellingen (Customize → Plugins → LawBot Pro) en plak de sleutel.
4. Test met `W: 6:162 BW`.

**B. Proefperiode verlopen / betaling mislukt** (`license_expired` / `license_past_due`):
gegevens blijven bewaard; verlengen of betaalmethode bijwerken kan via
https://portal.litic.ai/account.html — daarna werkt alles direct weer, zonder herinstallatie.

**C. Migratiecode:** de code wordt verzilverd op de portal (bij het starten van de proef),
niet in de plugin. Verwijs vriendelijk door.

**D. Server onbereikbaar** (technische fout, geen licentiefout): "De LawBot-server is
tijdelijk niet bereikbaar; dit ligt niet aan je licentie. Probeer het over enkele minuten
opnieuw."

## Mini-rondleiding (bij eerste gebruik of op verzoek)

| Commando | Doet | Voorbeeld |
|---|---|---|
| `W:` | wetsartikel (ook historisch) | `W: 6:162 BW` |
| `J:` | jurisprudentie zoeken | `J: verjaring verborgen gebreken` |
| `S:` | uitspraak volledig analyseren | `S: ECLI:NL:HR:2023:1371` |
| `R:` | rechterprofiel | `R: J.A.R. van Eijsden` |
| `G:` | juridisch webzoeken | `G: NOvA gedragsregel 12` |
| `URL:` | webpagina ophalen | `URL: https://…` |
| `V5:` | interview (5 vragen) → advies | `V5: incassoadvies` |
| — | documentanalyse | upload een dagvaarding/contract |
| — | stukken opstellen | "stel een sommatie op" |

Nieuw t.o.v. de Custom GPT: wetsgeschiedenis (MvT), tuchtrecht, EU-recht en
rechtspraak-bij-artikel — vraag er gewoon om in natuurlijke taal.
