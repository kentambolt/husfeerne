# Husfeerne – vores plan for at få de første kunder

Følg planen fase for fase. Sæt kryds, når et punkt er klaret. Fase 0–1 er fundamentet – spring dem ikke over, for alt det andet bygger ovenpå.

> **Om sitet:** Statisk hjemmeside på GitHub Pages, uden database og uden cookies. Den findes på fire sprog – dansk, engelsk, tysk og ukrainsk – som hver har deres egne sider: dansk på `husfeerne.dk/`, de tre andre under `/en/`, `/de/` og `/uk/` med oversatte adresser (fx `/en/home-cleaning-aalborg.html`). Flag-vælgeren øverst skifter til siden på det valgte sprog, og valget huskes i browseren. Alle fire udgaver er bundet sammen med `hreflang`, så Google viser den rigtige til hver søgning. Formularerne sendes via Formspree. Vores interne dokumenter ligger på `/cherpak/` – et fælles arkiv for os tre på dansk, engelsk og russisk. Det er ikke hemmeligt, men siderne er markeret `noindex`, så de ikke konkurrerer med salgssiderne i Google. Kilderne ligger i `cherpak/_src/` og bygges med `python cherpak/build.py`; kilder og trykfiler udgives ikke. De engelske, tyske og ukrainske sider genereres af `build_lang.py` ud fra de danske sider og oversættelserne i `i18n/tr/*.json` – ret altid i den danske side og i JSON-filerne, og kør `python build_lang.py build`; ret aldrig direkte i `/en/`, `/de/` og `/uk/`.

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
- [ ] **Indsæt CVR-nummeret** tre steder: `index.html` (kontaktsektion + footer), `privatlivspolitik.html` og `handelsbetingelser.html`. Placeholderteksten er fjernet fra sitet, så der ikke står noget ufærdigt offentligt – søg i stedet efter `NNNNNNNN`, som markerer de fire steder. I `index.html` ligger CVR-feltet i kontaktkortet som en HTML-kommentar, der bare skal åbnes igen. CVR på hjemmesiden er et lovkrav (e-handelsloven).
- [ ] **Tjek telefonnummer og adresse** på sitet. Nummeret 60 60 33 60 og Akvavitvej 7 er overført fra RenGlad – skal Husfeerne have sit eget nummer, skal det rettes i `index.html` (kontaktsektion, footer, structured data, fejlbeskederne i JavaScript) samt i begge juridiske sider.
- [ ] **Få en advokat til at gennemlæse** handelsbetingelser og privatlivspolitik. De er solide udgangspunkter, ikke juridisk rådgivning – og privatlivspolitikken beskriver nu overførsel af persondata til USA, hvilket er værd at få bekræftet.
- [x] **Egne fotos på plads.** Tolv billeder af os i arbejde bruges på forsiden og undersiderne: teamfoto med logo på trøjerne (hero og "Mød holdet"), puder ("Vores tilgang"), sofarens, trappevask, vinduespudsning og bilrengøring (forsidens kort), lampe (hovedrengøring), støvsugning og køkken (privat rengøring), ovn og bad (flytterengøring), gulvvask (erhverv), trappevask og vinduer på deres egne sider. De komprimerede udgaver har søgeordsnavne (fx `privat-rengoering-aalborg-stoevsugning.jpg`, `trappevask-aalborg-opgang.jpg`) samt `husfeerne-team.jpg`, alle med `-560`/`-800`-varianter til mobil; originalerne ligger i `raw_photos/` og udgives ikke. Ingen stock-fotos er tilbage.
- [x] **Logo på plads.** Sitet bruger `husfeerne-logo.png` – en web-optimeret udgave på 440 px bredde (10 KB, 256 farver), som er rigelig til de 148×66 px logoet vises i. Den højopløste original ligger som `husfeerne-logo-print.png` (1880 px, 479 KB) til tryk, visitkort og bilfolie; den indlæses ikke af hjemmesiden. Filen `husfeerne-logo.jpg` bruges ikke længere og kan slettes.

