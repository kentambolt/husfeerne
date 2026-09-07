/* Husfeerne – fælles script for alle sider.
   Sprogvælger, formularer og mobilmenu. Alle opslag er null-sikrede,
   så den samme fil kan bruges på forsiden og på servicesiderne,
   uanset om siden har jobformular og job-sektion. */

/* ---------- Sprogvalg: dansk, engelsk, tysk, ukrainsk ---------- */
const LANGS = {
  da: {name:'Dansk',      flag:'#f-da', htmlLang:'da'},
  en: {name:'English',    flag:'#f-en', htmlLang:'en'},
  de: {name:'Deutsch',    flag:'#f-de', htmlLang:'de'},
  uk: {name:'Українська', flag:'#f-uk', htmlLang:'uk'}
};
const LANG_KEY = 'husfeerne-lang';
let lang = 'da';

const langWrap = document.getElementById('langWrap');
const langBtn  = document.getElementById('langBtn');
const langMenu = document.getElementById('langMenu');

function setLang(code){
  if(!LANGS[code]) code = 'da';
  lang = code;
  document.documentElement.lang = LANGS[code].htmlLang;

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
  document.querySelector('#langFlag use').setAttribute('href', LANGS[code].flag);
  document.getElementById('langName').textContent = LANGS[code].name;
  langMenu.querySelectorAll('button').forEach(b=>
    b.setAttribute('aria-selected', b.dataset.lang === code ? 'true' : 'false'));

  /* Sproget følger med i formularerne, så vi svarer på det rigtige sprog */
  opdaterSprogfelter();

  /* Servicesiderne er kun skrevet på dansk. Har den besøgende valgt et andet
     sprog, forklarer vi det i deres eget sprog i stedet for at lade siden
     stå halvt oversat. Notitsen findes ikke på forsiden. */
  const kunDansk = document.getElementById('kunDansk');
  if(kunDansk) kunDansk.hidden = (code === 'da');

  try{ localStorage.setItem(LANG_KEY, code); }catch(e){}
  closeLangMenu();
  const nav = document.getElementById('navLinks');
  if(nav) nav.classList.remove('open');
}
function openLangMenu(){
  langMenu.classList.add('open');
  langBtn.setAttribute('aria-expanded','true');
}
function closeLangMenu(){
  langMenu.classList.remove('open');
  langBtn.setAttribute('aria-expanded','false');
}
langBtn.addEventListener('click', e=>{
  e.stopPropagation();
  langMenu.classList.contains('open') ? closeLangMenu() : openLangMenu();
});
langMenu.querySelectorAll('button').forEach(b=>
  b.addEventListener('click', ()=> setLang(b.dataset.lang)));
document.addEventListener('click', e=>{ if(!langWrap.contains(e.target)) closeLangMenu(); });
document.addEventListener('keydown', e=>{ if(e.key === 'Escape') closeLangMenu(); });

/* Dansk er standard, så Google altid indekserer den danske udgave.
   Kun et aktivt valg huskes – og kun i den besøgendes egen browser. */
try{
  const saved = localStorage.getItem(LANG_KEY);
  if(saved && LANGS[saved] && saved !== 'da') setLang(saved);
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
/* Findes kun på forsiden. Fra servicesiderne peger menupunktet paa index.html#job. */
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
