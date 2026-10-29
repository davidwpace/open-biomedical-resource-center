"use strict";
(() => {
  const chapters=Array.from(document.querySelectorAll(".story-chapter"));
  if(!chapters.length)return;
  const back=document.getElementById("storyBack");
  const next=document.getElementById("storyNext");
  const progress=document.getElementById("storyCount");
  const fill=document.getElementById("storyFill");
  const label=document.getElementById("storyProgress");
  const mission=document.getElementById("mission");
  if(!back||!next||!progress||!fill||!label||!mission)return;
  let i=0;
  const motion=window.matchMedia("(prefers-reduced-motion: reduce)");
  function show(index,focus=true){
    i=Math.max(0,Math.min(chapters.length-1,index));
    chapters.forEach((c,n)=>{c.hidden=n!==i});
    progress.textContent="Chapter "+(i+1)+" of "+chapters.length;
    label.setAttribute("aria-valuenow",String(i+1));
    fill.style.width=(100*(i+1)/chapters.length)+"%";
    back.disabled=i===0;
    next.textContent=i===chapters.length-1?"Try the mini research task ↓":"Next chapter →";
    if(focus){chapters[i].scrollIntoView({behavior:motion.matches?"auto":"smooth",block:"start"});chapters[i].querySelector("h3")?.focus({preventScroll:true});}
  }
  back.addEventListener("click",()=>show(i-1));
  next.addEventListener("click",()=>{
    if(i<chapters.length-1)show(i+1);
    else{mission.scrollIntoView({behavior:motion.matches?"auto":"smooth",block:"start"});mission.querySelector("h2")?.focus({preventScroll:true});}
  });
  show(0,false);
})();
