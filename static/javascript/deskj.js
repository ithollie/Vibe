const  ms =  {};//Model
const  vs =  {};//view
const  cs =  {};//Controller

cs.initialize  =  function(eventObject){
  let likes = document.getElementById("likes");
  let dislikes = document.getElementById("dislikes");
  let comments = document.getElementById("comments");
  
  let comments2 = document.getElementById("comments2");
//   let image = document.getElementById("mg");
  
  
   
  
  likes.addEventListener('click', cs.message);
  dislikes.addEventListener('click', cs.wrong);
  comments.addEventListener('click',cs.message);
  comments2.addEventListener('click',cs.message);
}
cs.message = function(event){
  console.log(event.target);
  
}
cs.wrong = function(event){
   let y = parseInt(event.target.childNodes[1].innerText) + 1;
   event.target.childNodes[1].innerText = y;
      
      $.ajax({
          type: "POST",
          url: "/dislikes",
          data: JSON.stringify({ "title" :$("#blogname")[0].textContent,
          "email":$("#blogemail")[0].textContent, 
           "_id" :$("#blogemail")[0].attributes[1].value,
           "current_num":parseInt(event.target.childNodes[1].innerText)
          } ),
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          success: function (data) {
              alert(JSON.stringify(data['title']));
          }
       })
       event.preventDefault();
}
cs.right  =  function(event){
 
      let y = parseInt(event.target.childNodes[1].innerText) + 1;
      event.target.childNodes[1].innerText = y;
      
      $.ajax({
          type: "POST",
          url: "/likes",
          data: JSON.stringify({ "title" :$("#blogname")[0].textContent,
          "email":$("#blogemail")[0].textContent, 
           "_id" :$("#blogemail")[0].attributes[1].value,
           "current_num":parseInt(event.target.childNodes[1].innerText)
          } ),
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          success: function (data) {
              alert(JSON.stringify(data['title']));
          }
       })
       event.preventDefault();
}
