function optsSmall() {
	var ret = {
	  lines: 13, // The number of lines to draw
	  length: 4, // The length of each line
	  width: 2, // The line thickness
	  radius: 4, // The radius of the inner circle
	  // length: 20, // The length of each line
	  //width: 10, // The line thickness
	  //radius: 30, // The radius of the inner circle
	  corners: 1, // Corner roundness (0..1)
	  rotate: 0, // The rotation offset
	  direction: 1, // 1: clockwise, -1: counterclockwise
	  color: '#000', // #rgb or #rrggbb or array of colors
	  speed: 1, // Rounds per second
	  trail: 60, // Afterglow percentage
	  shadow: false, // Whether to render a shadow
	  hwaccel: false, // Whether to use hardware acceleration
	  className: 'spinner', // The CSS class to assign to the spinner
	  zIndex: 2e9, // The z-index (defaults to 2000000000)
	  top: 'auto', // Top position relative to parent in px
	  left: 'auto' // Left position relative to parent in px
	};
	return ret;
}

function optsBig() {
	var ret = {
	  lines: 13, // The number of lines to draw
	  length: 6, // The length of each line
	  width: 3, // The line thickness
	  radius: 8, // The radius of the inner circle
	  // length: 20, // The length of each line
	  //width: 10, // The line thickness
	  //radius: 30, // The radius of the inner circle
	  corners: 1, // Corner roundness (0..1)
	  rotate: 0, // The rotation offset
	  direction: 1, // 1: clockwise, -1: counterclockwise
	  color: '#000', // #rgb or #rrggbb or array of colors
	  speed: 1, // Rounds per second
	  trail: 60, // Afterglow percentage
	  shadow: false, // Whether to render a shadow
	  hwaccel: false, // Whether to use hardware acceleration
	  className: 'spinner', // The CSS class to assign to the spinner
	  zIndex: 2e9, // The z-index (defaults to 2000000000)
	  top: 'auto', // Top position relative to parent in px
	  left: 'auto' // Left position relative to parent in px
	};
	return ret;
}

function showSpinner(event) {
	$('.progress-container').empty()
	var size = event.data['size'];
	var opts;
	if (size == "small") {
		opts = window.optsSmall();
	} else if (size == "big") {
		opts = window.optsBig();
	}
	var form = $(event.target).parent();
	var container = form.find('.progress-container')
	container.css('opacity', '1.0');
	var spinner = new Spinner(opts).spin(container[0]);
}

window.onload = function() {
	$('.table-action').find('input[type="submit"]').click(
		{ 'size' : 'small' }, showSpinner
	);
	$('.form-user-input').find('input[type="submit"]').click(
		{ 'size' : 'big' }, showSpinner
	);
};