/*
* Copyright David Watkins 2011
* 
* AMP-CMS is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
* 
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

define(['ampcms/sandbox'], function(sandbox) {
	var module_data = {};

	return {
		create : function(core, pagelet_selector) {
			var CONTAINER = core.dom.find('#' + pagelet_selector);
			var pagelet = {
				__CONTAINER : CONTAINER,
				events : {},
				log : function(severity, message) {
					core.log(severity, message);
				},
				// Module Handling Methods
				register_module : function(module_id, creator) {
					core.log('registering module ' + module_id);
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
					core.log('unregistering module ' + module_id);
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
					core.log('starting module ' + module_id);
					var mod = module_data[module_id], mod_sandbox;
					if(mod) {
						mod_sandbox = sandbox.create(this, module_id);
						mod.instance = mod.create(mod_sandbox);
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
					core.log('stopping module ' + module_id);
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
							module = module_data[module];
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
							module = module_data[module];
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
				load_page : function(module, page, pagelets) {
					core.load_page(module, page, pagelets);
				},
				redirect : function(url) {
					core.redirect(url);
				},
				// Pagelet Methods
				load_response : function(response) {
					var thiz = this
					core.log(response);
					this.unregister_all();
					if (typeof response.redirect !== 'undefined' && response.redirect) {
						core.redirect(response.location);
					}
					if (response.css.length > 0) {
						core.load_css(response.css);
					}
					if (response.js.length > 0) {
						core.load_js(response.js, function() {
							var _i, _len, new_pagelet;
							thiz._load_html(response.html);
							thiz._transform_links();
							for (_i = 0, _len = arguments.length; _i < _len; _i++) {
								new_pagelet = arguments[_i];
								if (new_pagelet != null && typeof new_pagelet === 'object' && new_pagelet.hasOwnProperty('create')) {
									new_pagelet.create(thiz);
								}
							}
							thiz.start_all();
							thiz.replace_state(response.location);
						});
					} else {
						this._load_html(response.html);
						this._transform_links();
						thiz.replace_state(response.location);
					}
				},
				load : function(url) {
					var data, thiz = this, new_url;
					if(url == null) {
						url = this._get_url();
					}
					core.log('pagelet loading with url: ' + url)
					if(url != null && typeof url !== 'undefined') {
						core.log('loading url: ' + url);
						new_url = this._build_url(url);
						data = core.dom.data(CONTAINER);
						if(new_url != null && url !== data.location) {
							core.dom.trigger(CONTAINER, 'ampcms.pagelet.loadstart');
							core.ajax.get(new_url, function(response) {
								core.dom.trigger(CONTAINER, 'ampcms.pagelet.loadajaxcomplete');
								thiz.load_response(response);
								core.dom.trigger(CONTAINER, 'ampcms.pagelet.loadfullcomplete');
							});
						}
					}
				},
				push_state : function(url) {
					core.log('Pushing state : '+pagelet_selector+'-'+url);
					return core.history.push_state(pagelet_selector, url);
				},
				replace_state : function(url) {
					return core.history.replace_state(pagelet_selector, url);
				},
				get_state : function() {
					return core.history.get_state(pagelet_selector)
				},
				push_url : function(url) {
					// TODO: Remove this function and replace with push_state
					this.log(2, 'pagelet.push_url is deprecated');
					return this.push_state(url);
				},
				_get_url : function() {
					var url, data;
					url = this.get_state();
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
					CONTAINER = this.__CONTAINER = core.dom.find('#' + pagelet_selector);
				},
				_transform_links : function(container_element) {
					if (typeof container_element === 'undefined') {
						container_element = CONTAINER;
					}
					var thiz = this, anchor, anchors, transformed_anchors, href, _i, _len;
					anchors = container_element.find('a[target!=_blank][data-ampcms-transform!=ignore]');
					transformed_anchors = [];
					for( _i = 0, _len = anchors.length; _i < _len; _i++) {
						anchor = anchors[_i];
						href = core.dom.attr(anchor, 'href');
						if (typeof href !== 'undefined') {
							href = href.replace(/^.*\.com/, '');
							if (href[0] != '#') {
								core.dom.attr(anchor, 'href', '#' + href);
							}
							transformed_anchors.push(anchor);
						}
					}
					core.dom.bind(transformed_anchors, 'click', function(event) {
						var target, url;
						target = core.dom.find(event.target);
						url = core.dom.attr(target, 'href').split('#')[1];
						thiz.push_state(url);
						return false;
					});
				},
				// Other Functions
				extend : function(target, source) {
					return core.extend(target, source);
				}
			};
			pagelet = core.extend(pagelet, this.extension.create(core, CONTAINER));
			pagelet.load();
			return pagelet;
		},
		extension : {}
	};
});
