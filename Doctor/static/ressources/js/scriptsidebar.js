function myFunction() {
    var element = document.getElementById("sidebar");
    element.classList.toggle("side");
  }
/*function activ(){
const mydivclass = document.querySelector('.list-group-item');
// if 'hasClass' is exist on 'mydivclass'
if(mydivclass.classList.contains('activée')) {
console.log("exists")
}
else{
  alert("The URL of this page is: " + window.location.href);
  mydivclass.classList.add("activée");
}
} */
function activ(){
  const element1= document.querySelector('.item1');
  const element2= document.querySelector('.item2');
  const element3= document.querySelector('.item3');
  const element4= document.querySelector('.item4');
  const element5= document.querySelector('.item5');
  const element6= document.querySelector('.item6');
  const element7= document.querySelector('.item7');
  const element8= document.querySelector('.item8');
  const element9= document.querySelector('.item9');
  const element10= document.querySelector('.item10')
  if(window.location.href==='file:///C:/Users/kouss/Desktop/Cabinet%20folders/cabinet-final/dashboarddoc.html'){
  element1.classList.add("activée");
}
else if(window.location.href==='file:///C:/Users/kouss/Desktop/Cabinet%20folders/cabinet-final/dashboarddoccalendar.html'){
  element2.classList.add("activée");
}
else if(window.location.href==='file:///C:/Users/kouss/Desktop/Cabinet%20folders/cabinet-final/dashboarddocpatients.html'){
  element3.classList.add("activée");
}
else if(window.location.href==='file:///C:/Users/kouss/Desktop/Cabinet%20folders/cabinet-final/dashboarddocconsultation.html'){
  element4.classList.add("activée");
}
else if(window.location.href==='file:///C:/Users/kouss/Desktop/Cabinet%20folders/cabinet-final/dashboarddoccertif.html'){
  element5.classList.add("activée");
}
else if(window.location.href==='file:///C:/Users/kouss/Desktop/Cabinet%20folders/cabinet-final/dashboarddocordenance.html'){
  element6.classList.add("activée");
}
else if(window.location.href==='file:///C:/Users/kouss/Desktop/Cabinet%20folders/cabinet-final/dashboarddocrendezvous.html'){
  element7.classList.add("activée");
}
else if(window.location.href==='file:///C:/Users/kouss/Desktop/Cabinet%20folders/cabinet-final/dashboarddocpaiement.html'){
  element8.classList.add("activée");
}
else if(window.location.href==='file:///C:/Users/kouss/Desktop/Cabinet%20folders/cabinet-final/dashboarddocassurance.html'){
  element10.classList.add("activée");
  console.log('activée');
}
else{
  element9.classList.add("activée");
}
}
