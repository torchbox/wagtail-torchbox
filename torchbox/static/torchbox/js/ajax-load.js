$(function() {
	$(document).on('click', '.next', function(e){
		e.preventDefault();
		$.scrollTo($('section.blog'), 1000);
		$('#listing').load(blog_page, next_params, function(){
			
		});
	});

	$(document).on('click', '.previous', function(e){
		e.preventDefault();
		$.scrollTo($('section.blog'), 1000);
		$('#listing').load(blog_page, prev_params, function(){
			
		});
	});
});