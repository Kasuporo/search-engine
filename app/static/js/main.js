function main() {
  $('.form-center').hide();
  $('.form-center').fadeIn(1000);

  $('.content').hide();

  $('.advanced-button').on('click', function() {
	$(this).next().slideToggle(400);
    $(this).toggleClass('active');
	});
}

$(document).ready(main);
