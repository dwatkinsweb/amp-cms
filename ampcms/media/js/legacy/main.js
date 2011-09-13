require(['jquery', 'page', 'pagelet', 'jquery.ba-bbq', 'amplify.core'], function($, Page, Pagelet) {
	return require.ready(function() {
		var page;
		page = new Page('#page');
		console.log('main subscribing to ampcms.pageletload');
		amplify.subscribe('ampcms.pageletload', function(pagelet) {
			console.log('ampcms.pageletload triggered');
			return pagelet.transform_links().transform_forms();
		});
		console.log('main subscribing to ampcms.pageload');
		amplify.subscribe('ampcms.pageload', function(page) {
			console.log('ampcms.pageload triggered');
			return $(window).trigger('hashchange');
		});
		console.log('main subscribing to hashchange');
		$(window).bind('hashchange', function(event) {
			console.log('hashchange triggered');
			return page.load_pagelets();
		});
		console.log('load pagelets');
		return page.load_pagelets();
	});
});
