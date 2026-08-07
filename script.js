const menu = document.querySelector(".menu");
const nav = document.querySelector(".nav-links");

menu.onclick = () => {

nav.classList.toggle("active");

};

const typing = document.querySelector(".typing");

const words = [

"AI|ML Engineer",

"Software Developer",

"MERN Developer",

"C++ Developer",

];

let wordIndex = 0;
let charIndex = 0;
let deleting = false;

function type(){

const current = words[wordIndex];

if(!deleting){

typing.textContent = current.substring(0,charIndex++);

if(charIndex>current.length){

deleting=true;

setTimeout(type,1000);

return;

}

}else{

typing.textContent = current.substring(0,charIndex--);

if(charIndex<0){

deleting=false;

wordIndex=(wordIndex+1)%words.length;

}

}

setTimeout(type,deleting?60:120);

}

type();

window.addEventListener("scroll",()=>{

document.querySelectorAll(".reveal").forEach(section=>{

const top = section.getBoundingClientRect().top;

if(top<window.innerHeight-100){

section.classList.add("active");

}

});

});

// ===============================
// EXPERIENCE ACCORDION
// ===============================

document.querySelectorAll(".experience-header").forEach(header => {

    header.addEventListener("click", () => {

        const card = header.parentElement;
        const content = card.querySelector(".experience-content");
        const button = card.querySelector(".toggle-btn");

        content.classList.toggle("active");
        button.classList.toggle("active");

    });

});
