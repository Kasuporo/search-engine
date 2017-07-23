$(document).ready(function() {
	$(':input[type="submit"]').prop("disabled", true);
	$('#error').hide();

	$('#seed').keyup(function() {
		var seed = $(this).val();

		var re = /((http|https):\/\/www.)/;

		if (!re.test(seed)) {
	   		$('#error').slideDown();
		}

		if (re.test(seed)) {
			$('#error').slideUp();
	   		$('input[type="submit"]').prop("disabled", false);
		}
	});
});
