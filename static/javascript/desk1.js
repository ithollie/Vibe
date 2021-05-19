const  Model =  {};//Model
const  View =  {};//view
const  Controller =  {};//Controller
const  Objects    =  {};//Objects 

Objects.object_initialize = function(eventObject){
   likes_objects   = new Likes(Controller,  View, Model);
   request_objects = new Requests(Controller, View , Model)
}

Controller.initialize  =  function(eventObject){
  View.send  =       document.querySelectorAll("#send");
  View.holder    =   document.querySelectorAll(".holder");
  View.commentfirst = document.getElementById("fname");
  View.commentlast  = document.getElementById("lname");
  View.commentSubject = document.getElementById("suject");

  View.subject  = document.getElementById("subject");
  View.comdiv =   document.getElementById("comdiv");
  View.likes =    document.getElementById("likes");
  View.dislikes = document.getElementById("dislikes");
  View.comments = document.getElementById("comments");
  View.insertComments =  document.getElementById("insertComment");
  View.popup = document.getElementById("myPopup");
  
  View.requests  =  document.querySelector("#requests");
  
  View.titles     =  document.querySelectorAll("#title");
  View.titlesNum    =  document.querySelectorAll("#spcomments");
  //View.acceptedRequest  =  document
  View.commentAll = document.querySelectorAll("#comments");
  View.requestAll = document.querySelectorAll("#requests");
  View.likesAll   = document.querySelectorAll('#likes');
  View.dislikesAll = document.querySelectorAll('#dislikes');
  View.createRequestsAll = document.querySelectorAll("#createRequests");
  View.tubs  = document.querySelectorAll(".tub");
 
 View.comments.addEventListener('click',Controller.comments);
//  View.insertComments.addEventListener('click', Controller.insertComment);
 
 
 View.send.forEach(elements=>{
    elements.addEventListener('click', Controller.sendComment);
 })
  View.createRequestsAll.forEach(elements=>{
     elements.addEventListener('click',  Controller.message);
 })

  View.commentAll.forEach(elements=>{
      elements.addEventListener('click',Controller.message);
 })
 
   View.likesAll.forEach(elements=>{
      
      elements.addEventListener('click', Controller.likes)
  })
  
   View.dislikesAll.forEach(elements=>{
      elements.addEventListener('click', Controller.dislikes)
  })
  
   View.requestAll.forEach(element=>{
      element.addEventListener("click",Controller.requests);
  })
  
   View.tubs.forEach(element=>{
      element.addEventListener("click", Controller.reacte);
  })
  
  
}
Controller.change  = function(title,number){
	View.titles.forEach(likes=>{
		if(likes.childNodes[1].childNodes[5].attributes[1].value ==  title){
		   likes.childNodes[1].childNodes[5].childNodes[1].childNodes[1].innerText= number+1;
        }
	})
}
Controller.title = function(event){
	var   value;
	var   number; 
	View.titles.forEach(likes=>{
	    
		if(likes.childNodes[1].childNodes[5].attributes[1].value ==  event){
		   number  = likes.childNodes[1].childNodes[5].childNodes[1].childNodes[1].innerText;
		   value = likes.childNodes[1].childNodes[5].attributes[1].value;
        }
		
	})
	return  number;

}
Controller.myFunction =  function(event){
    console.log("hello Ibrahim There is no doubt that  life  is black and  white");
    let show = document.getElementById("myPopup")
    show.classList.toggle("show");
}

Controller.insertComment = function(event){
  console.log(event);
    $.ajax({
          type: "POST",
          url: "/comment",
          data: JSON.stringify({
           
          "login_name":$("#login_user")[0].innerText,
          "user_email":$("#login_email")[0].innerText, 
          "login_id":$("#login_user_id")[0].attributes[1].nodeValue,
           
          "title":event.path[2].attributes[1].value,
          "email":event.path[2].attributes[2].value,
          "comment":event.path[2].attributes[2].value,
          "_id":event.path[2].attributes[3].value
          } ),
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          success: function (data) {
              console.log(data);
              
          }
      })
      event.preventDefault();
}

Controller.comments  = function(event){
    // event.target.style.visibility = 'visible';
    console.log(event);
    alert("comdiv has been  clicked hey");
}

Controller.sendComment = function(event){
    
    console.log($(".iden")[0].innerText);
    console.log($("#header")[0].attributes[2].value);
    console.log($("#header")[0].attributes[1].value);
    
    var li = document.createElement("li");
    var inputValue  =  event.target.parentNode.childNodes[1].value;
    var infor       =  event.target.parentNode.childNodes[1].value;
    var title       =  event.target.parentNode.attributes[0].value;
    var number      =  parseInt(Controller.title(title));   
    var t = document.createTextNode(inputValue);
    
    li.appendChild(t);
    
    if (inputValue === '') {
        alert("You must write something!");
    } else {
        Controller.change(title, number);
       $.ajax({
              type: "POST",
              url: "/commente",
              data: JSON.stringify({
               
              "name":$(".iden").innerText,
              "mail":$("#header")[0].attributes[1].value, 
              "id":$("#header")[0].attributes[2].value,
               
              "title":event.target.attributes[2].value,
              "email":event.target.attributes[3].value,
              "comment":infor,
              "_id":event.target.attributes[4].value
              } ),
              contentType: "application/json; charset=utf-8",
              dataType: "json",
              success: function (data) {
                  console.log(data);
                  
              }
          })
                  event.preventDefault();
       for(let i = 0; i < View.holder.length; i++){
 	        if (View.holder[i].attributes[1].value == title){   
                 View.holder[i].appendChild(li);
                 event.target.parentNode.childNodes[1].value ="";
                 
            }
        }
        
    }
   
    
}

Controller.dislikes =  function(event){
   console.log(event);
   console.log("number" + event.path[1].childNodes[1].innerText);
   console.log("email" +  event.path[2].attributes[2].nodeValue);
   console.log("title" +  event.path[2].attributes[1].nodeValue)
   console.log("_id"  +   event.path[2].attributes[3].nodeValue)
   
   let y = parseInt(event.path[1].childNodes[1].innerText) + 1;
   event.path[1].childNodes[1].innerText = y;
      
      $.ajax({
          type: "POST",
          url: "/dislikes",
          data: JSON.stringify({
          "title":event.path[2].attributes[1].nodeValue,
          "email":event.path[2].attributes[2].nodeValue, 
          "_id":event.path[2].attributes[3].nodeValue,
           "current_num":parseInt(event.path[1].childNodes[1].innerText)
          } ),
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          success: function (data) {
              alert(JSON.stringify(data['title']));
          }
       })
       event.preventDefault();
}
Controller.requests =  function(event){
    request_objects.requests(event)
    request_objects.count()
}
Controller.likes    =  function(event){
   likes_objects.likes(event)
   likes_objects.count()
}

Controller.message  =  function(event){
   console.log(event);
}