> **Om prisen:** 325 kr./time inkl. moms (260 kr. ex), minimum 3 timer pr. besøg og gratis kørsel kun i Aalborg Kommune. Timeprisen dækker omtrent lønnen til en nyansat på overenskomst; marginen kommer fra tætte ruter, flytte- og specialopgaver og fra 349 kr., når de første 10 anmeldelser er i hus. Hele regnestykket står i [Sådan er vores priser](priser.html) og markedsbilledet i [konkurrentanalysen](analyse.html) – begge på dansk, engelsk og russisk. Lad revisoren regne pension og øvrige arbejdsgiverbidrag præcist.

## Fase 0b · Godkend teksten på de nye servicesider

Sitet har fået seks undersider: `flytterengoering-aalborg.html`, `privat-rengoering-aalborg.html`,
`erhvervsrengoering-aalborg.html`, `vinduespudsning-aalborg.html`, `hovedrengoering-aalborg.html`
og `trappevask-aalborg.html`. Priser og garantier er hentet ordret fra forsiden, men nedenstående
er **nye udsagn, der ikke stod på sitet før**. Læs dem igennem, og ret eller slet det, I ikke kan stå
ved – det er formuleringer, en kunde kan holde jer fast på.

- [ ] **Tidsestimater** (mine skøn, ikke jeres tal): lejlighed 70–90 m² ≈ 3 timer, hus 130–160 m² ≈ 4–5 timer,
      hovedrengøring 6–8 timer for lejlighed og 10–12 for hus. Ret dem til det, I reelt bruger.
- [ ] **Flytterengøring – vinduer**: siden siger, at vinduer *indvendigt* er med i den faste pris, og at
      *udvendigt* er tilkøb. Bekræft, at det er den rigtige afgrænsning.
- [ ] **Flytterengøring – ikke inkluderet**: rens af væg-til-væg-tæpper og bortkørsel af møbler/affald er
      beskrevet som tilkøb, ikke standard.
- [ ] **Vinduespudsning – rentvandsanlæg**: siden beskriver afioniseret vand ført op gennem teleskopstang,
      og at der ikke tørres efter med klud. Bekræft, at det svarer til jeres udstyr.
- [ ] **Besøg før tilbud**: erhvervs- og trappevaskesiden lover, at I kommer forbi og ser lokalerne/opgangen,
      før I giver tilbud. Vil I binde jer til det?
- [ ] **Anbefalede intervaller**: vinduer hver 8. uge, opgange hver 14. dag. Skift tal, hvis I hellere vil andet.
- [ ] **Erhverv – faktura**: "fakturaen sendes pr. email med de oplysninger, din bogholder skal have".
      Skal der stå noget om EAN-fakturering til offentlige kunder?
- [ ] **Trappevask – fast pris i aftaleperioden** og "ingen binding ud over den aftaleperiode, I selv vælger".
- [ ] **Servicefradraget** står nu på tre sider (forside, privat rengøring, hovedrengøring) med 18.300 kr.
      pr. voksen og ca. 26 % skatteværdi. Tallet indgår også i FAQ-structured data, som Google kan vise
      direkte i søgeresultatet – tjek satsen for 2026 hos Skattestyrelsen, og sæt et årligt tjek i kalenderen.

> **Teknisk om undersiderne:** CSS og JavaScript ligger nu i `styles.css` og `app.js`, som alle sider deler –
> ret designet ét sted. Siderne er almindelig HTML, som kan redigeres direkte. Skal der flere til
> (tekstilrens, bilrengøring, Airbnb, byggerengøring), er den nemmeste vej at kopiere en eksisterende side
> og skifte tekst, `<title>`, `description`, `canonical` og JSON-LD ud – og huske at føje den til
> `sitemap.xml` og footeren. Filen `.gitattributes` sikrer, at git ikke længere melder hele filer som
> ændrede, når en Windows-editor gemmer med CRLF.

## Fase 0c · SEO-opsætningen, som den er nu

Sitet er sat op til at rangere på rengøring af private hjem og kontorer i Aalborg. Det ligger fast i dag:

