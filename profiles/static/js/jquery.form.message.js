(function($){
	"use strict";

	var MessagePlugin = function(el, options )
	{
		this.defaults = {
			fadeOut: false,
			element: el,
			errorClass: 'danger',
			successClass: 'success',
			infoClass: 'info',
			defaultClass: 'errorClass',
			fadeOutTime: 1000
		};

		this.clearMessages = function()
		{
			var divContainer = $( that.defaults.element );

			if ( divContainer.find( '.alert' ).length )
		    	divContainer.find( '.alert:not(.not-remove)' ).remove();

		    divContainer.find( '.form-group.has-error' ).removeClass('has-error');
		    divContainer.find( '.help-block' ).remove();

		    return that;
		};

		this.invalidFields = function( fields )
		{
			$.each(
				fields,
				function( index, value )
				{
					var element = $( '[name=' + index + ']', that.defaults.element );
					if ( !element ) return true;
					$( element ).closest( '.form-group' ).addClass( 'has-error' );

					$.each( 
						value,
						function( i, message )
						{
							var span = $( '<span />' ).addClass( 'help-block' );
							span.html( message );
							element.closest( '.controls' ).append( span );
						}
					);
				}
			);
		};

		this.setOption = function( option, value )
	    {
			that.defaults[option] = value
	    };

	    this.setOptions = function( options )
	    {
	    	that.defaults = $.extend( that.defaults, options );
	    };

	    this.showMsg = function( text, type )
	    {
	    	that.clearMessages();

	    	if ( typeof type == 'object' )
	    		that.setOptions( type );

	    	var type = type || that.defaults[that.defaults.defaultClass];

			var divContainer = $( that.defaults.element );
			if ( divContainer.find( '.alert' ).length )
			    divContainer.find( '.alert:not(.not-remove)' ).remove();

			var msgDiv = $( '<div />' );
			msgDiv.addClass( 'alert animated bounce alert-' + type );

			var buttonClose = $( '<button />' );
			buttonClose.attr( 'type', 'button' )
				    .addClass( 'close' )
				    .attr( 'data-dismiss', 'alert' );

			msgDiv.html( text );
			msgDiv.prepend( buttonClose );

			divContainer.prepend( msgDiv );

			msgDiv.fadeIn();

			if ( that.defaults.fadeOut ) {
			    
			    setTimeout(
					function()
					{
					    msgDiv.fadeOut( 'slow',
						function()
						{
						    msgDiv.remove();
						}
					    );
					},
					10 * that.defaults.fadeOutTime
				);
			}
			
			that.defaults.fadeOut = true;
			return that;
	    };

	    this.msgError = function( text )
	    {
	    	return that.showMsg( text, that.defaults.errorClass );
	    };

	    this.msgInfo = function( text )
	    {
	    	return that.showMsg( text, that.defaults.infoClass );
	    };

	    this.msgSuccess = function( text )
	    {
	    	return that.showMsg( text, that.defaults.successClass );
	    };

	    var that = this;
		this.setOptions( options );
	};

	var pluginName = 'bootstrap-message';


	$.fn.message = function( options ) 
    {
    	var allArguments = arguments;
    	return this.each(
    		function()
    		{
    			var instance = $( this ).data( pluginName );
    			if ( !instance ) {
    				
    				instance = new MessagePlugin( $( this ), options );
    				$( this ).data( pluginName, instance );
    			}

    			if ( instance[options] ) {
		            return instance[ options ].apply( this, Array.prototype.slice.call( allArguments, 1 ));
		        } else if ( typeof options == 'string' ) {
		            return instance.showMsg.apply( this, allArguments );
		        } else {
		            $.error( 'Method ' +  options + ' does not exist on jQuery.message' );
		        }
    		}
    	);
    };
}
(jQuery));