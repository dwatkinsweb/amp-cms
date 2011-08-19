require(["jquery", "jquery.page", "jquery.pagelet", "jquery.ba-bbq.min"], function($, page, pagelet) {
	require.ready(function(){
		// Load the page
		var page_object = page.init('#page');
		$(window).bind('hashchange', function(event){
			page_object.load_pagelets();
		});
		$(document).bind('ampcms.pageletload', function(event, pagelet_object) {
			pagelet_object.transform_links().transform_forms();
		});
		$(document).bind('ampcms.pageload', function(event, page_object) {
			$(window).trigger('hashchange');
		});
		page_object.load_pagelets();
	});
});