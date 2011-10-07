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
				}
			};
			sandbox = pagelet.extend(sandbox, this.extension.create(pagelet, CONTAINER));
			return sandbox;
		},
		extension : {}
	};
});
