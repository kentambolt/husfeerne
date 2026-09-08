# Husfeerne – our plan for getting the first customers

Follow the plan phase by phase. Tick things off as they are done. Phases 0–1 are the foundation – do not skip them, because everything else is built on top.

> **About the site:** A static website on GitHub Pages, with no database and no cookies. It exists in four languages – Danish, English, German and Ukrainian – which visitors pick with the flag selector at the top. Danish is the default, and the Danish version is what Google indexes. Forms are sent via Formspree. Our internal documents live at `/cherpak/` – a shared archive for the three of us in Danish, English and Russian. It is not secret, but the pages are marked `noindex` so they do not compete with the sales pages in Google. The sources live in `cherpak/_src/` and are built with `python cherpak/build.py`; sources and print files are not published. See "Multilingual SEO" in Phase 5 if we later want the other three languages in the search results too.

---

## Phase 0 · Foundation in place (week 1)

- [ ] **Register the domain husfeerne.dk** with a registrar (e.g. DanDomain or One.com). Check availability on punktum.dk first.
- [ ] **Turn on GitHub Pages**: the repo → Settings → Pages → Source: "GitHub Actions". The workflow `.github/workflows/main.yml` publishes automatically on push to `main`.
- [ ] **Custom domain and DNS**: the file `CNAME` in the repo already contains `husfeerne.dk`. At the registrar, create four A records for `husfeerne.dk` pointing to GitHub's addresses (185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153) and a CNAME for `www` pointing to `<username>.github.io`. Then enable "Enforce HTTPS" in the Pages settings.
- [ ] **Confirm the Formspree form**: the forms post to `https://formspree.io/f/xdeowewq`. Log in at formspree.io and check that the recipient e-mail is verified, otherwise messages will not arrive. Turn on their spam filter/reCAPTCHA as needed – the site already has a hidden honeypot field (`_gotcha`) that Formspree understands.
- [ ] **Test both forms after deploy**: send a test message from both the contact and the job form and check it does not land in spam. The subject is set via `_subject`, and the e-mail contains the field `sprog` (language), so we can see whether to reply in Danish, English, German or Ukrainian.
- [ ] **Mind Formspree's limit**: the free plan caps at 50 submissions a month. If we exceed it we must upgrade – otherwise enquiries are lost.
- [ ] **Consider a separate form for jobs**: both forms use the same endpoint, so everything lands in the same inbox. To keep applications separate, create another form at Formspree and change the `action` and the `FORMSPREE` constant in the job form.
- [ ] **Data processing agreement with Formspree** (and GitHub): both are data processors for us and are located in the USA. Download/save Formspree's DPA from their control panel. The privacy policy now describes them as processors – have it reviewed by a lawyer, see the item below.
- [ ] **Set up company e-mail** hej@husfeerne.dk and job@husfeerne.dk (often comes with the domain, otherwise Google Workspace).
- [ ] **Take out insurance**: business liability insurance (we promise it on the website!) and the statutory occupational injury insurance for employees.
- [ ] **Employment contracts and payroll**: written contracts for the employees, a payroll system (e.g. Salary or Dataløn). Use the 3F Private Service collective agreement as the benchmark – proper conditions are part of our brand.
- [ ] **Insert the CVR number** in three places: `index.html` (contact section + footer), `privatlivspolitik.html` and `handelsbetingelser.html`. The placeholder text has been removed from the site so nothing unfinished is public – search instead for `NNNNNNNN`, which marks the four spots. In `index.html` the CVR field in the contact card is an HTML comment that just needs to be reopened. CVR on the website is a legal requirement (the Danish E-commerce Act).
- [ ] **Check phone number and address** on the site. The number 60 60 33 60 and Akvavitvej 7 were carried over from RenGlad – if Husfeerne is to have its own number, it must be changed in `index.html` (contact section, footer, structured data, the error messages in the JavaScript) and on both legal pages.
- [ ] **Have a lawyer read through** the terms and conditions and the privacy policy. They are solid starting points, not legal advice – and the privacy policy now describes transfer of personal data to the USA, which is worth having confirmed.
- [x] **Our own photos in place.** Nine pictures of us at work are used on the front page and the sub-pages: team photo with the logo on the shirts (hero and "Meet the team"), cushions ("Our approach"), sofa cleaning (front-page card), lamp (deep cleaning), vacuuming and kitchen (home cleaning), oven and bathroom (move-out cleaning), floor (business). The compressed versions are `foto-*.jpg` and `husfeerne-team.jpg`; the originals live in `raw_photos/` and are not published.
- [x] **Logo in place.** The site uses `husfeerne-logo.png` – a web-optimised version 440 px wide (46 KB), plenty for the 148×66 px the logo is shown at. The high-resolution original is `husfeerne-logo-print.png` (1880 px, 479 KB) for print, business cards and car decals; the website does not load it. The file `husfeerne-logo.jpg` is no longer used and can be deleted.

