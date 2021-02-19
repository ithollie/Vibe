/*
  Author:  Abbas Abdulmalik
  Created: ~ May, 2017
  Revised: January 26, 2018 
  Original Filename: L.js 
  Purpose: a small personal re-usable js library for a simple MVC architecture
  Notes: Now qualifyFunction helper doesn't return true for empty arrays (no vacuous truth)
         UploadFiles added.
         uploadFiles takes a callback -- progressReporter-- as it FIRST argument (parameter)
         to allow for an optional fourth parameter of an upload path for the server.
         progressReporter will be passed three arguments when called:
         1.) the amount of bytes uploaded so far
         2.) the total size of the file in bytes
         3.) the index of the file in the "array" of files being uploaded
         
      Added sortByExtension that alphabetizes an array of strings 'in place' by filename extension          
      Added arrayStringMatch that matches a collection of string arrays to a search string.
      Added attribs method to elements as alternative to attributes method as a shortened form.
*/

var L = {}
L.styles = function(styleString){
  const colonPosition = styleString.indexOf(':')
  const property = styleString.slice(0, colonPosition)
  const value = styleString.slice(colonPosition + 1)
  this.style[property] = value
  
  return this.styles  
}

L.attributes = function(attributeString){
  const assignmentPosition = attributeString.indexOf('=')
  const attribute = attributeString.slice(0, assignmentPosition)
  const value = attributeString.slice(assignmentPosition + 1)
  this.setAttribute(attribute, value)
  
  return this.attributes
}

L.attribs = function(attributeString){
  const assignmentPosition = attributeString.indexOf('=')
  const attribute = attributeString.slice(0, assignmentPosition)
  const value = attributeString.slice(assignmentPosition + 1)
  this.setAttribute(attribute, value)
  
  return this.attribs
}

L.attachAllElementsById = function(here){
  let allElements = document.getElementsByTagName('*')
  let array = []
  array.forEach.call(allElements, function(element)  {
      if(element.id){
          here[element.id] = element
          element.styles = L.styles.bind(element) // attach L's styles() method here
          element.attributes = L.attributes.bind(element) // attach L's attributes() method here
          element.attribs = L.attribs.bind(element) // attach L's attribs() method here          
      }
  })
}

L.noPinchZoom = function(){
  window.ontouchstart = function(eventObject){
    if(eventObject.touches && eventObject.touches.length > 1){
      eventObject.preventDefault();
    }
  }  
}

L.runQualifiedMethods = function(functionQualifiers, object, runNextUpdate){
  Object
    .keys(functionQualifiers)
    .filter(qualifyFunction)
    .forEach(runFunction)
  if(typeof runNextUpdate === 'function'){runNextUpdate()}
  
  //-----| helpers |-----//
  function qualifyFunction(functionName){
    const isQualified = functionQualifiers[functionName].every( qualifier => qualifier) &&
                        !!functionQualifiers[functionName].length
    return isQualified
  }
  function runFunction(functionName){
    if(typeof object[functionName] === 'function'){
      object[functionName]()        
    }
   
    /*
      If the prefix of this function's name is 'set' (for updating the MODEL),
      and there is a similarly named function with a prefix of 'show' (for updating the VIEW),
      then run the 'show' version as well.
    */
    let prefix = functionName.slice(0,3)
    let newFunctionName = 'show' + functionName.slice(3)
    
    if(prefix === 'set' && typeof object[newFunctionName] === 'function'){
      object[newFunctionName]()
    }
  }
}

