const assert=require('node:assert/strict');
const {spawn}=require('node:child_process');
const {chromium}=require('playwright');
(async()=>{
 const server=spawn('python3',['-m','http.server','8767','--bind','127.0.0.1','--directory','dist']);let browser;
 try{
  for(let i=0;i<30;i++){try{await fetch('http://127.0.0.1:8767');break;}catch{await new Promise(r=>setTimeout(r,100));}}
  browser=await chromium.launch({headless:true});const page=await browser.newPage({viewport:{width:390,height:844}});
  await page.addInitScript(()=>{window.spoken=[];window.SpeechSynthesisUtterance=class{constructor(text){this.text=text;}};
    Object.defineProperty(window,'speechSynthesis',{value:{paused:false,speak(u){window.spoken.push(u.text);},pause(){this.paused=true;},resume(){this.paused=false;},cancel(){window.stopped=true;}}});});
  await page.goto('http://127.0.0.1:8767/review-drafts.html');
  await page.locator('main a').first().click();
  assert((await page.textContent('main')).includes('UNAPPROVED'));
  await page.click('#listen');assert((await page.evaluate(()=>window.spoken.length))>0);
  await page.click('#pause');assert.equal(await page.evaluate(()=>speechSynthesis.paused),true);
  await page.click('#pause');assert.equal(await page.evaluate(()=>speechSynthesis.paused),false);
  await page.click('#stop');assert.equal(await page.textContent('#speech-status'),'Stopped.');
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  console.log('PASS: mobile review draft, explicit unapproved label, source links and speech controls');
 }finally{if(browser)await browser.close();server.kill();}
})().catch(e=>{console.error(e);process.exitCode=1});
