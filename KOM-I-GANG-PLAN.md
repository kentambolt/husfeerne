# Husfeerne – Din plan for at få de første kunder

Følg planen fase for fase. Sæt kryds, når et punkt er klaret. Fase 0–1 er fundamentet – spring dem ikke over, for alt det andet bygger ovenpå.

> **Om sitet:** Statisk hjemmeside på GitHub Pages, uden database og uden cookies. Den findes på fire sprog – dansk, engelsk, tysk og ukrainsk – som besøgende vælger med flag-vælgeren øverst. Dansk er standard, og det er den danske udgave Google indekserer. Formularerne sendes via Formspree. Se "Flersproget SEO" i Fase 5, hvis I senere vil have de tre andre sprog med i søgeresultaterne.

---

## Fase 0 · Fundamentet på plads (uge 1)

- [ ] **Registrér domænet husfeerne.dk** hos en registrator (fx DanDomain eller One.com). Bekræft først ledigheden på punktum.dk.
- [ ] **Slå GitHub Pages til**: repoet → Settings → Pages → Source: "GitHub Actions". Workflowet `.github/workflows/main.yml` udgiver automatisk ved push til `main`.
- [ ] **Custom domain og DNS**: filen `CNAME` i repoet indeholder allerede `husfeerne.dk`. Opret hos registratoren fire A-records for `husfeerne.dk` mod GitHubs adresser (185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153) og et CNAME for `www` mod `<brugernavn>.github.io`. Slå derefter "Enforce HTTPS" til i Pages-indstillingerne.
- [ ] **Bekræft Formspree-formularen**: formularerne sender til `https://formspree.io/f/xdeowewq`. Log ind på formspree.io og tjek, at modtager-mailen er verificeret, ellers kommer beskederne ikke frem. Slå deres spamfilter/reCAPTCHA til efter behov – sitet har allerede et skjult honeypot-felt (`_gotcha`), som Formspree forstår.
- [ ] **Test begge formularer efter deploy**: send en testbesked fra både kontakt- og jobformularen, og tjek at den ikke lander i spam. Emnet er sat via `_subject`, og mailen indeholder feltet `sprog`, så I kan se, om der skal svares på dansk, engelsk, tysk eller ukrainsk.
- [ ] **Vær opmærksom på Formsprees grænse**: gratisplanen har et loft på 50 indsendelser om måneden. Kommer I over, skal I opgradere – ellers går henvendelser tabt.
- [ ] **Overvej en separat formular til job**: begge formularer bruger samme endpoint, så alt lander i samme mailboks. Vil I have ansøgninger for sig, opret en formular mere på Formspree og skift `action` og `FORMSPREE`-konstanten i jobformularen.
- [ ] **Databehandleraftale med Formspree** (og GitHub): begge er databehandlere for jer og ligger i USA. Hent/gem Formsprees DPA fra deres kontrolpanel. Privatlivspolitikken beskriver dem nu som databehandlere – få den læst igennem af en jurist, se punktet nedenfor.
- [ ] **Opret firma-email** hej@husfeerne.dk og job@husfeerne.dk (følger ofte med domænet, ellers Google Workspace).
- [ ] **Tegn forsikringer**: erhvervsansvarsforsikring (I lover det på hjemmesiden!) og lovpligtig arbejdsskadeforsikring for medarbejderne.
- [ ] **Ansættelseskontrakter og løn**: skriftlige kontrakter til medarbejderne, lønsystem (fx Salary eller Dataløn). Tjek 3F Privat Service-overenskomsten som benchmark – ordnede forhold er en del af jeres brand.
- [ ] **Indsæt CVR-nummeret** tre steder: `index.html` (kontaktsektion + footer), `privatlivspolitik.html` og `handelsbetingelser.html`. Søg efter `[INDSÆT CVR-NUMMER]`. CVR på hjemmesiden er et lovkrav (e-handelsloven).
- [ ] **Tjek telefonnummer og adresse** på sitet. Nummeret 60 60 33 60 og Akvavitvej 7 er overført fra RenGlad – skal Husfeerne have sit eget nummer, skal det rettes i `index.html` (kontaktsektion, footer, structured data, fejlbeskederne i JavaScript) samt i begge juridiske sider.
- [ ] **Få en advokat til at gennemlæse** handelsbetingelser og privatlivspolitik. De er solide udgangspunkter, ikke juridisk rådgivning – og privatlivspolitikken beskriver nu overførsel af persondata til USA, hvilket er værd at få bekræftet.
- [ ] **Bed om logoet som PNG med transparent baggrund og tætbeskåret**. Sitet bruger `husfeerne-logo.jpg`, som har hvid baggrund og bred tom margin. Det er løst med `mix-blend-mode: multiply` og negative marginer i CSS, men en tætbeskåret PNG ville gøre begge hacks unødvendige og logoet skarpere.

