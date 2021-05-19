/*global L*/
const m = {} //MODEL
const v = {} //VIEW
const c = {} //CONTROLLER

const  models = {}; // Model
const  views  = {}; //  view
const  cons   = {}; // controller

//=======================================//
m.todoList = []

//==========| INITIALIZATION |=============================//
c.initialize = function(){
  //----| refer all id'ed elements to the view object v |----//
  L.attachAllElementsById(v)
  c.getLocalTodoList();
  
  //----|configure event listners |-----//
  v.btnDelete.onclick = function(eventObject){
    v.numDelete.attribs(`max=${m.todoList.length}`)
    const position = 1 * v.numDelete.value
    if (position > 0){
        c.deleteTodo(position)        
    }
   //----|END of configure event listners |-----//    
  }
  c.showTodoList();
}
//==========| END of INITIALIZATION |======================//
/*
  c.clearCompleted is a method that filters the todoList
  to include only those todos that are not yet completed,
  i.e. it deletes the completed todos.
*/
c.clearCompleted =()=>{
  m.todoList.forEach(clearCompleted)
  //----| helper |------//
  function clearCompleted(todo){
     m.todoList = m.todoList.filter(todo => !todo.completed) 
  }
  //--------------------//
  c.showAndSave()
}



c.showCompleted = (object) => {
  let completedArray = m.todoList.filter(todo => todo.completed)
  console.log(completedArray)
}
c.clearCom = function(){
  c.clearCompleted();
}
c.showActive  = function(){
  let activeArray = m.todoList.filter(activeTodos);
  console.log(activeArray);
  //----|helper|-------//
  function activeTodos(todo){
    return  !todo.completed;

  }
}

c.getLocalTodoList = function(){
    const local = localStorage.getItem(`todoList`);
    if (local) {
      m.todoList = JSON.parse(local);
    }
    v.numDelete.attribs
      (`max=${m.todoList.length}`)
      (`min=1`)
  
    c.showTodoList();    
  }

//-----| Augment the c object with the remaining methods (function properties)
c.toggleAll = function(){
  if( m.todoList.every( todo => todo.completed) ){
    m.todoList.forEach( todo => todo.completed = false)
     c.showAndSave();
  }
  else{m.todoList.forEach( todo => todo.completed = true)
     c.showAndSave();
  }
 
}

c.toggleAll2 = function(){
  let completedCount = 0
  const maxCount = m.todoList.length
  // Count the completed todos
  for(let i = 0; i < maxCount; i++){
    if(m.todoList[i].completed){completedCount++}
  }
  //Now toggle all, based on the result
  if(completedCount === maxCount){
    for(let i = 0; i < maxCount; i++){m.todoList[i].completed = false}
  }
  else{
    for(let i = 0; i < maxCount; i++){m.todoList[i].completed = true}    
  }
  c.showAndSave()  
}

c.toggleAll3 = function(){
  //---| helper function |------//
  function todoIsCompleted(todo){
    return todo.completed
  }
  
  if( m.todoList.every(todoIsCompleted) ){
    m.todoList.forEach(function(todo){
      todo.completed = false
    })    
  }
  else{
    m.todoList.forEach(todo => todo.completed = true)
  }
  c.showAndSave()  
}

c.showTodoList = function (aTodoList = m.todoList) {
  const length = aTodoList.length;
  v.numDelete.attribs
    (`max=${length}`)
    (`min=1`)
  v.numDelete.value=`` 
  
  for (let i = 0; i < length; i++){
    /*
      1.make a proper prefix: 
        a. if completed = false => ( )
        b. if completed = true =>  (X)
      2. Show the prefix and the corresponding todo string  
    */
    
    let prefix = aTodoList[i].completed ? "(Cpmpleted)" : "(not yet completed)"
    console.log(prefix, aTodoList[i].todo)
    const undolist = document.getElementById("todoslist");
    const does    =  document.getElementById("Ger");
    does.innerHTML = aTodoList[i];
    
  }
    /*
      1. Count our uncompleted tasks, and ...
      2. Show number of items left to do
    */
    let count = 0;
    aTodoList.forEach(function(todo){
      if(todo.completed === false){
        count++
      }
    })
    const itemOrItems = (count === 1) ? "item" : "items"
    console.log(`${count} ${itemOrItems} left to complete`)  
}

c.toggleCompleted = function(position){
  m.todoList[position - 1].completed =  ! m.todoList[position - 1].completed 
  c.showAndSave()
}
c.remove = function(){
  
}
c.addTodo = function (name, todo) {
  //const todoObject = {todo: todo, completed: false}
  //m.todoList.push(todoObject);
  if(m.todoList.name != name){
    m.todoList.push({todo: todo,name:name, completed: false})
  }else{
    console.log("please  enter a  name and  a description")
  }
  c.showAndSave()
}
//delete  a to do
c.deleteTodo = function (name) {
  const amount = m.todoList.length;
  const stops  = [];
  
  for(let i = 0; i < amount; i++){
    if(m.todoList.length === 1){
      if(m.todoList[i].name === name){
        stops.push({position:i, name:m.todoList[i].name});
        m.todoList.splice(i, 1);
  	    console.log(i);
  	    console.log(stops[0]);
      }
    }else{
  	  if (m.todoList[i].name === name){ 
  	    m.todoList.splice(i -1, 1);
  	    console.log(i);
  	  }
    }
  }
  c.showAndSave();
}

