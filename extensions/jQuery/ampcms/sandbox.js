define(function() {
	return {
		create : function(pagelet, CONTAINER) {
			return {
				// Event Handling
		        bind : function (element, type, fn) {
		            pagelet.bind(element, type, fn);           
		        },
		        unbind : function (element, type, fn) {
		            pagelet.unbind(element, type, fn);              
		        },
		        live : function (element, type, fn) {
		            pagelet.live(element, type, fn);           
		        },
		        die : function (element, type, fn) {
		            pagelet.die(element, type, fn);              
		        },
		        // Ajax Handling
		        post_form : function (form, callback) {
		        	pagelet.post_form(form, callback);
		        },
		        post : function(url, data, callback) {
		        	pagelet.post(url, data, callback);
		        },
		        get : function(url, data, callback) {
		        	pagelet.get(url, data, callback);
		        },
		        ajax : function(url, config) {
		        	pagelet.ajax(url, config);
		        },
		        // Dom Handling
				find : function(selector) {
					return CONTAINER.find(selector);
				},
				filter : function(element, selector) {
					if (typeof selector == 'string') {
						selector = CONTAINER.find(selector);
					}
					return pagelet.filter(element, selector);
				},
				data : function(selector, key, data) {
					if (typeof selector == 'string') {
						selector = CONTAINER.find(selector);
					}
					return pagelet.data(selector, key, data);
				},
				remove_data : function(selector, key) {
					if (typeof selector == 'string') {
						selector = CONTAINER.find(selector);
					}
					pagelet.remove_data(selector, key);
				},
				add_class : function(selector, css) {
					if (typeof selector == 'string') {
						selector = CONTAINER.find(selector);
					}
					pagelet.add_class(selector, css);
				},
				remove_class : function(selector, css) {
					if (typeof selector == 'string') {
						selector = CONTAINER.find(selector);
					}
					pagelet.remove_class(selector, css);
				},
				has_class : function(selector, css) {
					if (typeof selector == 'string') {
						selector = CONTAINER.find(selector);
					}
					return pagelet.has_class(selector, css);
				},
				html : function(selector, html) {
					if (typeof html === 'undefined') {
						html = selector;
						selector = CONTAINER;
					}
					if (typeof selector == 'string') {
						selector = CONTAINER.find(selector);
					}
					pagelet.html(selector, html);
				},
				remove : function(selector) {
					if (typeof selector == 'string') {
						selector = CONTAINER.find(selector);
					}
					pagelet.remove(selector);
				},
				append : function(selector, child) {
					if (typeof selector == 'string') {
						selector = CONTAINER.find(selector);
					}
					pagelet.append(selector, child);
				},
				// Utilities
				in_array: function(array, value) {
					return pagelet.in_array(array, value);
				}
			};
		}
	};
});