- **Titler og beskrivelser** er under 60/160 tegn og bærer de søgeord, folk faktisk bruger: forsiden "Rengøring Aalborg – privat og erhverv", privat-siden "Privat rengøringshjælp i Aalborg", erhvervssiden "Erhvervsrengøring og kontorrengøring i Aalborg". Ordene *rengøringshjælp*, *kontorrengøring* og *rengøringsfirma* står nu i overskrifter og brødtekst – de manglede helt før.
- **Aalborg-kvarterer** nævnes naturligt i dækningsafsnit, FAQ og prisbokse: Hasseris, Vejgaard, Gug, Kærby, Skalborg, Vestbyen, Aalborg Øst, Nørresundby, Svenstrup, Klarup, Vodskov, Vadum, Nibe. Ingen kvarter-sider – det ville Google straffe som dørsider.
- **Structured data**: virksomheden har ét `@id` (`https://husfeerne.dk/#organization`) på alle sider, så Google ser én virksomhed og ikke syv; forsidens ydelseskatalog peger på undersiderne; FAQPage-schemaet genereres fra den synlige FAQ og matcher den ordret (det er et krav). Koordinaterne i schemaet er sat til Akvavitvej (57.0547, 9.9085) – **tjek dem mod Google Maps**, de er beregnet, ikke opslået.
- **Teknisk**: `<main>`-landmark, brødkrummer, skip-link og aria på menuen; `404.html` i sitets design; `sitemap.xml` med kun de syv indekserbare sider; rigtige favicon-filer (`favicon.svg`, `favicon.ico`, `favicon-48.png`, `apple-touch-icon.png`) så Google viser bladet i søgeresultatet; kanoniske links til `/` i stedet for `index.html`; interne links med "… i Aalborg" som ankertekst; telefon og mail klikbare i kontaktkortet.
- **Hastighed**: hero-fotoet preloades med `fetchpriority="high"`; alle fotos har `srcset` i 560/800 (og 840/1040 for teamfotoet), så mobil henter en fjerdedel af dataene; app.js loader med `defer`; skrifterne (Cormorant Garamond, Lato og Source Sans 3 til kyrillisk) hostes selv fra `/fonts/` via `fonts.css` med `font-display:swap`, og de to vigtigste filer preloades – ingen opslag mod Google Fonts, og dermed heller ingen tredjepart i privatlivspolitikken for skrifter.
- **Delebilleder**: `husfeerne-og.jpg` (1200×628) bruges ved deling på Facebook/LinkedIn; trappevask og vinduespudsning har egne beskårne udgaver.
- **Fire sprog med hver deres sider**: forsiden og de seks servicesider findes på dansk, engelsk, tysk og ukrainsk – 28 sider i alt, alle i `sitemap.xml` med `hreflang`-alternativer. Hver sprogudgave har egen adresse med søgeord på sproget, egen title, beskrivelse, overskrifter, FAQ og structured data, og `x-default` peger på dansk. Formularerne sender stadig de danske valgmuligheder, så I læser det samme uanset kundens sprog. De ukrainske sider bruger skriften Source Sans 3 til brødtekst, fordi Lato ikke har kyrilliske tegn.
- **Ikke gjort, med vilje**: anmeldelses-schema (vi har ingen anmeldelser endnu – det må aldrig opfindes).

> **To udsagn, I skal kunne stå ved:** FAQ'en siger nu, at Husfeerne er et rengøringsfirma med *egne, ansatte* medarbejdere – ikke en platform. Og de tre gamle stock-fotos (trappevask, vinduer, bil) er slettet, fordi de viste andre firmaers logoer; egne fotos er sat ind i stedet.

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
- [x] **Flersproget SEO.** Alle fire sprog har egne adresser (`/`, `/en/`, `/de/`, `/uk/`) med `hreflang` imellem, så Google kan vise den engelske side til en engelsk søgning. Hold øje i Search Console med, hvilke sprog der faktisk giver trafik – og læg tekstændringer i den danske side og `i18n/tr/`, så de tre andre sprog følger med ved næste `python build_lang.py build`.
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
