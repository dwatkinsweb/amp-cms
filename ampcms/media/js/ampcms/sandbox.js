define(function() {
	return {
		create : function(paglet, module_selector) {
			var CONTAINER = paglet.find('#' + module_selector);
			return {
				// Sandbox Methods
				find : function(selector) {
					return CONTAINER.find(selector);
				},
				log : function(severity, message) {
					paglet.log(severity, message);
				},
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
		}
	};
});
