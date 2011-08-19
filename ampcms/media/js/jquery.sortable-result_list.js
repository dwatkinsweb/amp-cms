(function($) {
	$.fn.extend({
		list_sort: function(options) {
			var defaults = {
				pos_field: 'order'
			};
			var opts = $.extend(defaults, options);
			return this.each(function(){
				_enhance_list($(this), pos_col);
				var pos_col = _find_col_list($(this), opts);
				if (!pos_col){
					return;
				}
				_initialize_list($(this), pos_col)
			});
		}
	});
	
	var _find_col_list = function(ele, options) {
		var cols = ele.find('tbody tr:first').children();
		for (var i = 0; i < cols.length; i++) {
			var inputs = $(cols[i]).find('input[name*='+options.pos_field+']');
			if (inputs.length > 0){
				return i;
			}
		}
		return false;
	};
	
	var _enhance_list = function(ele, pos_col) {
		ele.find('tbody > tr').each(function(idx){
			var pos_td = $(this).children()[pos_col];
			var input = $(pos_td).children('input').first();
			input.hide();
			$(pos_td).append('<strong>'+input.attr('value')+'</strong>')
		});
		
		ele.find('tbody > tr').prepend('<td class="inline-mover">&nbsp;</td>');
		ele.find('thead > tr').prepend('<th class="inline-mover">&nbsp;</th>');
	};
	
	var _initialize_list = function(ele, pos_col) {
	    var sorted = ele.find('thead th.sorted');
	    var sorted_col = ele.find('thead th').index(sorted);
	    var sort_order = sorted.hasClass('descending') ? 'desc' : 'asc';
		
	    if (sorted_col != pos_col){
	    	return;
	    }
		
		var _update_list_sort = function() {
	        var items = $(this).find('tr').get();
	        
	        if (sort_order == 'desc') {
	            // Reverse order
	            items.reverse();
	        }
	        
	        $(items).each(function(index) {
	            var pos_td = $(this).children()[pos_col];
	            var input = $(pos_td).children('input').first();
	            var label = $(pos_td).children('strong').first();
	            
	            input.attr('value', index+1);
	            label.text(index+1);
	        });
	        
	        // Update row classes
	        $(this).find('tr').removeClass('row1').removeClass('row2');
	        $(this).find('tr:even').addClass('row1');
	        $(this).find('tr:odd').addClass('row2');
	    };
	    
	    ele.find('tbody').sortable({
	        axis: 'y',
			handle: '.inline-mover',
	        items: 'tr',
	        cursor: 'move',
	        update: _update_list_sort
	    });
	};
})(jQuery);