/**
  Use a php script to read contents of file from $_POST['contents'] that was converted by client
  as DataURL, and expects filename and uploadPath from: $_POST['filename'] and $_POST['uploadPath']
  with trailing slash (/) provided by client (though script could check for this).
  
  doneCounter is used to signal sending (1,1,index) to progressReporter to show:
    a. that all files have been uploaded
    b. which file (by the index number) was the last to upload completely
*/
L.uploadFiles = function(progressReporter, fileElement, phpScriptName, uploadPath='../uploads/'){
  let doneCounter = 0
  let fileCount = fileElement.files.length
  const array = [] // make a real array to borrow it's forEach method using 'call'
  array.forEach.call(fileElement.files, (file, index) => {
    const postman = new XMLHttpRequest() // make a file deliverer for each file
    const uploadObject = postman.upload // This object keeps track of upload progress
    const envelope = new FormData() // make a holder for the file's name and content
    envelope.stuff = envelope.append // give 'append' the nickname 'stuff'
    const reader = new FileReader() // make a file reader (the raw file element is useless)
    
    reader.readAsDataURL(file) // process the file's contents
    reader.onload = function(){ // when done ...
      const contents = reader.result // collect the result, and ...
      envelope.stuff('contents', contents) // place it in the envelope along with ...
      envelope.stuff('filename', file.name) // its filename
      envelope.stuff('uploadPath', uploadPath) // its upload path on the server
      
      postman.open(`POST`, phpScriptName)// open up a POST to the server's php script
      postman.send(envelope) // send the file
      
      //check when file loads and when there is an error
      postman.onload = eventObject => {
        postman.status !== 200 ? showMessage() : checkLastFileDone()
        //-----| helpers |------//
        function showMessage(){
          const message = `Trouble with file: ${postman.status}`
          console.log(message)
          alert(message)
        }
        
        function checkLastFileDone(){
          doneCounter++          
          if(typeof progressReporter === 'function'){
            if(doneCounter === fileCount){
              progressReporter(1, 1, index)              
            }
          }          
        }
      }
      
      postman.onerror = eventObject => {
        const message = `Trouble connecting to server`
        console.log(message)
        alert(message)
      }
      
      //invoke the callback for each upload progress report
      uploadObject.onprogress = function(progressObject){
        if(typeof progressReporter === 'function'){
          progressReporter(progressObject.loaded, progressObject.total, index)
        }
      }
    }
  })
}

//---------------------------------------------------------//
/**
  Given an array of strings (array), sorts the array 'in place' by filename EXTENSION,
  and returns a copy of the array as well. Since it mutates the array, it is decidedly not
  functionistic (but it functions).
*/
L.sortByExtension = function (array) {
  //two 'bouncers':
  //1. 'array' must be an actual array
  const type = {}.toString.call(array, null);
  if (type !== '[object Array]') {
    return array;
  }
  //2. 'array' must not be empty, and must contain only strings
  if (array.length === 0 || array.some(member => typeof member !== 'string')) {
    return array;
  }
  //-------------------------------------//
  let extension = ``;
  let nudeWord = ``;  
  array.forEach((m, i, a) => {
    if (m.lastIndexOf(`.`) !== -1) {
      //get the extension
      extension = m.slice(m.lastIndexOf(`.`) + 1);
      nudeWord = m.slice(0, m.lastIndexOf(`.`));
      a[i] = `${extension}.${nudeWord}`;
    }
  });
  
  array.sort();
  
  array.forEach((m, i, a) => {
    if (m.indexOf(`.`) !== -1){
      //get prefix (formerly the extension)
      extension = m.slice(0, m.indexOf(`.`))
      nudeWord = m.slice(m.indexOf(`.`) + 1)
      a[i] = `${nudeWord}.${extension}`
    }
  });
  
  const newArray = []
  array.forEach( m => newArray.push(m))
  
  return newArray;
}
//----------------------------------------------//


/*
From an array of string arrays, return a possibly smaller array
of only those string arrays whose member strings contain the given subString
regardless of case.
   1. For arrayOfStringArrays, use the filter method (a function property of an array)
   that expects a function argument that operates on each array member
   2. Let's call the function argument 'match'
   3. 'match' should test each member array for a match of the substring as follows:
    a.) join the members strings together into a bigString that is lowerCased
    b.) lowerCase the subString
    c.) use indexOf to match substring to the bigString
    d.) return true for a match, otherwise return false
   4. the filter creates a new array after doing this.
   5. final step: return the new array that the filter produced 
*/
L.arrayStringMatch = function(subString, arrayOfStringArrays){
  return arrayOfStringArrays.filter(match)
  //-------| Helper function 'match' |---------//
  function match(memberArray){
    const bigString = memberArray.join(``).toLowerCase()
    const substringToMatch = subString.toLowerCase()
    return bigString.indexOf(substringToMatch) !== -1   
  }
}
