/* Husfeerne – fælles script for alle sider.
   Sprogvælger, formularer og mobilmenu. Alle opslag er null-sikrede,
   så den samme fil kan bruges på forsiden, på servicesiderne og på de
   engelske, tyske og ukrainske udgaver under /en/, /de/ og /uk/. */

/* ---------- Sprogvalg: dansk, engelsk, tysk, ukrainsk ---------- */
const LANGS = {
  da: {name:'Dansk',      flag:'#f-da'},
  en: {name:'English',    flag:'#f-en'},
  de: {name:'Deutsch',    flag:'#f-de'},
  uk: {name:'Українська', flag:'#f-uk'}
};
const LANG_KEY = 'husfeerne-lang';
/* Sidens eget sprog står i <html lang>. Forsiden og servicesiderne findes som
   rigtige sider pr. sprog (bygget af build_lang.py) og peger på hinanden med
   <link rel="alternate" hreflang>. Sider uden alternativer (404, juridiske sider)
   oversættes i browseren via data-en/de/uk som før. */
const PAGE_LANG = (document.documentElement.lang || 'da').slice(0,2);
let lang = LANGS[PAGE_LANG] ? PAGE_LANG : 'da';

const langWrap = document.getElementById('langWrap');
const langBtn  = document.getElementById('langBtn');
const langMenu = document.getElementById('langMenu');

function alternateUrl(code){
  const link = document.querySelector('link[rel="alternate"][hreflang="' + code + '"]');
  if(!link) return null;
  /* Kun stien bruges, saa skiftet ogsaa virker paa en testserver eller et preview-domaene. */
  const u = new URL(link.href);
  return u.pathname + u.search;
}

function setLang(code){
  if(!LANGS[code]) code = 'da';
  try{ localStorage.setItem(LANG_KEY, code); }catch(e){}

  /* Findes siden på det valgte sprog, går vi derhen (ankeret følger med). */
  const url = alternateUrl(code);
  if(url && code !== lang){
    location.href = url + location.hash;
    return;
  }

  lang = code;
  document.documentElement.lang = code;

  /* Første gang gemmes den danske originaltekst i data-da, så vi altid kan skifte tilbage. */
  document.querySelectorAll('[data-en]').forEach(el=>{
    if(el.dataset.da === undefined) el.dataset.da = el.textContent;
    el.textContent = el.dataset[code] !== undefined ? el.dataset[code] : el.dataset.da;
  });
  document.querySelectorAll('[data-enph]').forEach(el=>{
    if(el.dataset.daph === undefined) el.dataset.daph = el.placeholder;
    const ph = el.dataset[code + 'ph'];
    el.placeholder = ph !== undefined ? ph : el.dataset.daph;
  });

  /* Knappen i toppen */
  const flag = document.querySelector('#langFlag use');
  if(flag) flag.setAttribute('href', LANGS[code].flag);
  const name = document.getElementById('langName');
  if(name) name.textContent = LANGS[code].name;
  if(langMenu) langMenu.querySelectorAll('button').forEach(b=>
    b.setAttribute('aria-selected', b.dataset.lang === code ? 'true' : 'false'));

  /* Sproget følger med i formularerne, så vi svarer på det rigtige sprog */
  opdaterSprogfelter();

  closeLangMenu();
  const nav = document.getElementById('navLinks');
  if(nav) nav.classList.remove('open');
}
function openLangMenu(){
  if(!langMenu) return;
  langMenu.classList.add('open');
  langBtn.setAttribute('aria-expanded','true');
}
function closeLangMenu(){
  if(!langMenu) return;
  langMenu.classList.remove('open');
  langBtn.setAttribute('aria-expanded','false');
}
if(langBtn && langMenu){
  langBtn.addEventListener('click', e=>{
    e.stopPropagation();
    langMenu.classList.contains('open') ? closeLangMenu() : openLangMenu();
  });
  langMenu.querySelectorAll('button').forEach(b=>
    b.addEventListener('click', ()=> setLang(b.dataset.lang)));
  document.addEventListener('click', e=>{ if(!langWrap.contains(e.target)) closeLangMenu(); });
  document.addEventListener('keydown', e=>{ if(e.key === 'Escape') closeLangMenu(); });
}

/* Har den besøgende tidligere valgt et andet sprog og lander på en dansk side
   (fx fra Google), sendes de til siden på deres sprog; findes den ikke, oversættes
   det, der kan oversættes i browseren. Lander de direkte på en engelsk, tysk eller
   ukrainsk side, respekteres den adresse, de har fået. Google har intet gemt valg
   og ser derfor altid siden på dens eget sprog. */
try{
  const saved = localStorage.getItem(LANG_KEY);
  if(saved && LANGS[saved] && saved !== lang && lang === 'da'){
    const url = alternateUrl(saved);
    if(url) location.replace(url + location.hash);
    else if(document.querySelector('[data-en]')) setLang(saved);
  }
}catch(e){}

