$(document).ready(function() 
{
	$( '#ProfileTabs a[data-toggle="tab"]' ).on( 'shown.bs.tab', 
            function (e) 
            {
                var tabIdentifier = $( e.target ).attr( 'href' ).replace( '#', '' ).toLowerCase();
                if ( tabCallbacks[tabIdentifier] && !$( e.target ).hasClass( 'callback-executed' ) ) {

                    tabCallbacks[tabIdentifier].apply( this, [e] );
                    $( e.target ).addClass( 'callback-executed' );
                }
            }
    );

    $('[data-toggle="tooltip"]').tooltip({'placement': 'top'});

    var hash = window.location.hash;
    $('#ProfileTabs a[href="' + hash + '"]').tab('show');
});