# Step by step: finding words again

[Nederlandse projecthandleiding](README.md)

Dutch-language speech and communication exercises for adults with aphasia or other language difficulties after a stroke. The project was conceived by **Marco Beenen** with ChatGPT (OpenAI) in November 2026.

**Use the free website:** [GitHub Pages](https://sosaklingo.github.io/afasie-oefenboekjes/).

When you open the website, choose **level 1, 2, 3 or 4**, or go directly to the communication board. You can switch levels at any time. The exercises themselves are in Dutch; this English document describes how to use and maintain the project.

## What's included?

| Section | Contents |
| --- | --- |
| Level 1 – Finding words | 12 simple interactive exercises and an 18-page PDF |
| Level 2 – Sentences and stories | 12 more challenging exercises and an 18-page PDF |
| Level 3 – Understanding texts | 12 exercises with longer texts, comprehension questions and responses in your own words; a 30-page PDF |
| Level 4 – Thinking and expressing | 12 exercises with more complex stories, connections, comparisons and opinions; a 30-page PDF |
| I want to say something | A communication board with 7 topics and 63 prepared phrases, plus a 14-page PDF |
| My phrases | Add up to 9 personal short phrases on your own device |

The website is designed for phones, tablets and computers. It offers large buttons, adjustable text size, high contrast, examples and optional Dutch text-to-speech through the browser. Exercises have no timer and no score.

## Files and folders

- [`website/dist/`](website/dist/) contains the static website (HTML, CSS, JavaScript, favicon and PDFs).
- [`website/test_site.mjs`](website/test_site.mjs) checks exercises, communication phrases, layout markers and download links.
- [`pdf/`](pdf/) contains five printable A4 booklets (110 pages in total).
- [`maak_boekjes.py`](maak_boekjes.py) generates the booklets.
- [`exporteer_extra_niveaus.mjs`](exporteer_extra_niveaus.mjs) exports data for the two harder-level booklets from the website source.
- [`levels-extra.json`](levels-extra.json) stores those exercise data for PDF generation.
- [`requirements.txt`](requirements.txt) lists the Python dependency.

## Running and testing locally

Open `website/dist/index.html` in a modern browser. Most features work without a server.

Run the automated content checks:

```sh
node website/test_site.mjs
```

GitHub Actions also runs these checks and a Python syntax check on commits and pull requests, using read-only repository permissions.

To regenerate the PDF booklets:

```sh
python3 -m pip install -r requirements.txt
node exporteer_extra_niveaus.mjs
python3 maak_boekjes.py
```

The generated files appear in `pdf/`. If you update the website, copy the PDFs to `website/dist/pdf/` as well.

## For users and supporters

- Ask whether the person wants to practise. Allow plenty of time and ask one question at a time.
- Pointing, drawing and writing are also forms of communication. Speaking aloud is not required.
- Take a break if an activity becomes difficult or tiring. This is not an exam.
- Ask a speech and language therapist which activities are suitable for the individual.

**Medical notice:** This is supplementary practice material, not a medical test or a validated treatment, and it does not replace individual speech and language therapy. In the Netherlands, call **112** for suddenly developing speech loss, facial droop or weakness.

Personal phrases, if added, are stored only in the browser on that device, not on a server. Shared devices offer an option to erase local data. Do not publish filled-in medical or personal details on GitHub.

## General information sources

- [Thuisarts – After a stroke](https://www.thuisarts.nl/beroerte/omgaan-met-gevolgen-herseninfarct-of-hersenbloeding) (Dutch)
- [Afasie.nl](https://www.afasie.nl/) (Dutch)
- [ASHA – Aphasia](https://www.asha.org/practice-portal/clinical-topics/aphasia/)

All exercises and illustrations were created for this project. **No open-source licence has been chosen yet.** Public GitHub visibility alone does not grant unrestricted reuse or commercial distribution rights.
