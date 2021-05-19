const  model =  {};//Model
const  View =  {};//view
const  acceptedController =  {};//Controller

acceptedController.initialize  =  function(eventObject){
  
  let acceptedRequestAll  =  document.querySelectorAll("#acceptRequests");
 
 acceptedRequestAll.forEach(elements=>{
     elements.addEventListener('click', acceptedController.acceptedRequests);
 })
 
}

acceptedController.acceptedRequests =  function(event){
    console.log(event);
    console.log("acceptedRequests");
}