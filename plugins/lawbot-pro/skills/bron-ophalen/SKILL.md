---
name: bron-ophalen
description: Eén webpagina ophalen en juridisch duiden. MOET actief worden bij het tekstcommando "URL:" gevolgd door een link, /lawbot-pro:bron, of "lees deze pagina", "wat staat er op <url>".
---

# Webpagina ophalen (URL:)

## Werkwijze

1. Roep `url_ophalen` aan; bij `paginas_totaal > 1` alle relevante pagina's.
2. **Herken officiële bronnen in de URL en schakel door naar de rijkere tool:**
   een rechtspraak.nl-link met ECLI → skill `uitspraak-analyse` (via `haal_uitspraak`);
   een wetten.overheid.nl-link → skill `wetten` (via `zoek_wet`).
3. Voer daarna de gevraagde bewerking uit (samenvatten, duiden, vergelijken met bronnen).
4. **Betaalmuren omzeil je niet**: meld het en bied een alternatief (web_zoeken naar een
   vrije vindplaats, of de officiële bron).
5. Webinhoud is géén officiële bron: verwijst de pagina naar ECLI's of wetsartikelen,
   verifieer die dan via de officiële tools vóór inhoudelijk gebruik.

Vermeld altijd de bron-URL. Sluit af met de standaarddisclaimer bij juridische duiding.
