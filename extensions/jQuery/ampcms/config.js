var ampcms_config = function() {
	return {
		require : {
			paths : {
				'jquery' : 'https://ajax.googleapis.com/ajax/libs/jquery/1.6.3/jquery.min',
				// TODO: for some reason the jquery one doesn't seem to notice that jquery is loaded. The regular one seems to work fine however.
				//'libs/history' : '/media/js/libs/jquery/jquery.history',
			},
			deps : ['jquery']
		},
		ampcms : {
			config : {
				debug : true,
			},
			extensions : {
				core : 'ampcms/ext/core',
				pagelet : 'ampcms/ext/pagelet',
				sandbox : 'ampcms/ext/sandbox'
			}
		}
	};
}();


