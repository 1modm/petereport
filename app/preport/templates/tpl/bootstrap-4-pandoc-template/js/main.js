$( document ).ready(function() {
	$('[data-spy="scroll"]').each(function () {
        $(this).scrollspy('refresh');
    });
});