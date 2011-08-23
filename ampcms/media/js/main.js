require(["jquery", "jquery.page", "jquery.pagelet", "jquery.ba-bbq", "amplify.core"], function($, Page, Pagelet) {
	require.ready(function(){
		// Load the page
		var page = Page().init('#page');
		
		amplify.subscribe('ampcms.pageletload', function(pagelet) {
			pagelet.transform_links().transform_forms();
		});
		amplify.subscribe('ampcms.pageload', function(page) {
			$(window).trigger('hashchange');
		});
		// TODO: Find a way to implement this using ampilfy instead of jquery bind/trigger
		$(window).bind('hashchange', function(event){
			page.load_pagelets();
		});
		page.load_pagelets();
	});
});