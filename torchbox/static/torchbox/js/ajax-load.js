$(function() {
	$(document).on('click', '.next', function(e){
		e.preventDefault();
		$('#listing').load(blog_page, next_params, function(){
			$.scrollTo({top:'400px', left:'0px'}, 1000);
		});
	});

	$(document).on('click', '.previous', function(e){
		e.preventDefault();
		$('#listing').load(blog_page, prev_params, function(){
			$.scrollTo({top:'400px', left:'0px'}, 1000);
		});
	});
});