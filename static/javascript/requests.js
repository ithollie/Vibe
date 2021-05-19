class Requests{

    length = 0;
    numberofcalls = 0;  

    constructor(Controller, View, Models){
        this.controller = Controller;
        this.view       = View
        this.models     = Models
    }
    count(){
        ++this.numberofcalls; 
        console.log(`requests is activated and  it  has been  called ${this.numberofcalls} times`)
    }
    activate(){
        console.log(`requests is activated and  it  has been  called ${this.numberofcalls} times`)
    }
    
    requests(event){
        console.log(`login name is ${document.getElementById("header").attributes[1].value}`)
        console.log(`login email is ${document.getElementById("header").attributes[2].value}`)
        console.log(`login id  ${document.getElementById("header").attributes[3].value}`)
        console.log(`event data ${event}`)
        $.ajax({
              type: "POST",
              url: "/user_request",
              data: JSON.stringify({
               "login_name":document.getElementById("header").attributes[1].value,
               "user_email":document.getElementById("header").attributes[2].value, 
               "login_id":document.getElementById("header").attributes[3].value,
               
               "post_user":event.path[2].attributes[1].value,
               "post_email":event.path[2].attributes[2].value,
               "post_id":event.path[2].attributes[3].value,
               
               
               "button_state":"clicked",
               "accept":0,
               "count":1
               
              } ),
              contentType: "application/json; charset=utf-8",
              dataType: "json",
              success: function (data) {
                  console.log(data);
                  
              }
           })
           event.preventDefault();

    }
}