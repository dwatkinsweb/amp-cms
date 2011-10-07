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
					pagelet.push_url(url);
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
			};
			sandbox = pagelet.extend(sandbox, this.extension.create(pagelet, CONTAINER));
			return sandbox;
		},
		extension : {}
	};
});
