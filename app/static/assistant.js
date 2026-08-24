(() => {
  "use strict";
  const copy={
    ar:{name:"مساعد الموظفين",status:"معزول · للقراءة والإرشاد فقط",welcome:"مرحباً. أشرح إجراءات العناوين والسجل العقاري والصلاحيات والأمن والعمل دون إنترنت. لا أستطيع تنفيذ أي إجراء في النظام.",placeholder:"اكتب سؤالك…",send:"إرسال",close:"إغلاق",thinking:"جارٍ البحث في دليل النظام…",error:"تعذر الوصول إلى المساعد المحلي.",notice:"إرشاد فقط · لا ينفذ أو يعتمد أي معاملة",prompts:["كيف أعتمد عنواناً؟","ما هي أدوار الموظفين؟","كيف أعمل بأمان دون إنترنت؟"]},
    en:{name:"Staff assistant",status:"Isolated · read-only guidance",welcome:"Hello. I explain address, cadastre, role, security and offline procedures. I cannot perform any action in the system.",placeholder:"Ask a question…",send:"Send",close:"Close",thinking:"Searching the system handbook…",error:"The local assistant is unavailable.",notice:"Guidance only · cannot execute or approve cases",prompts:["How do I approve an address?","What are the staff roles?","How do I work safely offline?"]},
    de:{name:"Mitarbeiter-Assistent",status:"Isoliert · nur lesende Beratung",welcome:"Hallo. Ich erkläre Adress-, Kataster-, Rollen-, Sicherheits- und Offline-Prozesse. Ich kann keine Aktion im System ausführen.",placeholder:"Frage eingeben…",send:"Senden",close:"Schließen",thinking:"Systemhandbuch wird durchsucht…",error:"Der lokale Assistent ist nicht erreichbar.",notice:"Nur Beratung · kann keine Vorgänge ausführen oder freigeben",prompts:["Wie genehmige ich eine Adresse?","Welche Mitarbeiterrollen gibt es?","Wie arbeite ich sicher offline?"]}
  };
  const esc=value=>String(value??"").replace(/[&<>"']/g,char=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
  const language=()=>["ar","en","de"].includes(document.documentElement.lang)?document.documentElement.lang:"ar";
  document.body.insertAdjacentHTML("beforeend",`<button id="assistant-launcher" class="assistant-launcher hidden" type="button" aria-haspopup="dialog"><span class="assistant-spark">✦</span><span id="assistant-launcher-label"></span></button><section id="assistant-panel" class="assistant-panel hidden" role="dialog" aria-modal="false"><header class="assistant-head"><div class="assistant-avatar">✦</div><div><strong id="assistant-name"></strong><small id="assistant-status"></small></div><button id="assistant-close" type="button">×</button></header><div id="assistant-messages" class="assistant-messages"></div><div id="assistant-prompts" class="assistant-prompts"></div><form id="assistant-form" class="assistant-form"><textarea id="assistant-input" rows="1" maxlength="1200"></textarea><button id="assistant-send" type="submit">➤</button></form><footer id="assistant-notice" class="assistant-notice"></footer></section>`);
  const launcher=document.querySelector("#assistant-launcher"),panel=document.querySelector("#assistant-panel"),messages=document.querySelector("#assistant-messages"),input=document.querySelector("#assistant-input");
  let welcomed=false;
  function add(role,text,sources=[],notice=""){
    const sourceMarkup=sources.length?`<div class="assistant-sources">${sources.map(source=>`<span>${esc(source.replace("docs/",""))}</span>`).join("")}</div>`:"";
    messages.insertAdjacentHTML("beforeend",`<article class="assistant-message ${role}"><div>${esc(text).replace(/\n/g,"<br>")}</div>${sourceMarkup}${notice?`<small>${esc(notice)}</small>`:""}</article>`);
    messages.scrollTop=messages.scrollHeight;
  }
  function renderLanguage(){
    const text=copy[language()];
    document.querySelector("#assistant-launcher-label").textContent=text.name;document.querySelector("#assistant-name").textContent=text.name;document.querySelector("#assistant-status").textContent=text.status;document.querySelector("#assistant-close").setAttribute("aria-label",text.close);input.placeholder=text.placeholder;document.querySelector("#assistant-send").setAttribute("aria-label",text.send);document.querySelector("#assistant-notice").textContent=text.notice;
    document.querySelector("#assistant-prompts").innerHTML=text.prompts.map(prompt=>`<button type="button">${esc(prompt)}</button>`).join("");
    document.querySelectorAll("#assistant-prompts button").forEach((button,index)=>button.onclick=()=>ask(text.prompts[index]));
    if(!welcomed){add("assistant",text.welcome);welcomed=true}
  }
  function syncVisibility(){launcher.classList.toggle("hidden",!localStorage.getItem("sna_token"));if(!localStorage.getItem("sna_token"))panel.classList.add("hidden")}
  async function ask(question){
    question=(question||input.value).trim();if(!question)return;input.value="";add("user",question);
    const waiting=document.createElement("article");waiting.className="assistant-message assistant waiting";waiting.textContent=copy[language()].thinking;messages.appendChild(waiting);messages.scrollTop=messages.scrollHeight;
    try{
      const response=await fetch("/api/v1/assistant/query",{method:"POST",headers:{"Content-Type":"application/json","Authorization":"Bearer "+localStorage.getItem("sna_token"),"X-Device-Time":new Date().toISOString()},body:JSON.stringify({question,language:language()})});
      const data=await response.json();waiting.remove();if(!response.ok)throw Error(data.error||"request_failed");add("assistant",data.answer,data.sources,data.notice);
    }catch(_){waiting.remove();add("assistant",copy[language()].error)}
  }
  launcher.onclick=()=>{panel.classList.toggle("hidden");launcher.setAttribute("aria-expanded",String(!panel.classList.contains("hidden")));if(!panel.classList.contains("hidden"))input.focus()};
  document.querySelector("#assistant-close").onclick=()=>{panel.classList.add("hidden");launcher.setAttribute("aria-expanded","false")};
  document.querySelector("#assistant-form").onsubmit=event=>{event.preventDefault();ask()};
  input.onkeydown=event=>{if(event.key==="Enter"&&!event.shiftKey){event.preventDefault();ask()}};
  new MutationObserver(syncVisibility).observe(document.body,{attributes:true,attributeFilter:["data-user-role"]});
  document.querySelector("#language").addEventListener("change",()=>setTimeout(renderLanguage));
  renderLanguage();syncVisibility();
})();
