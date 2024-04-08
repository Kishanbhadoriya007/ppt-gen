// var crsr = document.querySelector("#cursor")
// var blur = document.querySelector("#cursor-blur")
// document.addEventListener("mousemove",function(dets){
//     crsr.style.left = dets.x+"px"
//     crsr.style.top = dets.y+"px"
//     blur.style.left = dets.x - 250 +"px"
//     blur.style.top = dets.y - 250 +"px"
// })


// gsap.to("#nav",{
//     backgroundColor:"#000",
//     duration:1,
//     height:"120px",
//     scrollTrigger:{
//         trigger:"#nav",
//         scroller:"body",
//         markers:0,
//         start:"top -5%",
//         end:"top -15%",
//         scrub:1,
//     }  
// })

// gsap.to("#main",{
//     backgroundColor : "#000",
//     scrollTrigger:{
//         trigger:"main",
//         scroller:"body",
//         markers:true,
//         start:"top -25%",
//         end:"top -75%",
//         scrub:2,
//     }
// })

// const form = document.getElementById('presentation-form');
// const output = document.getElementById('output');

// form.addEventListener('submit', (event) => {
//   event.preventDefault(); // Prevent default form submission

//   const title = document.getElementById('title').value;
//   const slides = [
//     document.getElementById('slide1').value,
//     document.getElementById('slide2').value,
//     document.getElementById('slide3').value,
//     document.getElementById('slide4').value,
//   ];

//   // Simulate generation logic (replace with actual API call if possible)
//   const generatedText = `**Presentation Title:** ${title}\n\n`;
//   for (let i = 0; i < slides.length; i++) {
//     generatedText += `**Slide ${i + 1}:** ${slides[i]}\n\n`;
//   }

//   output.textContent = generatedText;
// });

const form = document.getElementById('presentation-form');
const output = document.getElementById('output');

form.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent default form submission
});
