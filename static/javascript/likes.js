class Likes{

    length = 0;
    numberofcalls = 0;  

    constructor(Controller, View, Models){
        this.controller = Controller;
        this.view       = View
        this.models     = Models
    }
    count(){
        ++this.numberofcalls; 
        console.log(`Likes is activated and  it  has been  called ${this.numberofcalls} times`)
    }
    activate(){
        console.log(`Likes is activated and  it  has been  called ${this.numberofcalls} times`)
    }

    check(event){
        console.log(event);
        console.log("number" + event.path[1].childNodes[1].innerText);
        console.log("email" +  event.path[2].attributes[2].nodeValue);
        console.log("title" +  event.path[2].attributes[1].nodeValue)
        console.log("_id"  +   event.path[2].attributes[3].nodeValue)

    }
    likes(event){
        this.check(event)
        let y = parseInt(event.path[1].childNodes[1].innerText) + 1;
        event.path[1].childNodes[1].innerText = y;
           
         $.ajax({
               type: "POST",
               url: "/likes",
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
}