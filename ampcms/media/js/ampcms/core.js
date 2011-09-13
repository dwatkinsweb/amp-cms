// core needs to be in the global scope to ensure that it's the same for all sandboxes/pagelets
var core = null;
define(['ampcms/pagelet', 'order!jquery', 'order!ampcms/jquery.ba-bbq'], function(pagelet) {
	var pagelet_data = {}
	debug = true;

	if(core === null) {
		core = {
			debug : function(on) {
				debug = on ? true : false;
			},
			log : function(severity, message) {
				if(debug && window.console) {
					console[ (severity === 1) ? 'log' : (severity === 2) ? 'warn' : 'error'](message);
				} else {
					// send to the server
				}
			},
			// Event Handling Methods
			events : {
				publish : function(event) {
					for(pagelet in pagelet_data) {
						if(pagelet_data.hasOwnProperty(pagelet)) {
							pagelet = pagelet_data[pagelet];
							if(pagelet.events && pagelet.events[event.type]) {
								for(module_event in pagelet.events) {
									if(pagelet.hasOwnProperty(module_event)) {
										module_event = pagelet[module_event]
										module[event.type](event.data)
									}
								}
							}
						}
					}
				},
				subscribe : function(event, pagelet, module) {
					if(core.utils.is_object(events) && pagelet) {
						if(pagelet_data[pagelet]) {
							pagelet = pagelet_data[pagelet]
							if(pagelet.events && pagelet.events[module]) {
								pagelet.events[module] = core.utils.extend(pagelet.events[module], events);
							} else {
								pagelet.events[module] = events;
							}
						} else {
							core.log(1, "Events subscribed by non existant pagelet: " + pagelet);
						}
					} else {
						core.log(1, "Invalid parameters sent to event subscription: events: " + events + "; pagelet: " + pagelet);
					}

				},
				unsubscribe : function(event, pagelet, module) {
					if(core.utils.is_object(events) && pagelet) {
						if(pagelet_data[pagelet]) {
							pagelet = pagelet_data[pagelet]
							if(pagelet.events && pagelet.events[module]) {
								pagelet.events = core.utils.retract(pagelet.events[module], events);
							}
						} else {
							core.log(1, "Events subscribed by non existant pagelet: " + pagelet);
						}
					} else {
						core.log(1, "Invalid parameters sent to event subscription: events: " + events + "; pagelet: " + pagelet);
					}
				}
			},
			// DOM Methods
			dom : {
				find : function(scope, selector) {
					var ret, thiz, jq_elements, _i, _len;
					thiz = this;
					if( typeof selector === 'undefined') {
						selector = scope;
						scope = null;
					}
					if(scope && scope.find) {
						jq_elements = jQuery(scope).find(selector);
					} else {
						jq_elements = jQuery(selector);
					}
					ret = jq_elements.get();
					ret.length = jq_elements.length;
					ret.find = function(sel) {
						return thiz.find(jq_elements, sel);
					}
					return ret;
				},
				attr : function(element, attr, value) {
					var ret;
					if( typeof value === 'undefined') {
						ret = jQuery(element).attr(attr);
					} else {
						ret = jQuery(element).attr(attr, value);
					}
					return ret;
				},
				html : function(element, html) {
					var ret;
					if( typeof html === 'undefined') {
						ret = jQuery(element).html();
					} else {
						ret = jQuery(element).html(html);
					}
					return ret;
				},
				data : function(element, key, data) {
					var ret;
					if( typeof key === 'undefined') {
						ret = jQuery(element).data();
					} else if( typeof data === 'undefined') {
						ret = jQuery(element).data(key);
					} else { ret
						jQuery(element).data(key, data);
					}
					return ret;
				},
				bind : function(element, event, callback) {
					if(element && event) {
						if( typeof event === 'function') {
							callback = event;
							event = 'click';
						}
						jQuery(element).bind(event, callback);
					} else {
						// log wrong arguments
					}
				},
				unbind : function(element, event, callback) {
					if(element && event) {
						if( typeof event === 'function') {
							callback = event;
							event = 'click';
						}
						jQuery(element).unbind(event, callback);
					} else {
						// log wrong arguments
					}
				},
			},
			// Ajax Methods
			ajax : {
				get : function(url, callback) {
					jQuery.get(url, function(response) {
						response = jQuery.parseJSON(response);
						callback(response);
					});
				}
			},
			// Utility Methods
			utils : {
				is_array : function(arr) {
					return jQuery.isArray(arr);
				},
				is_object : function(obj) {
					return jQuery.isPlainObject(obj);
				},
				extend : function(object1, object2) {
					return jQuery.extend(object1, object2);
				},
				retract : function(object1, object2) {
					for(object in object2) {
						if(object1.hasOwnProperty(object)) {
							delete object1[object];
						}
					}
					return object1
				}
			},
			// Hash Methods
			history : {
				push_state : function(id, url) {
					var state = {};
					state[id] = url;
					return jQuery.bbq.pushState(state);
				},
				get_state : function(id) {
					return jQuery.bbq.getState(id);
				}
			},
			// Pagelet Handling
			load_pagelets : function() {
				var pagelet_id, new_pagelet, pagelet_element, pagelet_elements, _i, _len, thiz = this;
				pagelet_elements = this.page.find('.pagelet');
				for (_i = 0, _len = pagelet_elements.length; _i < _len; _i++) {
					pagelet_element = pagelet_elements[_i];
					pagelet_id = pagelet_element.id;
					this.log(1, "loading pagelet " + pagelet_id + " : " + pagelet_element);
					pagelet_data[pagelet_id] = pagelet.create(this, pagelet_id);
				}
				$(window).bind('hashchange', function() {
					var pagelet_id, pagelet, pagelet_state;
					for (pagelet_id in pagelet_data) {
						pagelet = pagelet_data[pagelet_id];
						pagelet_state = thiz.history.get_state(pagelet_id);
						pagelet.load_url(pagelet_state);
					}
				});
			},
		};
		core.page = core.dom.find('#page');
	}
	return core;
});