c.changeTodo = function (name,  description) {
  for(let i = 0 ; i < m.todoList.length; i++){
    if(m.todoList[i].name === name){
        m.todoList[i].todo = description;
    }
  }
  c.showAndSave();
}

c.showAndSave = function () {
  c.showTodoList();
  const todoListString = JSON.stringify(m.todoList);
  localStorage.setItem(`todoList`, todoListString);
}

cons.changeTodoEvent =  function(){
  const btnChange = document.getElementById("btnChange");
  const changeName    = document.getElementById("change").value;
  const description   = document.getElementById("description").value;
  for(let i  = 0;  i < m.todoList.length; i++){
      if(m.todoList[i].name === changeName){
          c.changeTodo(m.todoList[i].name,description);
      }
  }
  document.getElementById("change").value = '';
  document.getElementById("description").value ='';
}
cons.changeBooleanTrue = function(name){
  const counts = 0;
  const array  = new Array()
  if(m.todoList.length < 0){
    for(let i = 0; i < m.todoList.length; i++){
      if(m.todolist[i] === "true"){
        m.todolist[i].pop();
      }
    }
  }
}
cons.deleteEvent = function(){
  const close = document.getElementsByClassName("close");
  const btnDelete = document.getElementById("btnDelete");
  const deleteInputName =  document.getElementById("deleteInput").value;
  const li    = document.querySelectorAll("LI");
  
  if (deleteInputName  === '') {
    alert("You must write a todo name!");
  }else{
    c.deleteTodo(deleteInputName)
  }
  document.getElementById("deleteInput").value = "";
  console.log("delete" + deleteInputName);
  c.showAndSave();
}
cons.delte = function(deleteInputName){
   for(let i = 0; i < m.todoList.length; i++){
  	  if (m.todoList[i].name === deleteInputName){ 
  	      if(m.todoList.length === 1){
            if(m.todoList[i].name === deleteInputName){
              m.todoList.splice(i, 1);
        	    console.log(i);
            }
          }else{
        	  if(m.todoList[i].name === deleteInputName){ 
        	    m.todoList.splice(i -1, 1);
        	    console.log(i);
        	  }
        }
      }
 
  	}
      
}
//create  close  botton and append each one
cons.createClose  = function(){
  const  myNodelist = document.getElementsByTagName("LI");
  for (let i = 0; i < myNodelist.length; i++) {
    const  span = document.createElement("SPAN");
    const  txt = document.createTextNode("\u00D7");
    span.className = "close";
    span.appendChild(txt);
    myNodelist[i].appendChild(span);
  }
}
// close if click
cons.closeLi =  function(){
  const  close = document.getElementsByClassName("close");
  for (let i = 0; i < close.length; i++) {
    close[i].onclick = function() {
      const div = this.parentElement;
      div.style.display = "none";
    }
  }
}
// Add a "checked" symbol when clicking on a list item
cons.addCheck =function(){
  const  list = document.querySelector('ul');
  list.addEventListener('click', function(ev) {
    if (ev.target.tagName === 'LI') {
      ev.target.classList.toggle('checked');
      cons.logic( ev.target.attributes["data-key"].nodeValue,ev.target.attributes["data-boolean"].nodeValue );
    }
  });
}
cons.uncheck =  function(){
  const list =  document.querySelector('ul');
  list.addEventListener('click' , function(ev){
    if(ev.target.tagName === 'LI'){
      cons.logic( ev.target.attributes["data-key"].nodeValue,ev.target.attributes["data-boolean"].nodeValue );
    }
  })
}
cons.logic = function(value,boolean){
  for(let i = 0 ; i< m.todoList.length; i++){
    if(m.todoList[i].name === value){
      if(m.todoList[i].completed === false){
          m.todoList[i].completed = true
        }else{
          if(m.todoList[i].completed === true){
             m.todoList[i].completed = false
          }
        }
      }
    }
}

// Create a new list item when clicking on the "Add" button
cons.newElement =function newElement(){
  const data_boolean = "true";
  const  close = document.getElementsByClassName("close");
  const li = document.createElement("li");
  const  todoName   = document.getElementById("todoName").value;
  const  inputValue = document.getElementById("myInput").value;
  const  t = document.createTextNode(inputValue);
  li.appendChild(t);
  li.setAttribute("data-key", todoName);
  li.setAttribute("data-boolean",data_boolean)
  if (todoName  === '') {
    alert("You must write a todo name!");
  }if(inputValue === '') {
    alert("You must  write a todo description");
  }else{
    document.getElementById("myUL").appendChild(li);
    c.addTodo(inputValue,todoName);
    console.log(inputValue);
  }
  document.getElementById("myInput").value = "";
  document.getElementById("todoName").value = "";

  var span = document.createElement("SPAN");
  var txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  li.appendChild(span);
  cons.remove(close, todoName);
}
cons.remove  = function(close, todoName){
  for (let i = 0; i < close.length; i++) {
    close[i].onclick = function(eventObject) {
      var div = this.parentElement;
      div.style.display = "none";
      c.deleteTodo(todoName);
    }
  }
  
}
c.getServerTodoList = function(){}
c.setLatestTodoList = function(){}
cons.createClose();
cons.closeLi();
cons.addCheck();
//cons.changeTodoEvent();
//cons.deleteEvent();
//cons.addTodoevent();

