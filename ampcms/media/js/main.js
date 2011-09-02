require(['jquery', 'page', 'jquery.ba-bbq', 'amplify.core'], function($, Page) {
	return require.ready(function() {
		var page;
		page = new Page('#page');
		amplify.subscribe('ampcms.pageletload', function(pagelet) {
			return pagelet.transform_links().transform_forms();
		});
		amplify.subscribe('ampcms.pageload', function(page) {
			return $(window).trigger('hashchange');
		});
		$(window).bind('hashchange', function(event) {
			return page.load_pagelets();
		});
		return page.load_pagelets();
	});
});