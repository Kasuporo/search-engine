function validate() {
	var seed;

	// Error messages
	var errors = ["Seed requires valid HTTP link"];

	// Regex for a HTTP link
	var re = /^((http|https):\/\/www.)/;

	seed = document.getElementById("seed").value;

	if (re.test(seed) == false) {
		alert(errors[0]);
	}
}



