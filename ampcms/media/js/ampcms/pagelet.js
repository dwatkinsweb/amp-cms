define(['ampcms/sandbox'], function(sandbox) {
	var module_data = {};

	return {
		create : function(core, pagelet_selector) {
			var CONTAINER = core.dom.find('#' + pagelet_selector);
			pagelet = {
				log : function(severity, message) {
					core.log(severity, message);
				},
				// Module Handling Methods
				register_module : function(module_id, creator) {
					core.log(1, 'registering module ' + module_id);
					var temp;
					if( typeof module_id === 'string' && typeof creator === 'function') {
						temp = creator(sandbox.create(this, module_id));
						if(temp.init && typeof temp.init === 'function' && temp.destroy && typeof temp.destroy === 'function') {
							temp = null;
							module_data[module_id] = {
								create : creator,
								instance : null
							};
						} else {
							core.log(2, "Module '" + module_id + "' Registration : FAILED : instance has no init or destory functions");
						}
					} else {
						core.log(2, "Module '" + module_id + "' Registration : FAILED : one or more arguments are of incorrect type");
					}
				},
				unregister_module : function(module_id) {
					core.log(1, 'unregistering module ' + module_id);
					this.stop(module_id);
					delete module_data[module_id];
				},
				unregister_all : function() {
					var module_id;
					for(module_id in module_data) {
						if(module_data.hasOwnProperty(module_id)) {
							this.unregister_module(module_id);
						}
					}
				},
				start : function(module_id) {
					core.log(1, 'starting module ' + module_id);
					var mod = module_data[module_id];
					if(mod) {
						mod.instance = mod.create(sandbox.create(this, module_id));
						mod.instance.init();
					}
				},
				start_all : function() {
					var module_id;
					for(module_id in module_data) {
						if(module_data.hasOwnProperty(module_id)) {
							this.start(module_id);
						}
					}
				},
				stop : function(module_id) {
					core.log(1, 'stopping module ' + module_id);
					var data = module_data[module_id];
					if(data && data.instance) {
						data.instance.destroy();
						data.instance = null;
					} else {
						core.log(2, "Stop Module '" + module_id + "': FAILED : module does not exist or has not been started");
					}
				},
				stop_all : function() {
					var module_id;
					for(module_id in module_data) {
						if(module_data.hasOwnProperty(module_id)) {
							this.stop(module_id);
						}
					}
				},
				// Pagelet Methods
				load : function(url) {
					var data = core.dom.data(CONTAINER), thiz = this;
					if(url == null) {
						url = this._get_url();
					}
					core.log(1, 'pagelet loading with url: ' + url)
					if(url != null) {
						url = this._build_url(url);
						core.log(1, 'loading url: ' + url);
						if(url != null && url !== data.location) {
							core.ajax.get(url, function(response) {
								core.log(1, response);
								thiz.unregister_all();
								if (response.css.length > 0) {
									core.load_css(response.css);
								}
								if (response.js.length > 0) {
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
							});
						}
					}
				},
				push_url : function(url) {
					return core.history.push_state(pagelet_selector, url);
				},
				_get_url : function() {
					var url, data;
					url = core.history.get_state(pagelet_selector);
					if(url == null) {
						data = core.dom.data(CONTAINER);
						if(data != null && data.starting_url) {
							url = data.starting_url;
						}
					}
					return url;
				},
				_build_url : function(url) {
					var data = core.dom.data(CONTAINER), page_data = core.dom.data(core.page);
					if(data && page_data) {
						return '/pagelet' + page_data.url + '/' + data.name + url;
					} else {
						core.log(2, 'page or pagelet missing data');
					}
				},
				_load_html : function(html) {
					core.dom.replace(CONTAINER, html);
					CONTAINER = core.dom.find('#' + pagelet_selector);
				},
				_transform_links : function() {
					var thiz = this, anchor, anchors, href, _i, _len;
					anchors = CONTAINER.find('a');
					for( _i = 0, _len = anchors.length; _i < _len; _i++) {
						anchor = anchors[_i];
						href = core.dom.attr(anchor, 'href');
						href = href.replace(/^.*\.com/, '');
						core.dom.attr(anchor, 'href', '#' + href);
					}
					core.dom.bind(anchors, 'click', function(event) {
						var target, url;
						target = core.dom.find(event.target);
						url = core.dom.attr(target, 'href').split('#')[1];
						thiz.push_url(url);
						return false;
					});
				},
				// Event Handling Methods
				publish : function(event) {
					for(module in module_data) {
						if(module_data.hasOwnProperty(module)) {
							module = module_data[module];
							if(module.events && module.events[event.type]) {
								module.events[event.type](event.data);
							}
						}
					}
				},
				subscribe : function(events, module) {
					if(core.utils.is_object(events) && module) {
						if(module_data[module]) {
							module = module_data[module]
							if(module.events) {
								module.events = core.utils.extend(module.events, events);
							} else {
								module.events = events;
							}
						} else {
							core.log(2, "Events subscribed by non existant module: " + module);
						}
					} else {
						core.log(2, "Invalid parameters sent to event subscription: events: " + events + "; module: " + module);
					}
				},
				unsubscribe : function(events, module) {
					if(core.utils.is_object(events) && module) {
						if(module_data[module]) {
							module = module_data[module]
							if(module.events) {
								module.events = core.utils.retract(module.events, events);
							}
						} else {
							core.log(2, "Events unsubscribed by non existant module: " + module);
						}
					} else {
						core.log(2, "Invalid parameters sent to event unsubscription: events: " + events + "; module: " + module);
					}
				},
				publish_global : function(event) {
					core.events.publish(event);
				},
				subscribe_global : function(events, module) {
					if(module_data[module]) {
						core.events.subscribe(events, pagelet_selector, module);
					} else {
						core.log(2, "Events globally subscribed by non existant module: " + module);
					}
				},
				unsubscribe_global : function(events, module) {
					if(module_data[module]) {
						core.events.unsubscribe(events, pagelet_selector, module);
					} else {
						core.log(2, "Events globally subscribed by non existant module: " + module);
					}
				},
				bind : function(element, type, fn) {
					core.dom.bind(element, type, fn);
				},
				unbind : function(element, type, fn) {
					core.dom.unbind(element, type, fn);
				},
				// Ajax Handling
				post_form : function(form, callback) {
					core.log(1, 'pagelet posting form: ' + form);
					var thiz = this, form_action;
					// Set a default callback to replace the current pagelet with the new html
					if (typeof callback === 'undefined') {
						callback = function(response) {
							core.log(1, response);
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
						form_action = this._build_url(this._get_url());
					} else {
						form_action = '/pagelet' + this.page.data.url + form_action;
					}
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
					return CONTAINER.find(selector);
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
			pagelet.load();
			return pagelet;
		}
	};
});