/* ---------- Formularer: sendes til Formspree (sitet er statisk på GitHub Pages) ---------- */
const FORMSPREE = 'https://formspree.io/f/xdeowewq';

/* Sproget sendes med som læsbar tekst, så mailen viser fx "Tysk (de)". */
function opdaterSprogfelter(){
  const vaerdi = LANGS[lang].name + ' (' + lang + ')';
  /* Felterne findes kun på de sider, der har den pågældende formular. */
  ['kontaktSprog','jobSprog'].forEach(id=>{
    const felt = document.getElementById(id);
    if(felt) felt.value = vaerdi;
  });
}

const BESKEDER = {
  kontakt: {
    da: 'Tak! Vi kontakter dig inden for 24 timer 😊',
    en: 'Thank you! We will contact you within 24 hours 😊',
    de: 'Danke! Wir melden uns innerhalb von 24 Stunden 😊',
    uk: 'Дякуємо! Ми зв’яжемося з вами протягом 24 годин 😊'
  },
  job: {
    da: 'Tak for din ansøgning! Vi vender tilbage inden for 2 hverdage 😊',
    en: 'Thanks for applying! We will get back to you within 2 business days 😊',
    de: 'Danke für deine Bewerbung! Wir melden uns innerhalb von 2 Werktagen 😊',
    uk: 'Дякуємо за заявку! Ми відповімо протягом 2 робочих днів 😊'
  },
  fejl: {
    da: 'Noget gik galt – ring til os på 60 60 33 60',
    en: 'Something went wrong – please call us on +45 60 60 33 60',
    de: 'Etwas ist schiefgelaufen – rufen Sie uns an: +45 60 60 33 60',
    uk: 'Щось пішло не так — зателефонуйте нам: +45 60 60 33 60'
  },
  /* Mindst ét af felterne email og mobilnummer skal udfyldes,
     ellers har vi ingen måde at kontakte personen på. */
  mangler: {
    da: 'Skriv din email eller dit mobilnummer, så vi kan kontakte dig',
    en: 'Please enter your email or mobile number so we can contact you',
    de: 'Bitte geben Sie Ihre E-Mail-Adresse oder Mobilnummer ein, damit wir Sie kontaktieren können',
    uk: 'Вкажіть email або номер мобільного, щоб ми могли з вами зв’язатися'
  }
};
function showToast(msg){
  const t = document.getElementById('toast');
  if(!t) return;
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'), 4500);
}
function hookForm(id, beskedNoegle, mailId, telId){
  const form = document.getElementById(id);
  if(!form) return;   /* siden har ikke denne formular */
  form.addEventListener('submit', async function(e){
    e.preventDefault();

    /* Egen validering: browseren kan ikke selv kraeve "et af to felter". */
    const mail = document.getElementById(mailId);
    const tel  = document.getElementById(telId);
    if(!mail.value.trim() && !tel.value.trim()){
      showToast(BESKEDER.mangler[lang]);
      mail.focus();
      return;
    }

    const knap = this.querySelector('button[type="submit"]');
    knap.disabled = true;
    try{
      const data = new FormData(this);
      const res = await fetch(FORMSPREE, {
        method: 'POST',
        body: data,
        headers: {'Accept': 'application/json'}
      });
      const svar = await res.json().catch(()=>({}));
      if(!res.ok) throw new Error((svar.errors || []).map(f=>f.message).join(', ') || 'server');
      this.reset();
      opdaterSprogfelter();   // reset() sætter skjulte felter tilbage til HTML-værdien
      showToast(BESKEDER[beskedNoegle][lang]);
    }catch(err){
      showToast(BESKEDER.fejl[lang]);
    }finally{
      knap.disabled = false;
    }
  });
}
hookForm('contactForm','kontakt','cmail','cphone');
hookForm('jobForm','job','jmail','jphone');
opdaterSprogfelter();

/* ---------- Job-sektion: skjult indtil man klikker på "Job" ---------- */
/* Findes kun på forsiden. Fra servicesiderne peger menupunktet på /#job. */
const jobSektion = document.getElementById('job');
if(jobSektion){
  document.querySelectorAll('a[href="#job"]').forEach(a=>
    a.addEventListener('click',()=>{ jobSektion.style.display='block'; }));
  if(location.hash==='#job'){ // direkte link, f.eks. husfeerne.dk#job
    jobSektion.style.display='block';
    jobSektion.scrollIntoView();
  }
}

/* ---------- Close mobile menu on click ---------- */
document.querySelectorAll('.nav-links a').forEach(a=>
  a.addEventListener('click',()=>{
    const nav = document.getElementById('navLinks');
    if(nav) nav.classList.remove('open');
  }));
