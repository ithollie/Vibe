// /*
//   1. make a method that toggles all completed properties to be true or false
//   If(all completeds are true){make them all false}
//   else(make them all true)
const model = {};
const view  = {};
const controller = {};

const todos = {
  todoList: [{todo: "default 1", completed: false}, {todo: "default 2", completed: false}],
  getLocalTodoList: function(){
    const local = localStorage.getItem(`todoList`);
    if (local) {
      todos.todoList = JSON.parse(local);
    }
  }
}
//alais todos
const  t = todos;
// loop
controller.change =  function(){
  var modal = document.getElementById('myModal');
  var btn = document.getElementById("myBtn");
  var span = document.getElementsByClassName("close")[0];
  var change = document.getElementById("change");
  var wrapperu = document.getElementById("wrapperu");
  var ge       = document.getElementById("g");

  const c =  document.getElementById("f").children[0].children;
  for(let  i = 0 ;  i < c.length; i++){
    c[i].addEventListener(`mouseenter`, function(eventObject){
      const  v = eventObject.target.attributes.nodeValue;
        console.log(change);
        // wrapperu.style.height = "50%";
        // change.style.visibility = "visible";
        // change.style.height     = "60%";
        // ge.style.height = "60%";

    })
  }
}

controller.changes =  function(){
  var modal = document.getElementById('myModal');
  var btn = document.getElementById("myBtn");
  var span = document.getElementsByClassName("close")[0];
  var change = document.getElementById("change");
  var wrapperu = document.getElementById("wrapperu");
  var ge       = document.getElementById("g");

  const c =  document.getElementById("f").children[0].children;
  for(let  i = 0 ;  i < c.length; i++){
    c[i].addEventListener(`mouseleave`, function(eventObject){
      const  v = eventObject.target.attributes.nodeValue;
        console.log(change);
        wrapperu.style.height = "30%";
        change.style.visibility = "hidden";
        change.style.height     = "1%";
        ge.style.height = "100%";

    })
  }
}
todos.all =  function(){
  window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
}
todos.open = function(){
  var modal = document.getElementById('myModal');
  modal.style.display = "block";
}
todos.closem = function(){
    var span = document.getElementsByClassName("close")[0];
    var modal = document.getElementById('myModal');
    span.addEventListener(`click`, function(eventObject){
      modal.style.display = "none";
    })
}
//-----| Augment the todos object with the remaining methods (function properties)
todos.toggleAll = function(){
  if( this.todoList.every( todo => todo.completed) ){
    this.todoList.forEach( todo => todo.completed = false)
  }
  else{this.todoList.forEach( todo => todo.completed = true)}
  this.showAndSave()
}

todos.toggleAll2 = function(){
  let completedCount = 0;
  const  maxCount =  todos.todoList.length;
  for(let i=0; i < maxCount; i++){
    if(todos.todoList[i].completed){
      completedCount++;
    }
  }
  if(completedCount === maxCount){
      for(let i = 0; i < maxCount; i++){
        todos.todoList[i].completed = false;
      }
  }else{
    for(let i = 0; i < maxCount; i++){
        todos.todoList[i].completed = true;
      }
  }
  this.showAndSave();
}
todos.toggleAll3 =  function(){
  function todosIsCompleted(todo){
    return todo.completed;
  }
  if(todos.todoList.every(todoIsCompleted)){
      todo.todolist.forEach(function(todo){
      todo.completed = false

    })
  }else{
    todos.toList.forEach(todo => todo.completed = true)
  }
}

todos.showtodoList = function () {
  for (let i = 0; i < this.todoList.length; i++){
    /*
      1.make a proper prefix:
        a. if completed = false => ( )
        b. if completed = true =>  (X)
      2. Show the prefix and the corresponding todo string
    */
    let prefix = this.todoList[i].completed ? "(X)" : "( )"
    console.log(prefix, this.todoList[i].todo)
  }
    /*
      1. Count our uncompleted tasks, and ...
      2. Show number of items left to do
    */
    let count = 0;
    this.todoList.forEach(function(todo){
      if(todo.completed === false){
        count++
      }
    })
    const itemOrItems = (count === 1) ? "item" : "items"
    console.log(`${count} ${itemOrItems} left to complete`)
}

todos.toggleCompleted = function(position){
  this.todoList[position - 1].completed =  ! this.todoList[position - 1].completed
  this.showAndSave()
}

todos.addTodo = function (todo) {
  //const todoObject = {todo: todo, completed: false}
  //this.todoList.push(todoObject);
  this.todoList.push({todo: todo, completed: false})
  this.showAndSave()
}

todos.deleteTodo = function (position) {
  //convert 'position' to 0-based index
  //by subtracting 1:
  this.todoList.splice(position - 1, 1);
  this.showAndSave();
}

todos.changeTodo = function (position, modifiedTodo) {
  //convert 'position' to 0-based index
  //by subtracting 1:
  this.todoList[position - 1].todo = modifiedTodo;
  this.showAndSave();
}

todos.showAndSave = function () {
  this.showtodoList();
  const todoListString = JSON.stringify(this.todoList);
  localStorage.setItem(`todoList`, todoListString);
}


todos.getServerTodoList = function(){}
todos.setLatestTodoList = function(){}


//--------| initialization |---------//
todos.getLocalTodoList();//initialize the todoList array
controller.change();
controller.changes();
