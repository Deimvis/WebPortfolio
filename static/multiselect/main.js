(function($) {

	"use strict";

	 $(document).ready(function() {
        $('.multiple-checkboxes').multiselect({
          includeSelectAllOption: true,
          nonSelectedText: '—',
          numberDisplayed: 10,
          ignoreAllSelected: true,
        });
    });

})(jQuery);