> **About the price:** DKK 325/hour incl. VAT (260 ex), a 3-hour minimum per visit and free travel only within Aalborg Municipality. The hourly rate roughly covers the wage of a new employee on the collective agreement; the margin comes from dense routes, move-out and special jobs, and from DKK 349 once the first 10 reviews are in. The full calculation is in [Our prices – and why](priser.html) and the market picture in the [competitor analysis](analyse.html) – both in Danish, English and Russian. Have the accountant work out pension and other employer contributions precisely.

## Phase 0b · Approve the text on the new service pages

The site has gained six sub-pages: `flytterengoering-aalborg.html`, `privat-rengoering-aalborg.html`, `erhvervsrengoering-aalborg.html`, `vinduespudsning-aalborg.html`, `hovedrengoering-aalborg.html` and `trappevask-aalborg.html`. Prices and guarantees are taken verbatim from the front page, but the following are **new statements that were not on the site before**. Read them through and correct or delete anything we cannot stand behind – these are wordings a customer can hold us to.

- [ ] **Time estimates** (the author's estimates, not our figures): flat 70–90 m² ≈ 3 hours, house 130–160 m² ≈ 4–5 hours, deep clean 6–8 hours for a flat and 10–12 for a house. Adjust them to what we actually use.
- [ ] **Move-out cleaning – windows**: the page says windows *inside* are included in the fixed price and *outside* is an add-on. Confirm that is the right split.
- [ ] **Move-out cleaning – not included**: cleaning wall-to-wall carpets and removing furniture/waste are described as add-ons, not standard.
- [ ] **Window cleaning – pure-water system**: the page describes de-ionised water fed up through a telescopic pole, with no wiping afterwards. Confirm that matches our equipment.
- [ ] **Visit before quote**: the business and stairwell pages promise that we come by and see the premises/stairwell before quoting. Do we want to commit to that?
- [ ] **Recommended intervals**: windows every 8 weeks, stairwells every 2 weeks. Change the numbers if we prefer otherwise.
- [ ] **Business – invoicing**: "the invoice is sent by e-mail with the details your bookkeeper needs". Should we say anything about EAN invoicing for public-sector customers?
- [ ] **Stairwells – fixed price for the agreement period** and "no commitment beyond the agreement period you choose yourself".
- [ ] **The service deduction** now appears on three pages (front page, home cleaning, deep cleaning) with DKK 18,300 per adult and approx. 26 % tax value. The figure is also in the FAQ structured data, which Google may show directly in the search result – check the 2026 rate with the tax authority, and put an annual check in the calendar.

> **Technical note on the sub-pages:** CSS and JavaScript now live in `styles.css` and `app.js`, shared by all pages – change the design in one place. The pages are plain HTML and can be edited directly. If more are needed (textile cleaning, car cleaning, Airbnb, construction cleaning), the easiest route is to copy an existing page and swap the text, `<title>`, `description`, `canonical` and JSON-LD – and remember to add it to `sitemap.xml` and the footer. The file `.gitattributes` makes sure git no longer reports whole files as changed when a Windows editor saves with CRLF.

## Phase 1 · Be visible where customers search (weeks 1–2)

- [ ] **Google Business Profile** – by far the single most important item for being found on "rengøring Aalborg". Create it at business.google.com: category "Cleaning service", service area Aalborg + all of North Jutland, opening hours, phone number, the team photo and the logo. Complete verification immediately. **Fill in the service-languages field with Danish, English, German and Ukrainian** – it is a real search advantage.
- [ ] **Google Search Console**: verify husfeerne.dk and submit `sitemap.xml`. Here we can follow which search terms people find us on.
- [ ] **Bing Places + Bing Webmaster Tools** (5 minutes, free traffic).
- [ ] **Create a Facebook page and Instagram profile** with logo, team photo and a link to the site. Instagram suits the visual identity particularly well – before/after pictures work strongly in this trade.
- [ ] **Krak.dk / degulesider.dk**: create free business profiles.
- [ ] **Trustpilot**: create a company profile so we are ready for reviews.
- [ ] **NAP consistency**: use EXACTLY the same name, address and phone number everywhere – it strengthens the local Google ranking. Remember Husfeerne and RenGlad must each have their own profiles; do not mix them.

## Phase 2 · The first 10 customers (weeks 2–4)

- [ ] **Activate the network**: send a personal message (not a mass message) to everyone we know in the Aalborg area. Ask them to share. The first customers almost always come from here.
- [ ] **Facebook groups**: make one good post with the team photo in local groups ("Aalborg", "Anbefalinger Aalborg", neighbourhood groups). Focus on the story: new local company, fixed price, the same two regular staff every time, no commitment.
- [ ] **Emphasise peace of mind over price in private homes.** What decides the choice is rarely the hourly rate, but whether people dare let someone in. Use the three concrete promises the site already makes: the same two people every time, insurance, and a written agreement if we are to hold a key.
- [ ] **Use the languages actively** – it is a clear difference from the competitors:
  - International staff and students at AAU and UCN (English).
  - German holiday-home guests and holiday-home owners along the west coast and around Skagen (German).
  - Ukrainian networks and associations in North Jutland – both as customers and as future colleagues (Ukrainian).
  Write the posts in the relevant language and link straight to the site; the visitor can switch language at the top.
- [ ] **Flyers/door hangers** in selected neighbourhoods with good incomes and busy families: Hasseris, Gug, Vejgaard, Kærby, Nørresundby. Remember: hand them out ourselves or deliver by hand – advertising in letterboxes with a "No thanks" sticker is illegal.
- [ ] **The cars as billboards**: magnetic signs or decals with the logo and phone number. Advertising every day, for free.
- [ ] **B2B push – move-out cleaning**: call estate agents, housing associations and landlords in Aalborg. Move-out cleaning is repeat business from the same contact.
- [ ] **B2B push – small businesses**: visit 20 small offices, clinics and hairdressers a week with a simple offer sheet. Business customers give fixed weekly hours.
- [ ] **Airbnb hosts and holiday-home owners**: write to hosts in Aalborg and along the coast about regular turnover cleaning. Mention that we can receive their German guests in German.

## Phase 3 · Reviews and referrals (from the first customer, and always)

- [ ] **Ask EVERY satisfied customer for a Google review** – send a text with a direct link (find the link in Google Business Profile → "Ask for reviews"). Target: 10 reviews in the first month. Reviews are the strongest factor for both ranking and conversion.
- [ ] **Referral programme**: give 1 free hour to customers who bring in a new regular customer. Put it on a small card left behind after each cleaning.
- [ ] **Leave a card from Husfeerne** after every visit with a QR code to the review link. Use the same green/cream identity as the site so it hangs together.

## Phase 4 · Paid advertising (week 4+, once the above is running)

- [ ] **Google Ads**: search ads on "rengøring aalborg", "rengøringshjælp aalborg", "flytterengøring aalborg". Start with DKK 2,000–3,000/month, geographically limited to North Jutland, with a call extension. Stop keywords that do not convert after 2–3 weeks.
- [ ] **Try English and German ad groups**: "cleaning service aalborg", "cleaning help aalborg", "reinigung aalborg", "putzhilfe nordjütland". Competition is far lower than on the Danish terms, and the click price correspondingly lower.
- [ ] **Facebook/Instagram ads**: use the team photo, target 25–65-year-olds in Aalborg +30 km. Message: the same regular staff, fixed price, no commitment, four languages.
- [ ] **IMPORTANT – cookie banner with tracking**: today the site uses no cookies, so no banner is required. But the moment we add Google Analytics, a Google Ads tag or a Facebook pixel, cookie consent MUST go on the site (e.g. Cookiebot or CookieYes), and the privacy policy must be updated.
- [ ] **Measure everything**: ask every single new customer "Where did you hear about us?" and write it down. Use Search Console + Google Business statistics monthly. Put the money where the customers actually come from.

## Phase 5 · Operations and growth (month 2+)

- [ ] **Reply fast**: all enquiries answered within 1 hour during opening hours. Speed wins more customers than price.
- [ ] **Reply in the customer's own language**: e-mails from the form carry the language in the `sprog` field, so we can see whether to reply in Danish, English, German or Ukrainian.
- [ ] **Fixed cadence**: call back the same day, send the quote the same day, follow up after 3 days without a reply.
- [ ] **Hire employee no. 3** when the calendar has been 80 % full for 4 weeks running.
- [ ] **About job ads – be careful here.** The site may tell customers that the team today consists of women; that is a factual statement. But a *job ad* may not, under the Danish Equal Treatment Act, address one gender, and the Anti-Discrimination Act also forbids targeting by age or appearance. The job section on the site is therefore deliberately kept neutral – keep it that way, also when we write ads on Jobindex or Facebook ourselves. Wordings like "smiling, service-minded employee" are perfectly fine.
- [ ] **Extend SEO with sub-pages**: separate pages per service and town ("Flytterengøring Aalborg", "Erhvervsrengøring Hjørring" etc.) – the strongest next SEO investment once the business is running.
- [ ] **Multilingual SEO – next step.** The language selector switches the text in the browser, but all four languages share the same URL (husfeerne.dk/). Google therefore indexes only the Danish version. To rank on English, German and Ukrainian searches too requires separate addresses – e.g. `husfeerne.dk/en/`, `/de/`, `/uk/` – with `hreflang` tags between them and a translated title and meta description on each page. The texts already exist in `index.html` (in `data-en`, `data-de` and `data-uk`), so it is mostly a matter of splitting the file up. Take it on once the Danish pages convert.
- [ ] **Monthly check (30 min.)**: Search Console clicks, Google Business calls, number of reviews, the "where did you hear about us" list, and Formspree usage.

---

## Milestones – do we know if it is working?

| When | Target |
|---|---|
| Week 2 | Site live at husfeerne.dk, Google Business verified, both forms tested |
| Week 4 | 10 enquiries, 3–5 regular customers, 5 Google reviews |
| Month 2 | 10 regular customers, 10+ reviews, first business customer |
| Month 3 | Full calendar for 2 employees → start recruiting |

## Three things that most often sink new cleaning companies

1. **The price is set too low to pay a proper wage** – work through the hourly economics before scaling (see the box in Phase 0).
2. **Slow follow-up** – an enquiry not answered the same day is a lost customer.
3. **No reviews** – 10 good Google reviews beat all other local marketing. Make it a habit from customer number one.

Good luck – Diligent, Friendly, Skilled.
