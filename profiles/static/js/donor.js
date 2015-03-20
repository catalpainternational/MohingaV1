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

    var hash = window.location.hash;
    $('#ProfileTabs a[href="' + hash + '"]').tab('show');

    $('#sector_container').readmore(
        {
            maxHeight: 213,
            moreLink: '<a href="#">' + translations.see_more + '</a>'
        }
    );

    $('#DP-address form').ajaxForm({
        beforeSubmit: function(arr, form )
        {
            $( form ).message( translations.loading, 'info' );
        },
        success: function( response )
        {
            $( arguments[3] ).message( translations.success, 'success' );

            $( '#DP-address' ).collapse('hide');
            
            /*var data = $( '#DP-address form' ).serializeArray();
            $.each( data, 
                function( i, item )
                {
                    $( '.Address.' + item.name ).html( item.value );
                }
            );*/

            $( '#contact-container' ).load( djangoUrls.contact_html.replace( '0000', response.pk ) );

            $( arguments[3] ).message( 'clearMessages' );
        },
        error: function( response ) { 

            var dataJson = response.responseJSON;
            var message = translations.required_fields;
            if ( dataJson && dataJson.message )
                message = dataJson.message;

            $( arguments[3] ).message( message ).message( 'invalidFields', dataJson );
        }
    });

    $( '#uploader' ).click(
        function()
        {
            $( '#id_photo' ).trigger( 'click' );
        }
    );

    $( '#choose-logo' ).click(
        function()
        {
            $( '#donor-logo' ).trigger( 'click' );
        }
    );

    $( '#donor-banner' ).on( 'change',
        function()
        {
            $( '#banner-image .banner-image-preview, #banner-image .banner-error').addClass( 'hide' );
            $( '#banner-image .banner-success').removeClass( 'hide' );
        }
    );

    $( '#profile-avatar' ).avatar({fileInput: '#id_photo', previewImage: '#image-avatar'});
    $( '#profile-avatar-logo' ).avatar({
        fileInput: '#donor-logo', 
        previewImage: '#profile-avatar-logo img',
        callbackSuccess: function()
        {
            $( '#form-logo' ).submit();
        }
    });

    //$( '#profile-banner' ).avatar({fileInput: '#donor-banner', previewImage: '#profile-banner img'});

    $( '#choose-banner' ).click(
        function()
        {
            $( '#donor-banner' ).trigger( 'click' );
        }
    );

    $('#form-logo').ajaxForm({
        success: function( response )
        {
            $( '#form-logo .ProfileAvatar-container img' ).attr( 'src', response.image );
        },
        error: function( response ) { 
            $( '#profile-avatar-logo' ).avatar( 'restorePreview' );
        }
    });

     $('#form-banner').ajaxForm({
        success: function( response )
        {
            $( '#banner-image .banner-image-preview, #banner-image .banner-error').addClass( 'hide' );
            $( '#banner-image .banner-success').removeClass( 'hide' );

            $( '#banner-image' ).modal( 'hide' );
            $( '.ProfileBanner' ).css( 'background-image', 'url("' + response.image + '")' );

            setTimeout(
                function()
                {
                    $( '#banner-image .banner-image-preview').removeClass( 'hide' );
                    $( '#banner-image .banner-success').addClass( 'hide' );
                }
                , 2000 );

        },
        error: function( response ) { 
            //$( '#profile-avatar-logo' ).avatar( 'restorePreview' );

            $( '#banner-image .banner-image-preview,#banner-image .banner-success').addClass( 'hide' );
            $( '#banner-image .banner-error').removeClass( 'hide' );
        }
    });

    $( '#save-donor-banner' ).click(
        function()
        {
            if ( $( '#donor-banner' ).val() )
                $( '#form-banner' ).submit();
        }
     );


    $('#new_person form').ajaxForm({
        beforeSubmit: function(arr, form )
        {
            if ( $('#new_person form').hasClass( 'submitting' ) )
                return false;

            $( form ).message( translations.loading, 'info' ).addClass( 'submitting' );
        },
        success: function( response )
        {
            $( arguments[3] ).message( translations.success, 'success' ).get( 0 ).reset();
            fetchPerson( response.pk );
        },
        complete: function()
        {
            $('#new_person form').removeClass( 'submitting' );
        },
        error: function( response ) { 

            var dataJson = response.responseJSON;
            var message = translations.required_fields;
            if ( dataJson && dataJson.message )
                message = dataJson.message;

            $( arguments[3] ).message( message ).message( 'invalidFields', dataJson );
        }
    });

    //toggle `popup` / `inline` mode
    $.fn.editable.defaults.mode = 'inline';
    
    $('#DPobjective').editable({
        name: 'banner_text',
        type: 'textarea',
        toggle: 'manual',
        validate: function( value )
        {
            return !value.length ? translations.required : null;
        },
        url: djangoUrls.update
        
    });

    $('#DPobjective').on('shown', function() {
        $(this).data('editable').input.$input.attr( 'maxlength', 140 );
    });
	
	// Data Toggles
    $('#edit_objective').click(function(e) {
        e.stopPropagation();
        e.preventDefault();
        $('#DPobjective').editable('toggle');
    });
    
    $('#DP_background').editable({
        name: 'background',
        type: 'textarea',
        toggle: 'manual',
        validate: function( value )
        {
            return !value.length ? translations.required : null;
        },
        url: djangoUrls.update
    });

    $('#DP_background').on('shown', function() {
        $(this).data('editable').input.$input.attr( 'maxlength', 8000 );
    });
    
    $('#edit_background').click(function(e) {
        e.stopPropagation();
        e.preventDefault();
        $('#DP_background').editable('toggle');
    });
    
	$( '#person-container' ).on('click', '.edit-button-profile',
        function()
        {
            editPerson( $( this ).data( 'pk' ) );
        }
    );

    $( '#new_person form' ).on( 'reset',
        function()
        {
            $( this ).attr( 'action', $( this ).data( 'default-action' ) );
            $( this ).message( 'clearMessages' );
            $( this ).find( '#delete-person' ).addClass( 'hide' ).data('pk', null);
        }
    );

    $( '.sortable' ).sortable({
        handle: '.handle'
    });

    $( '.sortable' ).on( "sortupdate", reorderPeople );

    /*
    $( '#Projects .btn-group button').on( 'click',
        function()
        {
            var buttonId = $( this ).data( 'id' );
            $( '#Projects .activity-block' ).fadeOut().each(
                function()
                {
                    if ( $( this ).find( '.label-' + buttonId ).length )
                        $( this ).fadeIn();
                }
            );
        }
    );
    */

    $( '.filter_list input' ).on( 'ifToggled', 
        function()
        {
            var filters = {};
            $( '.filter_list input:checked' ).each(
                function()
                {
                    var itemFilter = $(this).data('filter');
                    for ( id in itemFilter ) {

                        if ( !filters[id] )
                            filters[id] = [];

                        filters[id].push(itemFilter[id]);
                    }
                }
            );
            
            filterActivites(filters);
        }
    );
});

