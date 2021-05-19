/*global L*/
const m = {} //MODEL
const v = {} //VIEW
const c = {} //CONTROLLER
//=======================================//
m.todoList = [{todo: "default 1", completed: false}, {todo: "default 2", completed: false}]

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
  }
  else{m.todoList.forEach( todo => todo.completed = true)}
 
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
  const length = aTodoList.length  
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
    let prefix = aTodoList[i].completed ? "(X)" : "( )"
    console.log(prefix, aTodoList[i].todo)
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

c.addTodo = function (todo) {
  //const todoObject = {todo: todo, completed: false}
  //m.todoList.push(todoObject);
  m.todoList.push({todo: todo, completed: false})
  c.showAndSave()
}

c.deleteTodo = function (position) {
  //convert 'position' to 0-based index
  //by subtracting 1:
  m.todoList.splice(position - 1, 1);
  c.showAndSave();
}

c.changeTodo = function (position, modifiedTodo) {
  //convert 'position' to 0-based index
  //by subtracting 1:
  m.todoList[position - 1].todo = modifiedTodo;
  c.showAndSave();
}

c.showAndSave = function () {
  c.showTodoList();
  const todoListString = JSON.stringify(m.todoList);
  localStorage.setItem(`todoList`, todoListString);
}

c.getServerTodoList = function(){}
c.setLatestTodoList = function(){}


