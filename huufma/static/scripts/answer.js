const radio_selectors = document.querySelectorAll( "input[type = 'radio']" )

        for ( const r_selector of radio_selectors ){
            r_selector.addEventListener( "click", function( event ){
                radio_selectors.forEach( function ( item ) {
                    if ( itemm != event.target ){
                        item.checked = false
                    }
                } )
            } )
        }