function filterActivites( filters )
{
    $( '#Projects .activity-block' ).hide().each(
        function()
        {
            var show = true;
            var attrs = eval('(' + $(this).data('activity') + ')');

            for ( idFilter in filters ) {

                if ( filters[idFilter].length ) {

                    if ( !attrs[idFilter] ) {
                        show = false;
                        break;
                    } else if ( $.isArray( attrs[idFilter] ) &&
                         $(filters[idFilter]).filter(attrs[idFilter]).length != filters[idFilter].length ) {
                        show = false;
                        break;
                    } else if ( !$.isArray( attrs[idFilter] ) && $.inArray( attrs[idFilter], filters[idFilter] ) < 0 ) {
                        show = false;
                        break;
                    }
                }
            }

            if ( show ) $( this ).fadeIn();
        }
    );
}

function reorderPeople()
{
    var people = [];
    $( '.sortable li').each(
        function()
        {
            people.push( $( this ).data( 'pk' ) );
        }
    );

    $.ajax(
        {
            type: 'GET',
            url: djangoUrls.reorder_people,
            data: { people: people }
        }
    );
}


function fetchPerson( pk )
{
    $.ajax(
        {
            type: 'GET',
            url: djangoUrls.person_html.replace( '0000', pk ),
            dataType: 'html',
            success: function( response )
            {
                $( '#person-container #person-' + pk ).remove();

                $( '#person-container' ).prepend( response );
                $( '#person-container' ).find( 'li.person-profile:first' ).css( 
                    {
                        opacity: '0.5',
                        backgroundColor: '#F7FCCF'
                    }
                ).animate(
                    {
                        opacity: '1'
                    }, 
                    'slow',
                    function()
                    {
                        $( this ).css( 'backgroundColor', '#fff' );
                    }
                );

                scrollTo( $( '#person-container #person-' + pk ) );
                $('.sortable').sortable({
                    handle: '.handle'
                });
            }
        }
    );
}

