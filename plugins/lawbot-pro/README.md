# LawBot Pro — juridische onderzoeksassistent voor Nederlandse advocaten

Een plugin voor Claude (Cowork), gebouwd op **officiële, verifieerbare bronnen**:
rechtspraak.nl Open Data, wetten.overheid.nl (actueel én historisch), Kamerstukken,
tuchtrecht.overheid.nl en EUR-Lex — plus een eigen semantische index die dagelijks
meegroeit. Elke bewering komt met een klikbare bronlink; je documenten verlaten
Claude nooit.

## Installatie (5 minuten)

1. **Licentie:** start je gratis proefperiode van 14 dagen op
   **[lawbot.nl](https://lawbot.nl)** (je legt een betaalmethode vast en betaalt
   pas na de proef; met migratiecode van de Custom GPT: 30 dagen). Kopieer je sleutel (`lbp_…`).
2. **Plugin:** in Claude → *Customize → Plugins* (tabblad Cowork) → **+** →
   *Add marketplace* → *Add from a repository* → `anthonyloeff/lawbot-pro-marketplace`
   → installeer **LawBot Pro**.
3. **Connector verbinden:** in Claude → *Customize → Connectors* → **+** →
   *Add custom connector*, met als naam `lawbot` en als URL (exact overnemen, de plugin
   herkent de connector aan dit adres):

   ```
   https://fyzocmfqaatpivqjtphh.supabase.co/functions/v1/mcp-server/mcp
   ```

   Klik op **Connect**. Je komt op de inlogpagina van LawBot: plak je licentiesleutel
   (of vraag een inlogcode per e-mail aan) en je keert terug naar Claude. In de plugin
   staat de connector daarna op *Connected*.
   *Zie je geen "Add custom connector" (Team- of Enterprise-omgeving)? Vraag dan je
   beheerder de connector met deze URL toe te voegen; daarna klik je zelf op Connect.*
4. **Test:** typ `W: 6:162 BW`. Staat het artikel er binnen enkele seconden, dan werkt alles.

**Claude Code (terminal):** `/plugin marketplace add anthonyloeff/lawbot-pro-marketplace`
gevolgd door `/plugin install lawbot-pro@litic`, en plak je sleutel als Claude Code erom
vraagt. Een custom connector is daar niet nodig.

## Commando's

`W:` wetten · `J:` jurisprudentie · `S:` uitspraakanalyse · `R:` rechterprofiel ·
`G:` webzoeken · `URL:` pagina ophalen · `V5:` interview — plus documentanalyse en het
opstellen van stukken in gewone taal. Alle oude Custom GPT-commando's blijven werken;
zie [MIGRATIE.md](MIGRATIE.md).

## Privacy

De server verwerkt uitsluitend zoekvragen en slaat géén inhoud op (alleen anonieme
gebruiks-metadata voor de licentie). Documenten die je aanlevert blijven binnen Claude.

## Licentie

Source-available, **geen open source**. De code is openbaar zichtbaar zodat je kunt
controleren wat de plugin doet, maar **forken, kopiëren, herdistribueren, wijzigen of
commercieel exploiteren is niet toegestaan** zonder schriftelijke toestemming van Litic.ai.
Zie [LICENSE](LICENSE). De plugin werkt uitsluitend met een geldige LawBot Pro-licentie en
de Litic.ai-backend.

## Support

support@litic.ai · [lawbot.nl](https://lawbot.nl) · Litic.ai — Antwerpen/Eindhoven
