/*
 * FIXME: The following functions need to be implemented in a non library specific way or by using a smaller micro library:
 *  - dom.find
 *  - dom.data
 *  - dom.replace
 *  - dom.attr
 *  - ajax.get
 *  - utils.is_object
 *  - utils.retract
 */

// TODO: currently, I think core needs to be in the global scope to ensure that it's the same for all sandboxes/pagelets
var core = null;
define(['require', 'ampcms/pagelet', 'ampcms/sandbox', 'libs/history'], function(require, pagelet, sandbox) {
	var pagelet_data = {}, loaded_css = [], HistoryPlugin = History, PAGE, config;
	var config = {
		debug : false,
		log_server : false
	}
	if(core === null) {
		core = {
			log : function(severity, message) {
				if (typeof message === 'undefined') {
					message = severity;
					severity = 1;
				}
				if(config.debug && window.console) {
					console[ (severity === 1) ? 'log' : (severity === 2) ? 'warn' : 'error'](message);
				} else if (config.log_server && typeof core.server_log !== 'undefined') {
					core.server_log(severity, message);
				}
			},
			load_css : function(css) {
				this.log('loading css: ' + css);
				var _i, _len, _css_file;
				for (_i = 0, _len = css.length; _i < _len; _i++) {
					css_file = css[_i];
					if (!this.utils.in_array(loaded_css, css_file)) {
						if (css_file != null) {
							if (document.createStyleSheet) {
								document.createStyleSheet(css_file);
							} else {
								var head = document.getElementsByTagName('head')[0];
								var css_link = document.createElement('link');
								css_link.setAttribute('rel', 'stylesheet');
								css_link.setAttribute('type', 'text/css');
								css_link.setAttribute('href', css_file);
								head.appendChild(css_link);
							}
						}
						loaded_css.push(css_file);
					}
				}
			},
			load_js : function(js, callback) {
				this.log('loading js: ' + js);
				require(js, callback);
			},
			load_page : function(module, page, pagelets) {
				var _key, pagelet_data = [];
				for (_key in pagelets) {
					if (pagelets.hasOwnProperty(_key)) {
						pagelet_data.push(_key+'-pagelet='+pagelets[_key]);
					}
				}
				this.redirect('/'+module+'/'+page+'?'+pagelet_data.join('&'));
			},
			redirect : function(url) {
				location.href = url;
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
										module_event = pagelet[module_event];
										module[event.type](event.data);
									}
								}
							}
						}
					}
				},
				subscribe : function(event, pagelet, module) {
					if(core.utils.is_object(events) && pagelet) {
						if(pagelet_data[pagelet]) {
							pagelet = pagelet_data[pagelet];
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
							pagelet = pagelet_data[pagelet];
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
			// History Handling
			history : {
				push_state : function(id, url) {
					var new_url = '?'+id+'='+url;
					var title = id+' : '+url;
					var data = {};
					data[id] = url;
					// TODO: Currently not implementing title changes.
					HistoryPlugin.pushState(data, null, new_url);
				},
				replace_state : function(id, url) {
					var new_url = '?'+id+'='+url;
					var title = id+' : '+url;
					var data = {};
					data[id] = url;
					// TODO: Currently not implementing title changes.
					HistoryPlugin.replaceState(data, null, new_url);
				},
				get_state : function(id) {
					var state = History.getState(), data = state.data, query_string;
					if (core.utils.is_empty_object(data)) {
						query_string = window.location.search;
						if (query_string === "") {
							query_string = window.location.hash;
							if (query_string.length > 1) {
								query_string = query_string.substring(1);
							}
						}
						if (query_string.length > 1) {
							data = core.parse_query_string(query_string);
						}
						History.pushState(data, null, query_string);
						if (!window.history || !window.history.pushState) {
							window.location.search = '';
						}
						state = History.getState();
					}
					if (typeof id !== 'undefined') {
						state = state.data[id];
					}
					return state;
				},
				back : function() {
					HistoryPlugin.back();
				},
				forward : function() {
					HistoryPlugin.forward();
				},
				go : function(x) {
					HistoryPlugin.go(x);
				},
				subscribe : function(callback) {
					HistoryPlugin.Adapter.bind(window, 'statechange', callback);
				}
			},
			dom : {
				bind : function(target, event, callback) {
					HistoryPlugin.Adapter.bind(target, event, callback);
				}
			},
			utils : {
				is_empty_object : function(obj) {
				    for (var key in obj) {
				    	if (obj.hasOwnProperty(key)) {
				    		return false;
				    	}
				    }
				    return true;
				}
			},
			decode : function(s) {
				try {
					return decodeURIComponent(s).replace(/\r\n|\r|\n/g, "\r\n");
				} catch (e) {
					return "";
				}	
			},
			parse_query_string : function(query_string) {
				var multimap = {};
				if (query_string.length > 1) {
					query_string = query_string.substring(1);
					query_string.replace(/([^=&]+)=([^&]*)/g, function(match, hfname, hfvalue) {
						var name = core.decode(hfname);
						var value = core.decode(hfvalue);
						if (name.length > 0) {
							if (!multimap.hasOwnProperty(name)) {
								multimap[name] = [];
							}
							multimap[name].push(value);
						}
					});
			    }
			    return multimap;
			},
			build_query_string : function(array) {
				var key, map = [];
				for (key in array) {
					map.push(key+'='+array[key]);
				}
				return map.join('&');
			},
			// Pagelet Handling
			load_pagelets : function() {
				var pagelet_id, new_pagelet, pagelet_element, pagelet_elements, _i, _len, thiz = this;
				pagelet_elements = PAGE.find('.pagelet');
				for (_i = 0, _len = pagelet_elements.length; _i < _len; _i++) {
					pagelet_element = pagelet_elements[_i];
					pagelet_id = pagelet_element.id;
					this.log("loading pagelet " + pagelet_id + " : " + pagelet_element);
					pagelet_data[pagelet_id] = pagelet.create(this, pagelet_id);
				}
				this.history.subscribe(function() {
					thiz.log("loading state");
					var pagelet_id, pagelet, pagelet_state;
					for (pagelet_id in pagelet_data) {
						pagelet = pagelet_data[pagelet_id];
						pagelet_state = thiz.history.get_state(pagelet_id);
						pagelet.load(pagelet_state);
					}
				});
			},
			config : function(ampcms_config) {
				this.log('loading configurations');
				var thiz = this, extensions = [], extension_targets = [], i = 0;
				if (typeof ampcms_config.config !== 'undefined') {
					config = this.extend(config, ampcms_config.config);
				}
				
				if (typeof ampcms_config.extensions.core !== 'undefined') {
					extensions[i] = ampcms_config.extensions.core;
					extension_targets[i] = this;
					i += 1;
				}
				if (typeof ampcms_config.extensions.pagelet !== 'undefined') {
					extensions[i] = ampcms_config.extensions.pagelet;
					extension_targets[i] = pagelet.extension;
					i += 1;
				}
				if (typeof ampcms_config.extensions.sandbox !== 'undefined') {
					extensions[i] = ampcms_config.extensions.sandbox;
					extension_targets[i] = sandbox.extension;
				}
				require(extensions, function(){
					var _i, _len, target_object, mixin_object;
					for (_i = 0, _len = arguments.length; _i < _len; _i++) {
						target_object = extension_targets[_i];
						mixin_object = arguments[_i];
						target_object = core.extend(target_object, mixin_object);
					}
					// TODO: Don't really want to add page here but need it for some stuff in pagelet.
					thiz.page = PAGE = thiz.dom.find('#page');
					thiz.load_pagelets();
				});
			},
			extend : function(destination, source) {
				for (var k in source) {
					if (source.hasOwnProperty(k)) {
						if (typeof destination[k] === 'object' && typeof source[k] === 'object') {
							destination[k] = core.extend(destination[k], source[k]);
						} else {
							destination[k] = source[k]
						}
					}
				}
				return destination;
			}
		};
	}
	return core;
});
