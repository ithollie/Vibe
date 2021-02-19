$(document).ready(function() {
	query = document.body.querySelectorAll('#delete');

	$().on('click', function(event) {
		$.ajax({
			data : {
				data_key:"ibrahimthollie"
			},
			type : 'POST',
			url :$SCRIPT_ROOT + "/delete",
			contentType: "application/json; charset=utf-8",
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#alert').text(data.data_key).show();
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

});
