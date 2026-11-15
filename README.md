# Stap voor stap weer praten

Nederlandstalige taal- en communicatieoefeningen voor volwassenen met afasie of andere taalproblemen na een beroerte. Dit project is bedacht door **Marco Beenen**, samen met ChatGPT (OpenAI), in november 2026.

**Gebruik direct de openbare website:** [GitHub Pages](https://sosaklingo.github.io/afasie-oefenboekjes/) of [de andere openbare website](https://stap-voor-stap-weer-praten-2026.marcobeenen.chatgpt.site/).

Bij openen kies je zelf **niveau 1, 2, 3 of 4**, of direct het communicatiebord. Je kunt op elk moment een ander niveau kiezen.

## Wat zit erin?

| Onderdeel | Inhoud |
| --- | --- |
| Niveau 1 – Woorden terugvinden | 12 interactieve eenvoudige opdrachten en een PDF van 18 pagina's |
| Niveau 2 – Zinnen en verhalen | 12 uitdagendere opdrachten en een PDF van 18 pagina's |
| Niveau 3 – Teksten begrijpen | 12 opdrachten met langere teksten, begripsvragen en eigen formuleringen; PDF van 30 pagina's |
| Niveau 4 – Denken en verwoorden | 12 opdrachten met moeilijkere verhalen, verbanden, afwegingen en een eigen mening; PDF van 30 pagina's |
| Ik wil iets vertellen | Interactief aanwijsbord met 7 onderwerpen en 63 standaardzinnen, plus een PDF van 14 pagina's |
| Mijn woorden | Maximaal 9 eigen korte zinnen toevoegen op het eigen apparaat |

De website werkt op smartphone, tablet en computer en heeft grote knoppen, grotere-letteroptie, een contrastinstelling, voorbeelden en optioneel browser-voorlezen in het Nederlands. Opdrachten hebben geen tijdslimiet en geen score.

## Mappen en bestanden

- [`website/dist/`](website/dist/) bevat de volledige statische website (HTML, CSS, JavaScript, favicon en PDF's).
- [`website/test_site.mjs`](website/test_site.mjs) controleert de opdrachten, communicatiezinnen, schermopmaak en downloadlinks.
- [`pdf/`](pdf/) bevat de vijf printbare A4-boekjes (samen 110 pagina's).
- [`maak_boekjes.py`](maak_boekjes.py) is de generator voor de boekjes.
- [`exporteer_extra_niveaus.mjs`](exporteer_extra_niveaus.mjs) maakt de gegevens voor de twee moeilijkere boekjes vanuit de websitebron.
- [`levels-extra.json`](levels-extra.json) bevat die oefengegevens voor de PDF-generator.
- [`requirements.txt`](requirements.txt) bevat de Python-afhankelijkheid.

## Lokaal testen

Open `website/dist/index.html` in een moderne browser. De meeste functies werken zonder server.

Voer voor de automatische inhoudscontrole uit:

```sh
cd website
node test_site.mjs
```

Om de PDF's opnieuw te maken:

```sh
python3 -m pip install -r requirements.txt
node exporteer_extra_niveaus.mjs
python3 maak_boekjes.py
```

Daarna staan de nieuw gemaakte documenten in `pdf/`. Als je de webversie bijwerkt, kopieer je die PDF's ook naar `website/dist/pdf/`.

## Voor gebruikers en begeleiders

- Vraag eerst of iemand wil oefenen. Geef ruim de tijd en stel één vraag tegelijk.
- Aanwijzen, tekenen en schrijven zijn ook vormen van communicatie. Hardop antwoorden is niet verplicht.
- Pauzeer zodra het moeilijk of vermoeiend wordt. Oefenen is geen examen.
- Laat een logopedist bepalen welke opdrachten passen bij de persoon.

**Medische waarschuwing:** dit materiaal is aanvullend oefenmateriaal, geen medische test, geen gevalideerde behandeling en geen vervanging van individuele logopedie. Bij plotselinge nieuwe spraakuitval, een scheve mond of krachtsverlies: bel in Nederland **112**.

De website slaat eventueel toegevoegde eigen zinnen alleen in de browser van dat apparaat op, niet op de server. Voor gedeelde apparaten is er een knop om de lokale gegevens te wissen. Publiceer geen ingevulde medische of persoonlijke gegevens in GitHub.

## Gebruikte algemene informatiebronnen

- [Thuisarts - Gevolgen van een beroerte](https://www.thuisarts.nl/beroerte/omgaan-met-gevolgen-herseninfarct-of-hersenbloeding)
- [Afasie.nl](https://www.afasie.nl/)
- [ASHA - Aphasia](https://www.asha.org/practice-portal/clinical-topics/aphasia/)

Alle oefenopgaven en illustraties in deze repository zijn voor dit project gemaakt. Er is **nog geen open-sourcelicentie** gekozen. De code en documenten zijn zichtbaar, maar dat is niet hetzelfde als een algemene toestemming voor hergebruik of commerciële verspreiding.
