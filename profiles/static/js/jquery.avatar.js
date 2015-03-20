// Required for drag and drop file access
jQuery.event.props.push('dataTransfer');

// IIFE to prevent globals
(function() {

  function Avatar( element, options )
  {

      var that = this;
      this.defaults = {
          classDroppableArea: 'droppable',
          dropArea: null,
          fileInput: null,
          previewImage: null,
          imageWidth: null,
          imageHeight: null,
          callbackSuccess: function(){},
          callbackError: function(){}
      };

      this.setOption = function( option, value )
      {
          that.defaults[option] = value
      };

      this.setOptions = function( options )
      {
          that.defaults = $.extend( that.defaults, options );
      };

      this.bindUIActions = function() {

          var timer;

         /* $( that.defaults.dropArea  ).on( 'dragenter',
              function( event )
              {
                event.preventDefault();
              }
          );*/

          $( that.defaults.dropArea ).on( 'dragover', 
            function( event ) 
            {
                clearTimeout( timer );
                if ( event.currentTarget == $( that.defaults.dropArea )[0]) {
                 
                    that.showDroppableArea();
                    // Required for drop to work
                    return false;
                }
            }
          );

          $( that.defaults.dropArea ).on( 'dragleave', 
            function( event ) 
            {
                if ( event.currentTarget == $( that.defaults.dropArea )[0] ) {

                    // Flicker protection
                    timer = setTimeout(function() {
                        that.hideDroppableArea();
                      }, 
                      200
                    );
                }
            }
          );

          /*$( that.defaults.dropArea ).on( 'drop', 
              function( event ) 
              {

                  if ( event.currentTarget == $( that.defaults.dropArea )[0] ) {

                      // Or else the browser will open the file
                      event.preventDefault();

                      that.handleDrop( event.dataTransfer.files );
                  }
              }
          );*/

          $( that.defaults.fileInput ).on( 'change', 
            function( event ) 
            {
                that.handleDrop( event.target.files );
            }
          );

          $( that.defaults.previewImage ).data( 'old-src', $( that.defaults.previewImage ).attr( 'src' ) );

          $( that.defaults.previewImage ).closest( 'form' ).on( 'reset',
              function()
              {
                  $( that.defaults.previewImage ).attr( 'src', $( that.defaults.previewImage ).data( 'old-src' ) );
              }
          );
      };

      this.showDroppableArea = function() 
      {
          $( that.defaults.dropArea ).addClass( that.defaults.classDroppableArea );
      };

      this.hideDroppableArea = function() 
      {
          $( that.defaults.dropArea ).removeClass( that.defaults.classDroppableArea );
      };

      this.handleDrop = function( files ) 
      {

          that.hideDroppableArea();

          // Multiple files can be dropped. Lets only deal with the "first" one.
          var file = files[0];

          if ( typeof file !== 'undefined' && file.type.match('image.*') ) {

              that.currentFile = file;
              that.resizeImage( 
                    file, 
                    that.defaults.imageWidth, 
                    that.defaults.imageHeight,
                    function( data ) 
                    {
                        that.placeImage( data );
                    }
              );

          } else {

              if ( typeof that.defaults.callbackError == 'function' )
                  that.defaults.callbackError.apply( this, [files] );
              else
                  throw "That file wasn't an image.";
          }

      };

      this.resizeImage = function( file, width, height, callback ) 
      {
          var fileTracker = new FileReader;
          fileTracker.onload = function() {
              Resample(
                 this.result,
                 width,
                 height,
                 callback
             );
          }

          fileTracker.readAsDataURL( file) ;

          fileTracker.onabort = function() 
          {
              if ( typeof that.defaults.callbackError == 'function' )
                  that.defaults.callbackError.apply( this, arguments );
              else
                  throw "The upload was aborted.";
          }
          fileTracker.onerror = function() 
          {
              if ( typeof that.defaults.callbackError == 'function' )
                  that.defaults.callbackError.apply( this, arguments );
              else
                  throw "An error occured while reading the file.";
          }
      };

      this.placeImage = function( data ) 
      {
          $( that.defaults.previewImage ).attr( "src", data );

           if ( typeof that.defaults.callbackError == 'function' )
                that.defaults.callbackSuccess.apply( this, [data, that.currentFile] );
      };

      this.restorePreview = function()
      {
          $( that.defaults.previewImage ).attr( 'src', $( that.defaults.previewImage ).data( 'old-src' ) );
      };
      
      this.defaults.dropArea = $( element );
      this.setOptions( options );

      if ( !this.defaults.imageWidth )
          $(this.defaults.previewImage).on('load', function(){ that.defaults.imageWidth = $(that.defaults.previewImage).get(0).width });

      if ( !this.defaults.imageHeight )
          $(this.defaults.previewImage).on('load', function(){ that.defaults.imageHeight = $(that.defaults.previewImage).get(0).height });

      if ( !$( this.defaults.dropArea ).length || !$( this.defaults.fileInput ).length )
          throw "Must define droppable area and file input";

      this.bindUIActions();
  };

  var Resample = (function (canvas) {

         // (C) WebReflection Mit Style License

         function Resample(img, width, height, onresample) {
          var

           load = typeof img == "string",
           i = load || img;

          // if string, a new Image is needed
          if (load) {
           i = new Image;
           i.onload = onload;
           i.onerror = onerror;
          }

          i._onresample = onresample;
          i._width = width;
          i._height = height;
          load ? (i.src = img) : onload.call(img);
         }

         function onerror() {
          throw ("not found: " + this.src);
         }

         function onload() {
          var
           img = this,
           width = img._width,
           height = img._height,
           onresample = img._onresample
          ;
          // if width and height are both specified
          // the resample uses these pixels
          // if width is specified but not the height
          // the resample respects proportions
          // accordingly with orginal size
          // same is if there is a height, but no width
          var minValue = Math.min(img.height, img.width);
          width == null && (width = round(img.width * height / img.height));
          height == null && (height = round(img.height * width / img.width));

          delete img._onresample;
          delete img._width;
          delete img._height;

          // when we reassign a canvas size
          // this clears automatically
          // the size should be exactly the same
          // of the final image
          // so that toDataURL ctx method
          // will return the whole canvas as png
          // without empty spaces or lines
          canvas.width = width;
          canvas.height = height;
          // drawImage has different overloads
          // in this case we need the following one ...
          context.drawImage(
           // original image
           img,
           // starting x point
           0,
           // starting y point
           0,
           // image width
           minValue,
           // image height
           minValue,
           // destination x point
           0,
           // destination y point
           0,
           // destination width
           width,
           // destination height
           height
          );
          // retrieve the canvas content as
          // base4 encoded PNG image
          // and pass the result to the callback
          onresample(canvas.toDataURL("image/png"));
         }

         var context = canvas.getContext("2d"),
          // local scope shortcut
          round = Math.round
         ;

         return Resample;

    }(
     this.document.createElement("canvas"))
  );
	
  var pluginName = 'catalpa-avatar';


  $.fn.avatar = function( options ) 
    {
        var allArguments = arguments;
        return this.each(
          function()
          {
            var instance = $( this ).data( pluginName );
            if ( !instance ) {
              
              instance = new Avatar( $( this ), options );
              $( this ).data( pluginName, instance );
            }

              if ( typeof options == 'string' && instance[options] ) {
                  return instance[ options ].apply( this, Array.prototype.slice.call( allArguments, 1 ));
              } else if ( typeof options == 'object' ) {
                  return instance.setOptions.apply( this, allArguments );
              } else {
                  $.error( 'Method ' +  options + ' does not exist on jQuery.avatar' );
              }
          }
        );
    };


})();
