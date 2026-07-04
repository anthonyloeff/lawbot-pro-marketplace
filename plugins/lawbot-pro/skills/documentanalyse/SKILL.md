---
name: documentanalyse
description: Juridische stukken analyseren die de gebruiker aanlevert (dagvaarding, vonnis, conclusie, contract, sommatie). MOET actief worden bij /lawbot-pro:analyseer, een geüpload of geplakt juridisch document, of "wat vind je van dit stuk", "beoordeel dit contract", "bereid een verweer voor op deze dagvaarding".
---

# Documentanalyse

## Privacy-kader (eerst, zichtbaar voor de gebruiker)

Open je analyse met één regel:
> *Je document wordt binnen Claude verwerkt en niet naar de LawBot-server gestuurd; alleen
> abstracte zoekvragen (rechtsbegrippen, artikelnummers) gaan naar de officiële bronnen.*

Dat is ook een instructie aan jou: **stuur nooit passages, partijnamen, bedragen of
feitencomplexen als zoekterm mee** — abstraheer naar juridische begrippen
("non-conformiteit koopwoning", niet "de lekkage in de woning van familie X").

## Werkwijze

1. **Documenttype herkennen** → leesstrategie: dagvaarding (petitum + grondslagen),
   vonnis (dictum + dragende overwegingen), conclusie (weren per grondslag), contract
   (risicoclausules: aansprakelijkheid, opzegging, boete, toepasselijk recht), sommatie
   (gestelde verplichting + termijn).
2. **Analyse:** destilleer de rechtsvragen; benoem per partijpositie de sterke en zwakke
   punten; signaleer ontbrekende stellingen of bewijs; let scherp op termijnen, verval- en
   verjaringstermijnen (noem data).
3. **Automatisch bronnen erbij:** zoek voor elke geïdentificeerde rechtsvraag de relevante
   artikelen (`zoek_wet`) en 2–3 sleuteluitspraken (`zoek_jurisprudentie` of
   `jurisprudentie_bij_artikel`) — met de ijzeren regels uit `juridisch-onderzoek`.

## Outputformat

```
**Documenttype & partijen:** …
**Kern van het geschil:** …
**Rechtsvragen:** 1. … 2. …
**Sterke punten / zwakke punten:** <per partijpositie, tabel>
**Ontbreekt:** <stellingen, bewijs, formaliteiten>
**Termijnen & risico's:** <met data>
**Relevante bronnen:** <per rechtsvraag: artikel + rechtspraak, alle met links>
**Aanbevolen vervolgstappen:** …
```

Bied als vervolg aan: "Zal ik op basis hiervan een conceptreactie opstellen?
(/lawbot-pro:opstellen)". Sluit af met de standaarddisclaimer en de privacy-voetregel
"Dit document is niet naar externe servers verzonden."
