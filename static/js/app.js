const form=document.getElementById('uploadForm');
const input=document.getElementById('resume');
const fileName=document.getElementById('fileName');
const status=document.getElementById('status');
const results=document.getElementById('results');
const dropZone=document.getElementById('dropZone');
const analyzeBtn=document.getElementById('analyzeBtn');

input.addEventListener('change',()=>{if(input.files.length){fileName.textContent=input.files[0].name;dropZone.classList.add('file-selected')}});
['dragenter','dragover'].forEach(e=>dropZone.addEventListener(e,ev=>{ev.preventDefault();dropZone.classList.add('dragover')}));
['dragleave','drop'].forEach(e=>dropZone.addEventListener(e,ev=>{ev.preventDefault();dropZone.classList.remove('dragover')}));
dropZone.addEventListener('drop',ev=>{if(ev.dataTransfer.files.length){input.files=ev.dataTransfer.files;fileName.textContent=ev.dataTransfer.files[0].name;dropZone.classList.add('file-selected')}});

function setScoreRing(score){const ring=document.querySelector('.score-ring');ring.style.background=`conic-gradient(var(--purple) ${score*3.6}deg,#ececf3 ${score*3.6}deg)`}
function esc(s){return String(s).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]))}

form.addEventListener('submit',async e=>{
 e.preventDefault();
 if(!input.files.length)return;
 status.innerHTML='<span>●</span> Reading your resume and generating insights...';
 analyzeBtn.disabled=true;analyzeBtn.innerHTML='<span>Analyzing...</span><b>✦</b>';results.classList.add('hidden');
 try{
  const response=await fetch('/analyze',{method:'POST',body:new FormData(form)});
  const result=await response.json(); if(!response.ok)throw new Error(result.error||'Analysis failed.');
  const a=result.ats,c=result.career,score=a.score;
  document.getElementById('atsScore').textContent=score;document.getElementById('topCareer').textContent=c.top_career;document.getElementById('confidence').textContent=c.confidence+'%';document.getElementById('confidenceBar').style.width=c.confidence+'%';
  document.getElementById('wordCount').textContent=a.word_count;document.getElementById('sectionCount').textContent=a.sections_found.length;document.getElementById('skillCount').textContent=a.skills_found.length;document.getElementById('skillCount2').textContent=a.skills_found.length;setScoreRing(score);
  const skills=document.getElementById('skills');skills.innerHTML=a.skills_found.length?a.skills_found.map(s=>`<span class="chip">${esc(s)}</span>`).join(''):'<span class="chip">No skills detected</span>';
  const careers=document.getElementById('careers');careers.innerHTML=c.recommendations.map(item=>{const pct=Math.min(item.score*20,100);return `<div class="career-row"><div class="career-row-top"><strong>${esc(item.career)}</strong><span class="career-percent">${pct}% match</span></div><div class="career-keywords">${item.matched_keywords.length?esc(item.matched_keywords.join(', ')):'No direct keyword match'}</div><div class="bar"><span style="width:${pct}%"></span></div></div>`}).join('');
  const suggestions=document.getElementById('suggestions');suggestions.innerHTML=a.suggestions.map(x=>`<div class="suggestion">${esc(x)}</div>`).join('');
  results.classList.remove('hidden');status.innerHTML='<span>●</span> Analysis complete — scroll down to explore your report.';results.scrollIntoView({behavior:'smooth',block:'start'});
 }catch(err){status.innerHTML='⚠ '+esc(err.message);}
 finally{analyzeBtn.disabled=false;analyzeBtn.innerHTML='<span>Analyze Resume</span><b>→</b>';}
});
