$(function() {
	$('.next').click(function(e){
		e.preventDefault();
		$('#listing').load(blog_page, next_params, function(){
			console.log('loaded next page');
		});
		// $('.this-page-number').text(this_page + 1);
		// if(this_page + 1 === num_pages){
		// 	$('.next').hide();
		// } else {
		// 	$('.next').show();
		// }
		$.scrollTo({top:'400px', left:'0px'}, 1000);
	});

	$('.previous').click(function(e){
		e.preventDefault();
		$('#listing').load(blog_page, prev_params, function(){
			console.log('loaded previous page');
		});
		//$('.this-page-number').text(this_page);
		// if(this_page  === 1){
		// 	$(this).hide();
		// } else {
		// 	$(this).show();
		// }
		$.scrollTo({top:'400px', left:'0px'}, 1000);
	});

});