function editPerson( pk )
{
    $('#new_person form').trigger( 'reset' ).get(0).reset();
    $('#new_person').collapse('show');
     scrollTo( $('#new_person form') );
    $('#new_person form').message( translations.loading, 'info' );

    $.ajax(
        {
            type: 'GET',
            url: djangoUrls.person_data.replace( '0000', pk ),
            dataType: 'json',
            success: function( response )
            {
                $.each( response.fields,
                    function( index, value )
                    {
                        if ( index != 'photo' )
                            $( '[name=' + index + ']', $('#new_person form') ).val( value );
                    }
                );

                if ( response.fields.photo )
                    $( '#image-avatar' ).attr( 'src', djangoUrls.media_url + response.fields.photo );

                $('#new_person form').attr( 'action', djangoUrls.update_person.replace( '0000', pk ) );

                $('#new_person form').message( 'clearMessages' );
                $('#new_person form').find( '#delete-person' ).removeClass( 'hide' ).data('pk', pk);
            }
        }
    );
}

function scrollTo( seletor, time )
{
    if ( !$( seletor ).length )
        return false;

    el = $( seletor );
    time = time || 1000;

    if (  el.closest( '.modal-body' ).length ) {
        
        scroller = el.closest( '.modal-body' );
        scroll = el.position().top;
        
    } else {
        
        scroller = 'html,body';
        scroll = el.offset().top - 80;
    }

    $( scroller ).animate({scrollTop : scroll}, time );
    return true;
}

function removePerson()
{
    var pk = $( '#new_person form' ).find( '#delete-person' ).data('pk');
    if ( !pk ) return false;

    confirmDialog(
        translations.confirm_delete,
        function()
        {
            $('#new_person form').message( translations.loading, 'info' );
            
            $.ajax(
            {
                type: 'GET',
                url: djangoUrls.delete_person.replace( '0000', pk ),
                dataType: 'json',
                complete: function()
                {
                    $( '#new_person form' ).trigger( 'reset' ).get(0).reset();
                },
                success: function( response )
                {
                    if ( response.status ) {

                        $( '#person-container li#person-' + pk ).fadeOut(
                            'slow',
                            function()
                            {
                                $( this ).remove();
                            }
                        );
                    }
                }
            }
            );
        }
    );
}

function confirmDialog( text, callback )
{
    $( '#confirm-dialog .modal-body p' ).html( text );
    $( '#confirm-dialog .modal-footer #button-delete' ).unbind( 'click' ).click(
        function()
        {
            $( '#confirm-dialog' ).modal( 'hide' );
            callback.call();
        }
    );

    $( '#confirm-dialog' ).modal( 'show' );
}