> **Vigtigt om prisen:** 212 kr./time ex moms (265 kr. inkl.) er aggressivt. Regn efter: løn (~160–190 kr./time inkl. feriepenge og pension), transport, produkter, forsikring og administration. Overvej et minimumsbesøg på 3 timer, så kørsel ikke æder marginen på små opgaver.

## Fase 1 · Bliv synlig, hvor kunderne søger (uge 1–2)

- [ ] **Google Business Profile** – det absolut vigtigste enkeltpunkt for at blive fundet på "rengøring Aalborg". Opret på business.google.com: kategori "Rengøringsservice", serviceområde Aalborg + hele Nordjylland, åbningstider, telefonnummer, teamfotoet og logoet. Gennemfør verificeringen med det samme. **Udfyld feltet for betjeningssprog med dansk, engelsk, tysk og ukrainsk** – det er en reel søgefordel.
- [ ] **Google Search Console**: verificér husfeerne.dk og indsend `sitemap.xml`. Her kan du følge, hvilke søgeord folk finder jer på.
- [ ] **Bing Places + Bing Webmaster Tools** (5 minutter, gratis trafik).
- [ ] **Opret Facebook-side og Instagram-profil** med logo, teamfoto og link til sitet. Instagram passer særligt godt til den visuelle identitet – før/efter-billeder virker stærkt i denne branche.
- [ ] **Krak.dk / degulesider.dk**: opret gratis virksomhedsprofil.
- [ ] **Trustpilot**: opret virksomhedsprofil, så I er klar til anmeldelser.
- [ ] **NAP-konsistens**: brug PRÆCIS samme navn, adresse og telefonnummer alle steder – det styrker den lokale Google-placering. Husk at Husfeerne og RenGlad skal have hver deres profiler; bland dem ikke sammen.

## Fase 2 · De første 10 kunder (uge 2–4)

- [ ] **Aktivér dit netværk**: send en personlig besked (ikke massebesked) til alle, du kender i Aalborg-området. Bed dem dele. De første kunder kommer næsten altid herfra.
- [ ] **Facebook-grupper**: lav ét godt opslag med teamfotoet i lokale grupper ("Aalborg", "Anbefalinger Aalborg", kvarter-grupper). Fokusér på historien: nyt lokalt firma, fast lav pris, de samme to faste medarbejdere hver gang, ingen binding.
- [ ] **Fremhæv tryghed frem for pris i private hjem.** Det, der afgør valget, er sjældent timeprisen, men om man tør lukke nogen ind. Brug de tre konkrete løfter, sitet allerede giver: samme to medarbejdere hver gang, forsikring, og skriftlig aftale hvis I skal have en nøgle.
- [ ] **Udnyt sprogene aktivt** – det er en tydelig forskel fra konkurrenterne:
  - Internationale medarbejdere og studerende på AAU og UCN (engelsk).
  - Tyske sommerhusgæster og sommerhusudlejere langs vestkysten og i Skagen-området (tysk).
  - Ukrainske netværk og foreninger i Nordjylland – både som kunder og som fremtidige kolleger (ukrainsk).
  Skriv opslagene på det pågældende sprog og link direkte til sitet; den besøgende kan skifte sprog i toppen.
- [ ] **Flyers/dørhængere** i udvalgte kvarterer med god økonomi og travle familier: Hasseris, Gug, Vejgaard, Kærby, Nørresundby. Husk: uddel dem selv eller aflever i hånden – reklamer i postkasser med "Nej tak"-mærke er ulovligt.
- [ ] **Bilerne som reklamesøjler**: magnetskilte eller folie med logoet og telefonnummer. Kører reklame hver dag, gratis.
- [ ] **B2B-fremstød – flytterengøring**: ring til ejendomsmæglere, boligforeninger og udlejere i Aalborg. Flytterengøring er tilbagevendende forretning fra samme kontakt.
- [ ] **B2B-fremstød – småerhverv**: besøg 20 små kontorer, klinikker og frisører om ugen med et enkelt tilbudsark. Erhvervskunder giver faste ugentlige timer.
- [ ] **Airbnb-værter og sommerhusudlejere**: skriv til værter i Aalborg og langs kysten om fast skifterengøring. Nævn, at I kan tage imod deres tyske gæster på tysk.

## Fase 3 · Anmeldelser og henvisninger (fra første kunde og altid)

- [ ] **Bed HVER tilfreds kunde om en Google-anmeldelse** – send en sms med direkte link (find linket i Google Business Profile → "Bed om anmeldelser"). Mål: 10 anmeldelser den første måned. Anmeldelser er den stærkeste faktor for både placering og konvertering.
- [ ] **Henvisningsprogram**: giv 1 gratis time til kunder, der skaffer en ny fast kunde. Skriv det på et lille kort, der efterlades efter hver rengøring.
- [ ] **Efterlad et kort fra Husfeerne** efter hvert besøg med QR-kode til anmeldelseslinket. Brug samme grønne/cremede identitet som sitet, så det hænger sammen.

## Fase 4 · Betalt annoncering (uge 4+, når ovenstående kører)

