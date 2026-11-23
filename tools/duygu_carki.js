/* Duygu Çarkı — sitenin içinde çalışan hâli. Kaynak: tasarım ekibinin taslağı (2026-11-23).
   Çıkarılanlar: kapak/yelpaze, koyu tema. Veri tools/duygu_carki_veri.json'dan __VERI__ yerine gömülür (blog_uret.py). */
(function(){
const V = __VERI__;
const D = V.duygular;
const R = [62, 150, 240, 334];          // delik, duygu, alt duygu, ton halkalarının dış yarıçapları
const KISA = 22;                        // ikinci yerdeki tonun dilimi dıştan bu kadar kısa
const NS = 'http://www.w3.org/2000/svg';
const svg = document.getElementById('cark');
const panel = document.getElementById('panel');
const hareket = !matchMedia('(prefers-reduced-motion: reduce)').matches;

function parlaklik(h){const n=parseInt(h.slice(1),16),r=(n>>16)/255,g=(n>>8&255)/255,b=(n&255)/255;const f=c=>c<=.03928?c/12.92:Math.pow((c+.055)/1.055,2.4);return .2126*f(r)+.7152*f(g)+.0722*f(b)}
function yaziRengi(h){return parlaklik(h)>.32?'#1C1F2A':'#FFFFFF'}
function nokta(r,a){return [r*Math.cos(a), r*Math.sin(a)]}
function yay(r0,r1,a0,a1){
  const b=a1-a0>Math.PI?1:0,[x0,y0]=nokta(r1,a0),[x1,y1]=nokta(r1,a1),[x2,y2]=nokta(r0,a1),[x3,y3]=nokta(r0,a0);
  return `M${x0},${y0}A${r1},${r1} 0 ${b} 1 ${x1},${y1}L${x2},${y2}A${r0},${r0} 0 ${b} 0 ${x3},${y3}Z`;
}
function el(ad,at,ust){const e=document.createElementNS(NS,ad);for(const k in at)e.setAttribute(k,at[k]);if(ust)ust.appendChild(e);return e}
function yazi(g,metin,r,aOrta,boy,renk,agirlik){
  let der=aOrta*180/Math.PI, ters=Math.cos(aOrta)<0;
  const [x,y]=nokta(r,aOrta);
  const t=el('text',{x,y,'font-size':boy,'font-weight':agirlik||500,fill:renk,'text-anchor':'middle','dominant-baseline':'central',
    transform:`rotate(${ters?der+180:der} ${x} ${y})`},g);
  t.textContent=metin;return t;
}
function ortaRenk(tonlar){const s=[...tonlar].sort((a,b)=>parlaklik(a.hex)-parlaklik(b.hex));return s[Math.floor(s.length/2)].hex}
const asil=a=>a.tonlar.filter(t=>!t.ikinci);
const iki=n=>String(n+1).padStart(2,'0');
const serit=tonlar=>`<span class="serit" aria-hidden="true">${tonlar.map(t=>`<i style="background:${t.hex}"></i>`).join('')}</span>`;
const ilkCumle=m=>m.split('. ')[0].replace(/\.?$/,'.');


// ---- Adres çubuğu: #sec/1/2/3 ya da #cark/1/2/3 (duygu/alt/ton sırası) ----
function cozHash(){
  const p=decodeURIComponent(location.hash.replace(/^#/,'')).split('/');
  const s={gor:p[0]==='cark'?'cark':'sec',di:null,ai:null,ti:null}, n=p.slice(1).map(x=>/^\d+$/.test(x)?+x:-1);
  if(D[n[0]]){s.di=n[0]; if(D[s.di].alt[n[1]]){s.ai=n[1]; if(D[s.di].alt[s.ai].tonlar[n[2]]) s.ti=n[2];}}
  return s;
}
function hashYap(gor,di,ai,ti){return '#'+[gor,di,ai,ti].filter(x=>x!==null&&x!==undefined).join('/')}
function gitHash(h){if(location.hash!==h) location.hash=h; else uygula(true)}

// ---- Adım adım seçici ----
const secKutu=document.getElementById('gor-sec');
function adimCubugu(s){
  const asama=s.di===null?1:s.ai===null?2:s.ti===null?3:4;
  const adlar=['Duygu','Alt duygu','Ton'];
  const secilen=[s.di!==null?D[s.di].ad:'', s.ai!==null?D[s.di].alt[s.ai].ad:'', s.ti!==null?D[s.di].alt[s.ai].tonlar[s.ti].kod:''];
  const hedef=[hashYap('sec'),hashYap('sec',s.di),hashYap('sec',s.di,s.ai)];
  return `<ol class="adim-cubuk">${adlar.map((ad,i)=>{
    const durum=i+1<asama?'bitti':i+1===asama?'simdi':'bekler';
    const ic=`<b>${iki(i)}</b><span>${ad}</span>${secilen[i]?`<small>${secilen[i]}</small>`:''}`;
    return `<li class="${durum}"${durum==='simdi'?' aria-current="step"':''}>${durum==='bitti'?`<a href="${hedef[i]}">${ic}</a>`:ic}</li>`;
  }).join('')}</ol>`;
}
function alanlar(d){return `<div class="baslik-k">Nerede iyi çalışır</div><ul class="alan">${d.alanlar.map((x,i)=>`<li><span>${iki(i)}</span>${x}</li>`).join('')}</ul>`}
const lejant=`<div class="lejant"><svg viewBox="0 0 34 22" aria-hidden="true"><rect x="1" y="1" width="14" height="20" rx="2" fill="var(--dc-ikincil)"/><rect x="19" y="5" width="14" height="16" rx="2" fill="var(--dc-ikincil)" stroke="var(--dc-metin)" stroke-width="1.3" stroke-dasharray="3 2.5"/></svg><span>Kısa ve kesik çizgili dilim, asıl yeri başka bir duygu olan tonu gösterir. Bir ton en fazla iki duyguda yer alır.</span></div>`;
const lejantKart=`<div class="lejant"><svg viewBox="0 0 34 22" aria-hidden="true"><rect x="2" y="2" width="30" height="18" rx="4" fill="none" stroke="var(--dc-ikincil)" stroke-width="1.3" stroke-dasharray="3 2.5"/></svg><span>Kesik çerçeveli kart, asıl yeri başka bir duygu olan tonu gösterir. Bir ton en fazla iki duyguda yer alır.</span></div>`;
function yolBul(kod,ikinci){
  for(const [di,d] of D.entries()) for(const [ai,a] of d.alt.entries()) for(const [ti,t] of a.tonlar.entries())
    if(t.kod===kod && t.ikinci===ikinci) return {di,ai,ti};
}
function secCiz(s){
  let ic='';
  if(s.di===null){
    ic=`<div class="sec-bas"><p class="ust-yazi">Adım 1 / 3</p><h2 tabindex="-1">Mekân ne hissettirsin?</h2>
      <p>Sekiz duygudan biri seçildiğinde o duygunun alt başlıkları, ardından tonları açılır.</p></div>
      <div class="kartlar">${D.map((d,di)=>`<a class="kart" href="${hashYap('sec',di)}"><span class="kart-ust"><span class="rozet">${iki(di)}</span><span class="kart-ad">${d.ad}</span></span>${serit(d.alt.flatMap(asil))}<span class="kart-metin">${ilkCumle(d.metin)}</span></a>`).join('')}</div>`;
  } else if(s.ai===null){
    const d=D[s.di];
    ic=`<a class="geri" href="${hashYap('sec')}">← Tüm duygular</a>
      <div class="sec-bas"><p class="ust-yazi">Adım 2 / 3 · ${d.ad}</p><h2 tabindex="-1">${d.ad}</h2><p>${d.metin}</p></div>
      <div class="kartlar">${d.alt.map((a,ai)=>`<a class="kart" href="${hashYap('sec',s.di,ai)}"><span class="kart-ust"><span class="rozet">${iki(ai)}</span><span class="kart-ad">${a.ad}</span></span>${serit(a.tonlar)}<span class="kart-metin">${a.metin}</span></a>`).join('')}</div>
      ${alanlar(d)}`;
  } else if(s.ti===null){
    const d=D[s.di], a=d.alt[s.ai];
    ic=`<a class="geri" href="${hashYap('sec',s.di)}">← ${d.ad}</a>
      <div class="sec-bas"><p class="ust-yazi">Adım 3 / 3 · ${d.ad} › ${a.ad}</p><h2 tabindex="-1">${a.ad}</h2><p>${a.metin}</p></div>
      <div class="kartlar tonlar">${a.tonlar.map((t,ti)=>`<a class="kart ton${t.ikinci?' ikinci':''}" href="${hashYap('sec',s.di,s.ai,ti)}"><span class="ton-renk" style="background:${t.hex}"></span><span class="kart-ad">${t.kod}</span><span class="kart-sayi">${t.aile}</span>${t.ikinci?`<span class="ikinci-not">Asıl yeri: ${t.diger}</span>`:''}</a>`).join('')}</div>
      ${a.tonlar.some(t=>t.ikinci)?lejantKart:''}${alanlar(d)}`;
  } else {
    const d=D[s.di], a=d.alt[s.ai], t=a.tonlar[s.ti];
    const o=t.diger?yolBul(t.kod,!t.ikinci):null;
    const diger=o?`<dt>${t.ikinci?'Asıl yeri':'Ayrıca'}</dt><dd><a href="${hashYap('sec',o.di,o.ai,o.ti)}">${t.diger}</a></dd>`:'';
    ic=`<a class="geri" href="${hashYap('sec',s.di,s.ai)}">← ${a.ad}</a>
      <div class="sonuc">
        <div class="renk-buyuk" style="background:${t.hex}"><span style="color:${yaziRengi(t.hex)}">${t.kod}</span></div>
        <div>
          <div class="sec-bas" style="margin:0"><p class="ust-yazi">Seçilen ton</p><p class="yol">${d.ad} › ${a.ad}</p><h2 tabindex="-1">${t.kod}</h2></div>
          <dl class="bilgi"><dt>Renk ailesi</dt><dd>${t.aile}</dd>${diger}</dl>
          <div class="dugmeler"><a class="dugme dolu" href="${hashYap('cark',s.di,s.ai,s.ti)}">Çarkta göster</a><a class="dugme" href="${hashYap('sec')}">Baştan başla</a></div>
          ${alanlar(d)}
          <div class="baslik-k">${a.ad} altındaki tonlar</div>
          <div class="cipler">${a.tonlar.map((u,ti)=>`<a class="cip${u.ikinci?' ikinci':''}" href="${hashYap('sec',s.di,s.ai,ti)}"${ti===s.ti?' aria-current="true"':''}><i style="background:${u.hex}"></i>${u.kod}</a>`).join('')}</div>
        </div>
      </div>`;
  }
  secKutu.innerHTML=adimCubugu(s)+ic;
}

// ---- Çark (önceki sürüm; seçim artık adres çubuğundan gelir) ----
const dilimSay = D.reduce((s,d)=>s+d.alt.reduce((x,a)=>x+a.tonlar.length,0),0);
const adim = 2*Math.PI/dilimSay, bosluk=.004;
const dilimler = [];
let secim=null;

function ciz(){
  svg.innerHTML=''; dilimler.length=0; let aci=-Math.PI/2;
  D.forEach((d,di)=>{
    const dBas=aci, dSon=dBas+d.alt.reduce((s,a)=>s+a.tonlar.length,0)*adim;
    const dRenk=ortaRenk(d.alt.flatMap(asil));
    const gd=el('g',{class:'dilim',tabindex:0,role:'button','aria-label':d.ad},svg);
    el('path',{d:yay(R[0],R[1],dBas+bosluk,dSon-bosluk),fill:dRenk},gd);
    yazi(gd,d.ad,(R[0]+R[1])/2+6,(dBas+dSon)/2,15,yaziRengi(dRenk),650);
    dilimler.push({tur:'duygu',di,g:gd});
    let aBas=dBas;
    d.alt.forEach((a,ai)=>{
      const aSon=aBas+a.tonlar.length*adim, aRenk=ortaRenk(asil(a));
      const ga=el('g',{class:'dilim',tabindex:0,role:'button','aria-label':d.ad+' › '+a.ad},svg);
      el('path',{d:yay(R[1]+3,R[2],aBas+bosluk,aSon-bosluk),fill:aRenk,opacity:.92},ga);
      yazi(ga,a.ad,(R[1]+R[2])/2+2,(aBas+aSon)/2,11.5,yaziRengi(aRenk),600);
      dilimler.push({tur:'alt',di,ai,g:ga});
      a.tonlar.forEach((t,ti)=>{
        const tBas=aBas+ti*adim, tSon=tBas+adim, dis=t.ikinci?R[3]-KISA:R[3];
        const gt=el('g',{class:'dilim'+(t.ikinci?' ikinci':''),tabindex:0,role:'button',
          'aria-label':t.kod+', '+t.aile+(t.ikinci?' — asıl yeri '+t.diger:'')},svg);
        const p=el('path',{d:yay(R[2]+3,dis,tBas+bosluk,tSon-bosluk),fill:t.hex},gt);
        if(t.ikinci){p.setAttribute('stroke','var(--dc-metin)');p.setAttribute('stroke-width','1.3');p.setAttribute('stroke-dasharray','3 2.5')}
        yazi(gt,t.kod.slice(4),(R[2]+dis)/2+4,(tBas+tSon)/2,10,yaziRengi(t.hex),500).classList.add('ton-kod');
        dilimler.push({tur:'ton',di,ai,ti,kod:t.kod,g:gt});
      });
      aBas=aSon;
    });
    aci=dSon;
  });
  const orta=el('g',{},svg);
  el('circle',{r:R[0]-4,fill:'var(--dc-zemin)'},orta);
  const t1=el('text',{y:-6,'text-anchor':'middle','font-size':11,'font-weight':600,'letter-spacing':'.08em',fill:'var(--dc-ikincil)'},orta);t1.textContent='MEKÂN NE';
  const t2=el('text',{y:10,'text-anchor':'middle','font-size':11,'font-weight':600,'letter-spacing':'.08em',fill:'var(--dc-ikincil)'},orta);t2.textContent='HİSSETTİRSİN?';
  dilimler.forEach(s=>{
    const sec=()=>gitHash(hashYap('cark',s.di,s.ai,s.ti));
    s.g.addEventListener('click',sec);
    s.g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();sec()}});
  });
  isaretle();
}
function seciliKod(){return secim&&secim.tur==='ton'?D[secim.di].alt[secim.ai].tonlar[secim.ti].kod:null}
function isaretle(){
  svg.classList.toggle('secimli',!!secim);
  const kod=seciliKod();
  dilimler.forEach(s=>{
    s.g.classList.remove('secili','yakin');
    if(!secim) return;
    const ayniDuygu=s.di===secim.di, ayniAlt=ayniDuygu&&s.ai===secim.ai;
    if(secim.tur==='duygu'){ if(ayniDuygu) s.g.classList.add(s.tur==='duygu'?'secili':'yakin'); }
    else if(secim.tur==='alt'){
      if(s.tur==='alt'&&ayniAlt) s.g.classList.add('secili');
      else if((s.tur==='duygu'&&ayniDuygu)||(s.tur==='ton'&&ayniAlt)) s.g.classList.add('yakin');
    } else {
      if(s.tur==='ton'&&ayniAlt&&s.ti===secim.ti) s.g.classList.add('secili');
      else if(s.tur==='ton'&&s.kod===kod) s.g.classList.add('yakin');                 // aynı tonun öbür yeri
      else if((s.tur==='duygu'&&ayniDuygu)||(s.tur==='alt'&&ayniAlt)||(s.tur==='ton'&&ayniAlt)) s.g.classList.add('yakin');
    }
  });
}
function cipler(di,ai,secTi){
  const a=D[di].alt[ai];
  return `<div class="cipler">${a.tonlar.map((t,ti)=>`<button class="cip${t.ikinci?' ikinci':''}" type="button" data-di="${di}" data-ai="${ai}" data-ti="${ti}" aria-pressed="${ti===secTi}" title="${t.ikinci?'Asıl yeri: '+t.diger:t.aile}"><i style="background:${t.hex}"></i>${t.kod}</button>`).join('')}</div>`;
}
function yaz(){
  const notu=`<div class="baslik-k">Çarkı okumak</div>${lejant}`;
  if(!secim){
    panel.innerHTML=`<p class="ust-yazi">Çarkın tamamı</p><h2 class="buyuk">Duygudan tona</h2>
      <p>Çarkın ortasında duygular, onların çevresinde alt başlıklar, en dışta da tonlar yer alır. Bir duyguya, alt başlığa ya da tona dokunulduğunda ayrıntısı burada açılır.</p>${notu}`;
    return;
  }
  const d=D[secim.di];
  if(secim.tur==='duygu'){
    panel.innerHTML=`<p class="ust-yazi">Duygu</p><h2 class="buyuk">${d.ad}</h2><p>${d.metin}</p>
      ${d.alt.map((a,ai)=>`<div class="baslik-k"><button type="button" data-alt="${ai}">${a.ad}</button></div>${cipler(secim.di,ai,-1)}`).join('')}${alanlar(d)}`;
  } else {
    const a=d.alt[secim.ai];
    if(secim.tur==='alt'){
      panel.innerHTML=`<button class="geri" type="button" data-git="duygu">← ${d.ad}</button><p class="ust-yazi">${d.ad} · Alt duygu</p><h2>${a.ad}</h2><p>${a.metin}</p>
        <div class="baslik-k">Tonlar</div>${cipler(secim.di,secim.ai,-1)}${alanlar(d)}`;
    } else {
      const t=a.tonlar[secim.ti];
      const diger=t.diger?`<dt>${t.ikinci?'Asıl yeri':'Ayrıca'}</dt><dd><button type="button" data-kod="${t.kod}" data-ikinci="${t.ikinci?0:1}">${t.diger}</button></dd>`:'';
      panel.innerHTML=`<button class="geri" type="button" data-git="alt">← ${a.ad}</button><p class="yol">${d.ad} · ${a.ad}</p><h2>${t.kod}</h2>
        <div class="renk-alan" style="background:${t.hex}"></div>
        <dl class="bilgi"><dt>Renk ailesi</dt><dd>${t.aile}</dd>${diger}</dl>
        <div class="baslik-k">${a.ad} altındaki tonlar</div>${cipler(secim.di,secim.ai,secim.ti)}${alanlar(d)}`;
    }
  }
  const git=(di,ai,ti)=>gitHash(hashYap('cark',di,ai,ti));
  panel.querySelectorAll('.cip').forEach(b=>b.addEventListener('click',()=>git(+b.dataset.di,+b.dataset.ai,+b.dataset.ti)));
  panel.querySelectorAll('[data-alt]').forEach(b=>b.addEventListener('click',()=>git(secim.di,+b.dataset.alt)));
  panel.querySelectorAll('[data-kod]').forEach(b=>b.addEventListener('click',()=>{const o=yolBul(b.dataset.kod,b.dataset.ikinci==='1');git(o.di,o.ai,o.ti)}));
  panel.querySelectorAll('.geri').forEach(b=>b.addEventListener('click',()=>b.dataset.git==='duygu'?git(secim.di):git(secim.di,secim.ai)));
}

// ---- Görünümü adres çubuğuna göre kur ----
const gorSec=document.getElementById('gor-sec'), gorCark=document.getElementById('gor-cark');
const sekmeSec=document.getElementById('sekme-sec'), sekmeCark=document.getElementById('sekme-cark');
let sonGor=null;
function uygula(kullanici){
  const s=cozHash(), gorDegisti=s.gor!==sonGor; sonGor=s.gor;
  gorSec.hidden=s.gor!=='sec'; gorCark.hidden=s.gor!=='cark';
  sekmeSec.setAttribute('aria-current',s.gor==='sec'?'page':'false');
  sekmeCark.setAttribute('aria-current',s.gor==='cark'?'page':'false');
  sekmeSec.href=hashYap('sec',s.di,s.ai,s.ti); sekmeCark.href=hashYap('cark',s.di,s.ai,s.ti);   // görünüm değişince seçim korunur
  let hedef;
  if(s.gor==='sec'){ secCiz(s); hedef=secKutu; }
  else {
    secim=s.di===null?null:{tur:s.ai===null?'duygu':s.ti===null?'alt':'ton',di:s.di,ai:s.ai,ti:s.ti};
    isaretle(); yaz(); hedef=innerWidth<=900&&secim?panel:gorCark;
  }
  if(!kullanici) return;
  const bar=document.querySelector('.dc-bar').offsetHeight+60;   // 60: sitenin sabit menüsü
  // Seçicide her adımda içerik değişir → başına kay. Çarkta yalnız görünüme geçişte ya da telefonda panele kay
  // (çarkın üstünde tıklarken sayfa yerinden oynamasın).
  if(s.gor==='sec'||gorDegisti||hedef===panel)
    window.scrollTo({top:hedef.getBoundingClientRect().top+scrollY-bar-8,behavior:hareket?'smooth':'auto'});
  if(s.gor==='sec'){const h=secKutu.querySelector('h2');if(h)h.focus({preventScroll:true})}
}
addEventListener('hashchange',()=>uygula(true));
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!gorCark.hidden) gitHash('#cark')});
ciz();uygula(false);
})();
