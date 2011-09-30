require.config({
	baseUrl: '/media/js',
	paths: {
		'jquery' : 'https://ajax.googleapis.com/ajax/libs/jquery/1.6.3/jquery.min',
		'ampcms' : '/media/ampcms/js/ampcms',
		'order' : '/media/ampcms/js/libs/order'
	}
});
require(['ampcms/core'], function(core) {
	return require.ready(function() {
		core.load_pagelets();
	});
});
