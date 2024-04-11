// form.addEventListener('submit', (event) => {
//   event.preventDefault(); 
// });

console.log("hello ji")
let addslide = () => {
  // addslide.counter=5;
let newnodediv=document.createElement("div")
newnodediv.classList.add("slide-topic")
console.log("hello ji")
console.log(newnodediv)

let newnode = document.createElement("input");
//   newnode.classList.add("form-control");
newnode.classList.add("mt-2");
//   newnode.classList.add("skillt");
newnode.type = "text";
//   newnode.name = "skil";
//   newnode.placeholder = "skill";
// lable
console.log("hello ji")
console.log(newnode)

let newnodelabel=document.createElement("label")
// newnodelabel.classList.add("")
newnodelabel.innerHTML="Slide:"
let divskill = document.getElementById("input-columns");

//   newnodediv.innerHTML=newnodelabel
console.log("hello ji")
console.log(newnodelabel)

// newnodediv.innerHTML=newnodelabel
console.log("hello ji")
console.log(newnodediv)

//   let t=newnodediv.innerHTML
//   newnodediv.innerHTML=t+newnode
divskill.append(newnodediv);
newnodediv.appendChild(newnodelabel)
newnodediv.appendChild(newnode)
//    addslide.counter++;
}
// remove skills
function removeslideInputsByClassName() {
let elements = document.querySelectorAll('.slide-topic');
console.log(typeof(elements))
console.log(elements)

let numberOfProperties = (Object.keys(elements).length)-1;
elements[numberOfProperties].remove();
}