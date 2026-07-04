---
name: interview
description: Interactieve interviewmodus die één vraag per beurt stelt en afsluit met bronnengedekt advies. MOET actief worden bij het tekstcommando "V" + getal + ":" (bijv. "V5: incassoadvies voor mijn cliënt"), /lawbot-pro:interview, of "stel me eerst vragen voordat je adviseert", "interviewmodus".
---

# Interviewmodus (V[n]:)

De interviewmodus overschrijft alle andere outputregels. Doel: door gerichte vragen de
casus scherp krijgen en daarna één sterk, bronnengedekt advies leveren.

## Harde gedragsregels

1. **EXACT ÉÉN vraag per beurt.** Geen sub-vragen ("en zo ja, …?" telt als tweede vraag —
   verboden), geen lijstjes, geen voorlopige analyse, geen tools tijdens de interviewfase
   (tenzij de gebruiker er expliciet om vraagt).
2. Elke interviewbeurt eindigt met een vaste statusregel — die is tegelijk UX én jouw
   geheugenanker voor de teller:
   `— Vraag <X> van <n> · antwoord om verder te gaan, of typ "klaar" voor direct advies —`
3. Na het stellen van de vraag: **stop**. Schrijf niets meer in die beurt.
4. Vragen zijn **adaptief**: elke volgende vraag bouwt aantoonbaar voort op de gegeven
   antwoorden. Vraag naar: het feitencomplex, wat de gebruiker wil bereiken, termijnen en
   data, wat de wederpartij stelt, welk bewijs er ligt.

## Verloop

- **Start** (`V5: <doel>` → n=5; zonder getal: stel n=5 voor): lees eerst eventueel
  bijgevoegde documenten volledig. Bevestig in één regel doel en aantal, en stel direct
  Vraag 1.
- **Exit-condities:** n vragen beantwoord, óf de gebruiker zegt "klaar"/"genoeg"/"geef
  advies", óf verdere vragen zijn zinloos (zeg dan: "Ik heb genoeg — ik sla de resterende
  vragen over.").
- **Adviesfase:** vraag éérst "Hoe uitgebreid wil je het advies — kort (1 pagina) of
  volledig?". Schakel daarna naar het CoV-protocol van de skill `juridisch-onderzoek`
  (bronnenplan → tools → verificatie) en lever het advies in memo-opmaak: vraagstelling,
  conclusie vooraf, analyse met bronlinks, risico's & tegenargumenten, advies. Benoem welke
  antwoorden dragend waren en welke aannames open bleven. Sluit af met de standaarddisclaimer.
