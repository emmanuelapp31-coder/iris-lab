# The web page, embedded so it is always bundled with the serverless function.
HTML = r"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Iris Lab</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Public+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#EDF0F4;--sf:#fff;--ink:#1B2238;--mu:#5A6479;--ln:#CBD3E0;--setosa:#C9731A;--versicolor:#2F6FA8;--virginica:#6A3FA3;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#141A2B;--sf:#1E2640;--ink:#EAEEF7;--mu:#A3ADC4;--ln:#36415F;--setosa:#F0A04B;--versicolor:#6FAEE6;--virginica:#B592EA;color-scheme:dark}}
:root[data-theme=dark]{--bg:#141A2B;--sf:#1E2640;--ink:#EAEEF7;--mu:#A3ADC4;--ln:#36415F;--setosa:#F0A04B;--versicolor:#6FAEE6;--virginica:#B592EA;color-scheme:dark}
*,*::before,*::after{box-sizing:inherit}html{scroll-padding-top:env(safe-area-inset-top,0px)}
body{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.5 "Public Sans",system-ui,sans-serif}
main{max-width:1000px;margin:0 auto;padding:24px 20px 48px}
header{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
h1{font:600 clamp(26px,4vw,38px)/1.1 Fraunces,Georgia,serif;margin:0}h2{font:600 18px Fraunces,Georgia,serif;margin:0 0 12px}
.sub{color:var(--mu);margin:4px 0 0}
nav{display:flex;gap:6px;margin:20px 0;border-bottom:1px solid var(--ln);overflow-x:auto}
nav button{border:0;border-bottom:3px solid transparent;border-radius:0;padding:10px 14px;font-weight:500;color:var(--mu);white-space:nowrap}
nav button[aria-selected=true]{color:var(--ink);border-color:var(--versicolor)}
button,select,input{font:500 14px "Public Sans",sans-serif;color:var(--ink)}
button{background:transparent;border:1px solid var(--ln);border-radius:8px;padding:8px 12px;cursor:pointer}button:hover{border-color:var(--ink)}
select,input[type=number]{background:var(--sf);border:1px solid var(--ln);border-radius:8px;padding:7px 8px}
:focus-visible{outline:3px solid var(--versicolor);outline-offset:2px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}@media(max-width:760px){.grid{grid-template-columns:1fr}}
.panel{background:var(--sf);border:1px solid var(--ln);border-radius:14px;padding:20px;margin-bottom:20px}
.row{margin-bottom:14px}.row label{display:flex;justify-content:space-between;align-items:center;font-weight:500;margin-bottom:4px}
.row input[type=number]{width:84px;text-align:right}input[type=range]{width:100%;accent-color:var(--versicolor);height:26px}
.chips{display:flex;gap:8px;flex-wrap:wrap}.res{text-align:center}
#name{font:600 clamp(24px,4vw,32px) Fraunces,Georgia,serif;margin:4px 0 0;text-transform:capitalize}#conf{color:var(--mu);margin:0 0 6px}
svg{display:block;max-width:100%;height:auto}#glyph{width:100%;max-width:240px;margin:0 auto}
.pt{transition:transform .35s,opacity .35s}@media(prefers-reduced-motion:reduce){.pt{transition:none}}
.bar{display:grid;grid-template-columns:86px 1fr 52px;gap:10px;align-items:center;margin:6px 0;font-size:14px;text-align:left}
.tr{height:10px;background:var(--bg);border-radius:5px;overflow:hidden}.fl{height:100%;transition:width .35s}.bar span:last-child{text-align:right;font-variant-numeric:tabular-nums}
.hist{list-style:none;padding:0;margin:0}.hist li button{width:100%;text-align:left;border:0;border-bottom:1px solid var(--ln);border-radius:0;display:flex;justify-content:space-between;gap:8px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}
.scroll{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums}
th,td{padding:7px 10px;border-bottom:1px solid var(--ln);text-align:right}th:first-child,td:first-child,td.l,th.l{text-align:left}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:16px}.card{border:1px solid var(--ln);border-radius:10px;padding:12px}
.card b{display:block;font:600 26px Fraunces,Georgia,serif}.mu{color:var(--mu);font-size:14px}.err{color:#C0392B}
.drop{border:2px dashed var(--ln);border-radius:12px;padding:24px;text-align:center}
</style></head><body><main>
<header><div><h1>Iris Lab</h1><p class="sub">Predict, explore and test an iris species classifier.</p></div>
<button id="theme" type="button" aria-label="Toggle light or dark theme">Theme</button></header>
<nav role="tablist" id="tabs"></nav>

<section id="t-predict"><div class="grid">
 <div class="panel"><h2>Measurements (cm)</h2><div id="inputs"></div><div class="chips" id="samples"></div></div>
 <div>
  <div class="panel res" aria-live="polite"><svg id="glyph" viewBox="-150 -150 300 300" role="img" aria-label="Petals sized by probability"></svg>
   <p id="name"></p><p id="conf"></p><div id="bars"></div></div>
  <div class="panel"><h2>History</h2><ul class="hist" id="hist"></ul><p class="mu" id="hnone">Release a slider to log a prediction here.</p></div>
 </div></div></section>

<section id="t-explore" hidden><div class="panel">
 <h2>Where your flower sits among the 147 training flowers</h2>
 <div class="chips" style="margin-bottom:12px"><label>X axis <select id="ax"></select></label><label>Y axis <select id="ay"></select></label></div>
 <div class="scroll"><svg id="sc" viewBox="0 0 640 380" role="img" aria-label="Scatter plot of training data with your measurements marked" style="min-width:480px;width:100%"></svg></div>
 <div class="chips mu" id="leg" style="margin-top:8px"></div>
 <p class="mu">Setosa separates cleanly on the petal measurements. Versicolor and virginica overlap, which is where the model makes its mistakes. The ringed marker is the flower from the Predict tab.</p></div></section>

<section id="t-batch" hidden><div class="panel"><h2>Batch prediction</h2>
 <div class="drop"><p style="margin-top:0">Upload a CSV with columns <code>sepal_length, sepal_width, petal_length, petal_width</code>.<br><span class="mu">Headers are optional if the first four columns are the measurements in that order. Up to 1,000 rows.</span></p>
 <input type="file" id="file" accept=".csv,text/csv" aria-label="CSV file"> <button type="button" id="demo">Try sample data</button></div>
 <p id="bmsg" class="mu" role="status"></p><div class="scroll" id="btab"></div><p><button type="button" id="dl" hidden>Download results (CSV)</button></p></div></section>

<section id="t-model" hidden><div class="panel"><h2>Model report</h2><div id="info" class="mu">Loading…</div></div></section>
</main>
<script>
const F=["sepal_length","sepal_width","petal_length","petal_width"],C=["setosa","versicolor","virginica"];
const L={sepal_length:"Sepal length",sepal_width:"Sepal width",petal_length:"Petal length",petal_width:"Petal width"};
const R={sepal_length:[4,8,5.8],sepal_width:[2,4.5,3],petal_length:[1,7,4.3],petal_width:[.1,2.5,1.3]};
const S=[["Typical setosa",[5,3.4,1.5,.2]],["Typical versicolor",[5.9,2.8,4.3,1.3]],["Typical virginica",[6.6,3,5.5,2]],["Hard case",[6,2.7,5.1,1.6]]];
const $=id=>document.getElementById(id),col=c=>`var(--${c})`,cap=s=>s[0].toUpperCase()+s.slice(1);
let data=[],cur=null,hist=[],tok=0,lastBatch=[];

// tabs
const T=[["predict","Predict"],["explore","Explore data"],["batch","Batch CSV"],["model","Model report"]];
T.forEach(([id,n],i)=>{const b=document.createElement("button");b.type="button";b.role="tab";b.textContent=n;b.id="tab-"+id;b.setAttribute("aria-selected",i==0);
 b.onclick=()=>{T.forEach(([k])=>{$("t-"+k).hidden=k!=id;$("tab-"+k).setAttribute("aria-selected",k==id)});if(id=="explore")draw();if(id=="model")info()};$("tabs").appendChild(b)});
$("theme").onclick=()=>{const d=document.documentElement,dark=(d.dataset.theme||(matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light"))=="dark";d.dataset.theme=dark?"light":"dark"};

// inputs
const num={},rng={};
F.forEach(f=>{const[lo,hi,d]=R[f],r=document.createElement("div");r.className="row";
 r.innerHTML=`<label for="n_${f}">${L[f]}<input type="number" id="n_${f}" min="0.1" max="15" step="0.1" value="${d}"></label><input type="range" id="r_${f}" min="${lo}" max="${hi}" step="0.1" value="${d}" aria-label="${L[f]} slider">`;
 $("inputs").appendChild(r);num[f]=r.querySelector("[type=number]");rng[f]=r.querySelector("[type=range]");
 rng[f].oninput=()=>{num[f].value=rng[f].value;go()};rng[f].onchange=()=>log();
 num[f].oninput=()=>{rng[f].value=num[f].value;go()};num[f].onchange=()=>log()});
S.forEach(([n,v])=>{const b=document.createElement("button");b.type="button";b.textContent=n;b.onclick=()=>{set(v);log()};$("samples").appendChild(b)});
const set=v=>{F.forEach((f,i)=>{num[f].value=v[i];rng[f].value=v[i]});go()};
const vals=()=>F.map(f=>parseFloat(num[f].value));

// glyph
$("glyph").innerHTML=C.map((c,k)=>`<g transform="rotate(${k*120})"><ellipse class="pt" id="p_${c}" cx="0" cy="-72" rx="34" ry="62" style="fill:${col(c)};transform-origin:0 0"/></g>`).join("")+`<circle r="14" style="fill:var(--sf);stroke:var(--ln)"/>`;

async function post(url,body){const r=await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});const j=await r.json();if(!r.ok)throw new Error(j.error||"Request failed");return j}
let timer;const go=()=>{clearTimeout(timer);timer=setTimeout(update,60)};
async function update(){const x=vals(),t=++tok;let o;
 try{if(x.some(v=>!(v>0&&v<=15)))throw new Error("Enter values between 0 and 15 cm");o=await post("/predict",Object.fromEntries(F.map((f,i)=>[f,x[i]])))}
 catch(e){$("name").textContent="No prediction";$("conf").textContent=e.message;return}
 if(t!=tok)return;const p=C.map(c=>o.probabilities[c]),best=o.species;cur={x,species:best,p};
 C.forEach((c,k)=>{const e=$("p_"+c);e.style.transform=`scale(${.25+.75*p[k]})`;e.style.opacity=.35+.65*p[k]});
 $("name").textContent="Iris "+best;$("name").style.color=col(best);$("conf").textContent=(Math.max(...p)*100).toFixed(1)+"% confident";
 $("bars").innerHTML=C.map((c,k)=>`<div class="bar"><span>${c}</span><div class="tr"><div class="fl" style="width:${p[k]*100}%;background:${col(c)}"></div></div><span>${(p[k]*100).toFixed(1)}%</span></div>`).join("");
 if(!$("t-explore").hidden)draw()}
function log(){if(!cur)return;const k=cur.x.join();if(hist[0]&&hist[0].x.join()==k)return;hist.unshift(cur);hist=hist.slice(0,8);
 $("hnone").hidden=true;$("hist").innerHTML=hist.map((h,i)=>`<li><button type="button" data-i="${i}"><span><i class="dot" style="background:${col(h.species)}"></i>${h.species}</span><span class="mu">${h.x.join(" · ")}</span></button></li>`).join("");
 $("hist").querySelectorAll("button").forEach(b=>b.onclick=()=>set(hist[b.dataset.i].x))}

// explore
F.forEach(f=>{["ax","ay"].forEach((id,k)=>{const o=new Option(L[f],f,false,k==0?f=="petal_length":f=="petal_width");$(id).add(o)})});
$("ax").onchange=$("ay").onchange=()=>draw();
$("leg").innerHTML=C.map(c=>`<span><i class="dot" style="background:${col(c)}"></i>${c}</span>`).join("")+`<span>◯ your flower</span>`;
function draw(){if(!data.length)return;const a=F.indexOf($("ax").value),b=F.indexOf($("ay").value),W=640,H=380,m={l:50,r:16,t:12,b:44};
 const ext=i=>{const v=data.map(d=>d[i]);if(cur)v.push(cur.x[i]);const lo=Math.min(...v),hi=Math.max(...v),p=(hi-lo)*.06;return[lo-p,hi+p]};
 const[xl,xh]=ext(a),[yl,yh]=ext(b),X=v=>m.l+(v-xl)/(xh-xl)*(W-m.l-m.r),Y=v=>H-m.b-(v-yl)/(yh-yl)*(H-m.t-m.b);let s="";
 for(let i=0;i<=5;i++){const xv=xl+(xh-xl)*i/5,yv=yl+(yh-yl)*i/5;
  s+=`<line x1="${X(xv)}" x2="${X(xv)}" y1="${m.t}" y2="${H-m.b}" style="stroke:var(--ln)" stroke-width=".5"/><text x="${X(xv)}" y="${H-m.b+16}" text-anchor="middle" font-size="11" style="fill:var(--mu)">${xv.toFixed(1)}</text>`;
  s+=`<line y1="${Y(yv)}" y2="${Y(yv)}" x1="${m.l}" x2="${W-m.r}" style="stroke:var(--ln)" stroke-width=".5"/><text x="${m.l-6}" y="${Y(yv)+4}" text-anchor="end" font-size="11" style="fill:var(--mu)">${yv.toFixed(1)}</text>`}
 s+=`<text x="${W/2}" y="${H-6}" text-anchor="middle" font-size="12" style="fill:var(--ink)">${L[F[a]]} (cm)</text><text transform="translate(12 ${H/2}) rotate(-90)" text-anchor="middle" font-size="12" style="fill:var(--ink)">${L[F[b]]} (cm)</text>`;
 s+=data.map(d=>`<circle cx="${X(d[a])}" cy="${Y(d[b])}" r="4.5" opacity=".7" style="fill:${col(d[4])}"><title>${d[4]}: ${d[a]}, ${d[b]}</title></circle>`).join("");
 if(cur)s+=`<circle cx="${X(cur.x[a])}" cy="${Y(cur.x[b])}" r="10" fill="none" stroke-width="3" style="stroke:var(--ink)"/><circle cx="${X(cur.x[a])}" cy="${Y(cur.x[b])}" r="3" style="fill:var(--ink)"/>`;
 $("sc").innerHTML=s}
fetch("/api/data").then(r=>r.json()).then(d=>{data=d;draw()}).catch(()=>{});

// batch
function parse(t){const ln=t.trim().split(/\r?\n/).map(l=>l.split(",").map(s=>s.trim().replace(/^"|"$/g,"")));if(!ln.length)return null;
 const h=ln[0].map(s=>s.toLowerCase().replace(/[\s.]+/g,"_"));let ix=F.map(f=>h.indexOf(f)),st=1;
 if(ix.some(i=>i<0)){if(ln[0].length>=4&&ln[0].slice(0,4).every(v=>v!==""&&!isNaN(v))){ix=[0,1,2,3];st=0}else return null}
 return ln.slice(st).filter(r=>r.length>=4).map(r=>ix.map(i=>parseFloat(r[i])))}
async function runBatch(text){const rows=parse(text),m=$("bmsg");m.className="mu";
 if(!rows||!rows.length){m.className="err";m.textContent="Couldn’t find the four measurement columns. Check the header names.";return}
 if(rows.length>1000){m.className="err";m.textContent="Too many rows: the limit is 1,000.";return}
 try{const o=await post("/predict_batch",{rows:rows.map(r=>Object.fromEntries(F.map((f,i)=>[f,r[i]])))});
  lastBatch=rows.map((r,i)=>[...r,o.results[i].species,Math.max(...Object.values(o.results[i].probabilities))]);
  const cnt={};lastBatch.forEach(r=>cnt[r[4]]=(cnt[r[4]]||0)+1);
  m.textContent=`${rows.length} rows predicted: `+C.filter(c=>cnt[c]).map(c=>`${cnt[c]} ${c}`).join(", ")+(rows.length>200?" (showing first 200)":"");
  $("btab").innerHTML=`<table><thead><tr><th>#</th>${F.map(f=>`<th>${L[f]}</th>`).join("")}<th class="l">Species</th><th>Confidence</th></tr></thead><tbody>`+
   lastBatch.slice(0,200).map((r,i)=>`<tr><td>${i+1}</td>${r.slice(0,4).map(v=>`<td>${v}</td>`).join("")}<td class="l"><i class="dot" style="background:${col(r[4])}"></i>${r[4]}</td><td>${(r[5]*100).toFixed(1)}%</td></tr>`).join("")+"</tbody></table>";
  $("dl").hidden=false}
 catch(e){m.className="err";m.textContent=e.message}}
$("file").onchange=e=>{const f=e.target.files[0];if(f)f.text().then(runBatch)};
$("demo").onclick=()=>runBatch("sepal_length,sepal_width,petal_length,petal_width\n5.1,3.5,1.4,0.2\n4.9,3.0,1.4,0.2\n7.0,3.2,4.7,1.4\n6.4,3.2,4.5,1.5\n6.3,3.3,6.0,2.5\n5.8,2.7,5.1,1.9\n6.0,2.7,5.1,1.6");
$("dl").onclick=()=>{const csv=[...F,"predicted_species","confidence"].join(",")+"\n"+lastBatch.map(r=>r.join(",")).join("\n");
 const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([csv],{type:"text/csv"}));a.download="iris_predictions.csv";a.click()};

// model report
let loaded=false;async function info(){if(loaded)return;try{const i=await (await fetch("/api/info")).json(),pc=v=>(v*100).toFixed(1)+"%";loaded=true;
 $("info").className="";$("info").innerHTML=`<div class="cards"><div class="card"><b>${pc(i.test_accuracy)}</b><span class="mu">Held-out test accuracy (${i.n_test} flowers)</span></div><div class="card"><b>${pc(i.cv_accuracy)}</b><span class="mu">5-fold cross-validation</span></div><div class="card"><b>${i.n_total}</b><span class="mu">Unique training rows</span></div></div>
 <h2>Confusion matrix (test set)</h2><div class="scroll"><table><thead><tr><th>Actual ↓ / Predicted →</th>${C.map(c=>`<th>${c}</th>`).join("")}</tr></thead><tbody>${i.confusion.map((r,a)=>`<tr><td class="l">${C[a]}</td>${r.map((v,b)=>`<td style="${a==b?"background:color-mix(in srgb,"+col(C[a])+" "+(15+v*6)+"%,transparent);":""}font-weight:${a==b?600:400}">${v}</td>`).join("")}</tr>`).join("")}</tbody></table></div>
 <h2 style="margin-top:20px">Per-class results</h2><div class="scroll"><table><thead><tr><th>Species</th><th>Precision</th><th>Recall</th></tr></thead><tbody>${C.map(c=>`<tr><td class="l">${c}</td><td>${pc(i.per_class[c].precision)}</td><td>${pc(i.per_class[c].recall)}</td></tr>`).join("")}</tbody></table></div>
 <p>${i.notes}</p>`}catch(e){$("info").textContent="Couldn’t load the model report."}}
update();
</script></body></html>
"""
