/* For a cleaner solution that I haven't managed to make work, see also http://stackoverflow.com/questions/501719/dynamically-adding-a-form-to-a-django-formset-with-ajax */


function hide_extras(selectors_0, canary_selector, canary_placeholder_value){
    /**
     * Hides the selectors_0 fields after the first set if their value is the default one
     */
    var i = 0;
    while ( true ) {
        i += 1;
        var replacement = "-"+i+"-";
        var selector = canary_selector.replace(/(-0-)/,replacement);
        if ( $(selector).length == 0 ) {
            return;
        }

        if ( $(selector).val() == canary_placeholder_value && $(selector).closest('.has-error').length < 1 ) { // is a default value

            for(var s=0; s<selectors_0.length; s++){
                var selector = selectors_0[s].replace(/(-0-)/,replacement);

                if ( selectors_0[s].indexOf('DELETE') != -1 ) {
                    $( selector ).parent().hide()
                } else {
                    $( selector ).hide();
                }
                $(selector).find('select').removeAttr('data-parsley-required');
                $(selector).find('select').removeData('parsleyRequired');
                $(selector).find('.numberinput').removeAttr('data-parsley-required');
                $(selector).find('.numberinput').removeData('parsleyRequired');
            }
        }
    }
}


function reveal(selectors_0, to_hide_if_max){
    /* Find the next set of selectors that are not shown and make them visible. */
    var i = -1;
    var done = false;
    while(true){
        i+=1;
        var replacement = "-"+i+"-";
        var selector = selectors_0[0].replace(/(-0-)/,replacement);
        var name = $(selector).attr('id')
        if ($(selector).length == 0){
//            console.log("should hide", to_hide_if_max, $(to_hide_if_max).length);
            $(to_hide_if_max).hide();
            return;
        }
        if (done){
            return;
        }
        if($(selector).is(":visible") == false){
            for(var s=0; s<selectors_0.length; s++){
                var selector = selectors_0[s].replace(/(-0-)/,replacement);

                if ( selectors_0[s].indexOf('DELETE') != -1 ) {
                    $( selector ).parent().show()
                } else {
                    $( selector ).show();
                }

                if(name.match('financing') || name.match('ministry') || name.match('participating_organisation') || name.match('location')){
                    $(selector).find('select').attr('data-parsley-required', 'true');
                }
                else if(name.match('sector') || name.match('national_sector')){

                    $(selector).find('.numberinput').attr('data-parsley-required', 'true');
                }
            }
            done = true;
        }
    }
}


$(document).ready(
    function()
    {
        $('input[id$="DELETE"]').off('change.delete');
        $('input[id$="DELETE"]').on(
          'change.delete',
          function()
          {
                if ( $(this).is(':checked') ) {

                    console.log('Is Checked');

                    var id = $(this).attr('id').replace('-DELETE', '');
                    var idElement = $('#' + id + '-id').val();

                    if ( !idElement ) {

                        var elements = $('[id^="' + id + '-"]' ).not('[id$="DELETE"]').not(':hidden');

                        var idCheckbox = '#' + $(this).attr('id');
                        elements.each(
                            function()
                            {
                                $(this).parsley().reset();
                                $(this).val('').trigger('change').removeAttr('data-parsley-required').removeData('parsleyRequired');
                                console.log($(this));
                                $(this).closest('.form-group').hide();
                            }
                        );

                        $(this).attr('checked', false);
                        $(this).closest('.form-group').hide();
                    }
                }
          }
        );
    }
);