- [ ] **Google Ads**: søgeannoncer på "rengøring aalborg", "rengøringshjælp aalborg", "flytterengøring aalborg". Start med 2.000–3.000 kr./md., geografisk afgrænset til Nordjylland, med opkaldsudvidelse. Stop ord der ikke konverterer efter 2–3 uger.
- [ ] **Prøv engelske og tyske annoncegrupper**: "cleaning service aalborg", "cleaning help aalborg", "reinigung aalborg", "putzhilfe nordjütland". Konkurrencen er langt mindre end på de danske ord, og klikprisen tilsvarende lavere.
- [ ] **Facebook/Instagram-annoncer**: brug teamfotoet, målret 25–65-årige i Aalborg +30 km. Budskab: samme faste medarbejdere, fast lav pris, ingen binding, fire sprog.
- [ ] **VIGTIGT – cookie-banner ved tracking**: I dag bruger sitet ingen cookies, så der kræves intet banner. Men i samme øjeblik I tilføjer Google Analytics, Google Ads-tag eller Facebook-pixel, SKAL der cookie-samtykke på sitet (fx Cookiebot eller CookieYes), og privatlivspolitikken skal opdateres.
- [ ] **Mål alt**: spørg hver eneste ny kunde "Hvor hørte du om os?" og skriv det ned. Brug Search Console + Google Business-statistik månedligt. Læg pengene der, hvor kunderne faktisk kommer fra.

## Fase 5 · Drift og vækst (måned 2+)

- [ ] **Svar lynhurtigt**: alle henvendelser besvares inden for 1 time i åbningstiden. Hurtighed vinder flere kunder end pris.
- [ ] **Svar på kundens eget sprog**: mails fra formularen har sproget i feltet `sprog`, så I kan se, om der skal svares på dansk, engelsk, tysk eller ukrainsk.
- [ ] **Fast kadence**: ring tilbage samme dag, send tilbud samme dag, følg op efter 3 dage uden svar.
- [ ] **Ansæt medarbejder nr. 3**, når kalenderen har været 80 % fuld i 4 uger i træk.
- [ ] **Om jobopslag – vær opmærksom her.** Sitet må gerne fortælle kunderne, at teamet i dag består af kvinder; det er en faktuel oplysning. Men et *jobopslag* må efter ligebehandlingsloven ikke henvende sig til ét køn, og forskelsbehandlingsloven forbyder desuden at målrette efter alder eller udseende. Jobsektionen på sitet er derfor holdt neutral med vilje – lad den blive det, også når I selv skriver opslag på Jobindex eller Facebook. Formuleringer som "smilende og serviceminded medarbejder" er helt i orden.
- [ ] **Udbyg SEO med undersider**: separate sider pr. ydelse og by ("Flytterengøring Aalborg", "Erhvervsrengøring Hjørring" osv.) – den stærkeste næste SEO-investering, når der er drift i forretningen.
- [ ] **Flersproget SEO – næste skridt.** Sprogvælgeren skifter teksten i browseren, men alle fire sprog deler samme URL (husfeerne.dk/). Google indekserer derfor kun den danske udgave. Vil I også rangere på engelske, tyske og ukrainske søgninger, kræver det separate adresser – fx `husfeerne.dk/en/`, `/de/`, `/uk/` – med `hreflang`-tags mellem dem og oversat title og meta description på hver side. Teksterne findes allerede i `index.html` (i `data-en`, `data-de` og `data-uk`), så det er hovedsagelig et spørgsmål om at splitte filen op. Tag det, når de danske sider konverterer.
- [ ] **Nyt teamfoto, når I får poloer med logo på.** Gem det som `husfeerne-team.jpg` i rodmappen – det bruges tre steder (hero, "Vores tilgang", "Mød holdet") og som billede ved deling på sociale medier. Det nuværende foto er uden logo på tøjet.
- [ ] **Månedligt tjek (30 min.)**: Search Console-kliks, Google Business-opkald, antal anmeldelser, "hvor hørte du om os"-listen, og Formspree-forbrug.

---

## Målepunkter – ved du, om det virker?

| Tidspunkt | Mål |
|---|---|
| Uge 2 | Site live på husfeerne.dk, Google Business verificeret, begge formularer testet |
| Uge 4 | 10 henvendelser, 3–5 faste kunder, 5 Google-anmeldelser |
| Måned 2 | 10 faste kunder, 10+ anmeldelser, første erhvervskunde |
| Måned 3 | Fuld kalender for 2 medarbejdere → begynd rekruttering |

## Tre ting, der oftest vælter nye rengøringsfirmaer

1. **Prisen er sat for lavt til at kunne betale ordentlig løn** – regn din timeøkonomi igennem, før du skalerer (se boksen i Fase 0).
2. **Langsom opfølgning** – en henvendelse, der ikke besvares samme dag, er en mistet kunde.
3. **Ingen anmeldelser** – 10 gode Google-anmeldelser slår alt andet markedsføring lokalt. Gør det til en vane fra kunde nummer 1.

Held og lykke – Flittig, Venlig, Dygtig.
