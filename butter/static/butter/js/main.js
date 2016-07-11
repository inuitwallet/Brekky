$( document ).ready(function() {

    $('#tx_type_buy').prop('checked', true);
    $('.sell-element').hide();
    $('.buy-element').show();

    $('.tx_type_buy').change(function( event ) {
        $('.sell-element').hide("fast");
        $('.buy-element').show("slow");
    });

    $('.tx_type_sell').change(function( event ) {
        $('.buy-element').hide("fast");
        $('.sell-element').show("slow");
    });



});