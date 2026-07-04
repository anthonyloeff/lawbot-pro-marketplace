# LawBot Pro — juridische onderzoeksassistent voor Nederlandse advocaten

Een plugin voor Claude (Cowork), gebouwd op **officiële, verifieerbare bronnen**:
rechtspraak.nl Open Data, wetten.overheid.nl (actueel én historisch), Kamerstukken,
tuchtrecht.overheid.nl en EUR-Lex — plus een eigen semantische index die dagelijks
meegroeit. Elke bewering komt met een klikbare bronlink; je documenten verlaten
Claude nooit.

## Installatie (3 minuten)

1. **Licentie:** start je gratis proefperiode van 14 dagen op
   **[portal.litic.ai](https://portal.litic.ai)** (geen creditcard nodig; met
   migratiecode van de Custom GPT: 30 dagen). Kopieer je sleutel (`lbp_…`).
2. **Plugin:** in Claude → *Customize → Plugins* (tabblad Cowork) → **+** →
   *Add marketplace* → *Add from a repository* → `anthonyloeff/lawbot-pro-marketplace`
   → installeer **LawBot Pro**.
   Of via Claude Code: `/plugin marketplace add anthonyloeff/lawbot-pro-marketplace`
   gevolgd door `/plugin install lawbot-pro@litic`.
3. **Sleutel:** bij het inschakelen vraagt Claude om je licentiesleutel — plak hem daar.
4. **Test:** typ `W: 6:162 BW`. Staat het artikel er binnen enkele seconden, dan werkt alles.

## Commando's

`W:` wetten · `J:` jurisprudentie · `S:` uitspraakanalyse · `R:` rechterprofiel ·
`G:` webzoeken · `URL:` pagina ophalen · `V5:` interview — plus documentanalyse en het
opstellen van stukken in gewone taal. Alle oude Custom GPT-commando's blijven werken;
zie [MIGRATIE.md](MIGRATIE.md).

## Privacy

De server verwerkt uitsluitend zoekvragen en slaat géén inhoud op (alleen anonieme
gebruiks-metadata voor de licentie). Documenten die je aanlevert blijven binnen Claude.

## Support

support@litic.ai · [portal.litic.ai](https://portal.litic.ai) · Litic.ai — Antwerpen/Eindhoven
