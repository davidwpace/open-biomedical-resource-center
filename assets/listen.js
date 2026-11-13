(() => {
  const start=document.getElementById('listen'),pause=document.getElementById('pause'),stop=document.getElementById('stop'),status=document.getElementById('speech-status');
  if(!start)return;
  if(!('speechSynthesis' in window)){start.disabled=pause.disabled=stop.disabled=true;status.textContent='Read aloud is unavailable in this browser. The full text is below.';return;}
  let chunks=[],index=0,generation=0;
  function speak(token){if(token!==generation||index>=chunks.length){if(token===generation)status.textContent='Finished reading.';return;}
    const voice=new SpeechSynthesisUtterance(chunks[index++]);voice.rate=0.95;
    voice.onend=()=>speak(token);voice.onerror=()=>{if(token===generation)status.textContent='Reading stopped. Tap Listen to restart.';};speechSynthesis.speak(voice);}
  start.addEventListener('click',()=>{generation++;speechSynthesis.cancel();const text=document.getElementById('reading').innerText;chunks=text.match(/[^.!?]+[.!?]+|[^.!?]+$/g)||[text];index=0;status.textContent='Reading aloud. You can pause or stop.';speak(generation);});
  pause.addEventListener('click',()=>{if(speechSynthesis.paused){speechSynthesis.resume();status.textContent='Reading aloud.';}else{speechSynthesis.pause();status.textContent='Paused.';}});
  stop.addEventListener('click',()=>{generation++;speechSynthesis.cancel();status.textContent='Stopped.';});
  window.addEventListener('pagehide',()=>{generation++;speechSynthesis.cancel();});
})();
