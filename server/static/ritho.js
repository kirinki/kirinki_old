$(document).ready(function() {
    $('article').bind('keyup focusout',function(event){
	alert($('article').html());
    });

    $('section').mousedown(function(event){
	if(event.which == 1)
	    $('section').bind('mousemove',$('section').move());
    });

    $('section').mouseup(function(event){	
	if(event.which == 1)
	    $('section').unbind('mousemove',$('section').move());
    });
});

jQuery.fn.move = function() {
    this.addClass('floating');
};
