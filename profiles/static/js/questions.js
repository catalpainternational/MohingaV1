$(document).ready(function() {
    //toggle `popup` / `inline` mode
    $.fn.editable.defaults.mode = 'inline';
    
    $('#DPobjective').editable({
        url: '/post',
        title: 'Enter objective',
        rows: 2,
        toggle: 'manual'
        
    });

    $('#DP_background').editable({
        url: '/post',
        title: 'Enter comments',
        rows: 20,
        toggle: 'manual'
    });
		
	
	// Data Toggles
	    
    $('#DPobjective').editable();
    $('#edit_objective').click(function(e) {
        e.stopPropagation();
        e.preventDefault();
        $('#DPobjective').editable('toggle');
    });
    
    $('#DP_background').editable();
    $('#edit_background').click(function(e) {
        e.stopPropagation();
        e.preventDefault();
        $('#DP_background').editable('toggle');
    });
    
	
});


