define(function() {
	return {
		create : function(pagelet, module_selector) {
			pagelet.log('creating sandbox for module ' + module_selector);
			var CONTAINER = pagelet.find('#' + module_selector);
			var sandbox = {
				// Sandbox Methods
				log : function(severity, message) {
					pagelet.log(severity, message);
				},
				push_url : function(url) {
					pagelet.load(url);
				},
				// Event Handling
				publish : function(event) {
					pagelet.publish(event);
				},
				subscribe : function(events) {
					pagelet.subscribe(events, module_selector);
				},
				unsubscribe : function(events) {
					pagelet.unsubscribe(events, module_selector);
				},
				publish_global : function(event) {
					pagelet.publish_global(event);
				},
				subscribe_global : function(events) {
					pagelet.subscribe_global(events, module_selector);
				},
				unsubscribe_global : function(events) {
					pagelet.unsubscribe_global(events, module_selector);
				},
				// Url Handling
				build_url : function(url) {
					return pagelet._build_url(url);
				},
				load_page : function(module, page, pagelets) {
					pagelet.load_page(module, page, pagelets);
				},
				redirect : function(url) {
					pagelet.redirect(url);
				}
			};
			sandbox = pagelet.extend(sandbox, this.extension.create(pagelet, CONTAINER));
			return sandbox;
		},
		extension : {}
	};
});
