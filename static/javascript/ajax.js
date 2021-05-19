const  ms =  {};//Model
const  vs =  {};//view
const  cs =  {};//Controller

cs.initialize  =  function(eventObject){

 $(document).ready(function() {
     $('but').click(function(event) {
       $.ajax({
          data: $('form').serialize(),
          url : '',
          type : 'POST',
          success: function(response){
				console.log(response);
				
			},
			error: function(error){
				console.log(error);
			}
          
        })
    
      event.preventDefault();
      });
});
}