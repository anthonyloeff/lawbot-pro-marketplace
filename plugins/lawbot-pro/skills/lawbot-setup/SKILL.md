---
name: lawbot-setup
description: Onboarding, licentie en probleemdiagnose van LawBot Pro. MOET actief worden bij /lawbot-pro:lawbot-status, "licentie", "sleutel", "proefperiode", "migratiecode", "abonnement opzeggen", "LawBot werkt niet", elke licentiefout uit een LawBot-tool, "connector", "verbinden", "Connect-knop grijs", ontbrekende LawBot-tools, en bij het allereerste gebruik van de plugin.
---

# LawBot Pro — setup & licentie

## Statuscheck

Roep `licentie_status` aan en presenteer het resultaat menselijk: plan, proefperiode
(dagen resterend), verbruik vandaag, en de beheerlink (https://lawbot.nl/account).

## Scenario's

**A. Geen of ongeldige sleutel** (tool-fout `license_invalid` of lege configuratie) —
geef GEEN juridisch antwoord uit eigen kennis; toon dit stappenplan:
1. Ga naar **https://lawbot.nl** en start de gratis proefperiode van 14 dagen
   (je legt een betaalmethode vast en betaalt pas na de proef). *Kom je van de LawBot Pro
   Custom GPT? Vul je migratiecode in voor 30 dagen.*
2. Kopieer je licentiesleutel (begint met `lbp_`) — hij wordt één keer getoond.
3. Verbind de connector en log in met de sleutel (zie E). In Claude Code (terminal):
   `/mcp` → `lawbot` → **Authenticate**.
4. Test met `W: 6:162 BW`.

**B. Proefperiode verlopen / betaling mislukt** (`license_expired` / `license_past_due`):
gegevens blijven bewaard; verlengen of betaalmethode bijwerken kan via
https://lawbot.nl/account — daarna werkt alles direct weer, zonder herinstallatie.

**C. Migratiecode:** de code wordt verzilverd op de portal (bij het starten van de proef),
niet in de plugin. Verwijs vriendelijk door.

**D. Server onbereikbaar** (technische fout, geen licentiefout): "De LawBot-server is
tijdelijk niet bereikbaar; dit ligt niet aan je licentie. Probeer het over enkele minuten
opnieuw."

**E. Connector niet verbonden** (de LawBot-tools ontbreken, of de gebruiker meldt dat de
connector "niet verbonden" is) — geef GEEN juridisch antwoord uit eigen kennis; toon dit
stappenplan:
1. Open *Customize → Plugins → LawBot Pro → Connectors* en klik bij `lawbot` op **Connect**.
2. Plak op de LawBot-inlogpagina je licentiesleutel (of vraag een inlogcode per e-mail aan)
   en keer terug naar Claude.
3. Begin een nieuw gesprek en test met `W: 6:162 BW`.
Blijft Connect grijs of lukt het niet (bijv. een oudere versie van de plugin)? Werk de
plugin bij, of voeg zelf een custom connector toe: *Customize → Connectors* → **+** →
*Add custom connector*, naam `lawbot`, URL exact: `https://fyzocmfqaatpivqjtphh.supabase.co/functions/v1/mcp-server/mcp` → **Connect** → inloggen.
Zie je geen "Add custom connector" (Team- of Enterprise-omgeving)? Dan voegt een beheerder
de connector met deze URL toe; daarna klikt de gebruiker zelf op Connect.

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
