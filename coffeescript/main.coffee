require ['jquery', 'page', 'pagelet', 'jquery.ba-bbq', 'amplify.core'], ($, Page, Pagelet) ->
    require.ready () ->
        page = new Page('#page')
        
        console.log('main subscribing to ampcms.pageletload')
        amplify.subscribe 'ampcms.pageletload', (pagelet) ->
            console.log('ampcms.pageletload triggered')
            pagelet.transform_links().transform_forms()
        
        console.log('main subscribing to ampcms.pageload')
        amplify.subscribe 'ampcms.pageload', (page) ->
            console.log('ampcms.pageload triggered')
            $(window).trigger('hashchange')
        
        console.log('main subscribing to hashchange')
        $(window).bind 'hashchange', (event) ->
            console.log('hashchange triggered')
            page.load_pagelets()
        
        console.log('load pagelets')
        page.load_pagelets()
