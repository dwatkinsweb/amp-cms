define(function() {
	return {
		create : function(core, CONTAINER) {
			return {
				bind : function(element, type, fn) {
					core.dom.bind(element, type, fn);
				},
				unbind : function(element, type, fn) {
					core.dom.unbind(element, type, fn);
				},
		        live : function (element, type, fn) {
		            core.dom.live(element, type, fn);           
		        },
		        die : function (element, type, fn) {
		            core.dom.die(element, type, fn);              
		        },
				// Ajax Handling
				post_form : function(form, callback) {
					core.log('pagelet posting form: ' + form);
					var thiz = this, form_action;
					// Set a default callback to replace the current pagelet with the new html
					if (typeof callback === 'undefined') {
						callback = function(response) {
							core.log(response);
							if (response.location == thiz._get_url()) {
								thiz.unregister_all();
								if(response.css) {
									core.load_css(response.css);
								}
								if(response.js) {
									core.load_js(response.js, function(new_pagelet) {
										thiz._load_html(response.html);
										thiz._transform_links();
										new_pagelet.create(thiz);
										thiz.start_all();
									});
								} else {
									thiz._load_html(response.html);
									thiz._transform_links();
								}
							} else {
								thiz.push_url(response.location);
							}
						};
					}
					form_action = core.dom.attr(form, 'action');
					if(!form_action) {
						form_action = this._get_url();
					}
					form_action = this._build_url(form_action);
					// } else {
						// form_action = '/pagelet' + page_data.url + form_action;
					// }
					return core.ajax.post_form(form, form_action, callback);
				},
		        post : function(url, data, callback) {
		        	core.ajax.post(url, data, callback);
		        },
		        get : function(url, data, callback) {
		        	core.ajax.get(url, data, callback);
		        },
		        ajax : function(url, config) {
		        	core.ajax.ajax(url, config);
		        },
				// Dom Handling
				find : function(selector) {
					return this.__CONTAINER.find(selector);
				},
				filter : function(element, selector) {
					return core.dom.filter(element, selector);
				},
				data : function(selector, key, data) {
					return core.dom.data(selector, key, data);
				},
				remove_data : function(selector, key) {
					core.dom.remove_data(selector, key);
				},
				add_class : function(selector, css) {
					core.dom.add_class(selector, css);
				},
				remove_class : function(selector, css) {
					core.dom.remove_class(selector, css);
				},
				has_class : function(selector, css) {
					return core.dom.has_class(selector, css);
				},
				html : function(selector, html) {
					core.dom.html(selector, html);
				},
				remove : function(selector) {
					core.dom.remove(selector);
				},
				append : function(selector, child) {
					core.dom.append(selector, child);
				},
				// Utilities
				in_array: function(array, value) {
					return core.utils.in_array(array, value);
				}
			};
		}
	};
});
