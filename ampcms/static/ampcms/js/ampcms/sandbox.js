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
				push_url : function(url, force_refresh) {
					pagelet.load(url, force_refresh);
				},
				refresh_pagelet : function() {
					pagelet.load(null, true);
				},
				push_message : function(message) {
					return pagelet.push_message(message);
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
				},
				transform_links : function(container, callback) {
					if (typeof container === 'undefined') {
						callback = null;
						container = CONTAINER;
					}
					pagelet._transform_links(container, callback);
				}
			};
			sandbox = pagelet.extend(sandbox, this.extension.create(pagelet, CONTAINER));
			return sandbox;
		},
		extension : {}
	};
});
