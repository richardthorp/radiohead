// Get the card details from the user and send to set_default_card view
// Update payment details code taken from https://stripe.com/docs/payments/save-and-reuse
var updateCardForm = document.getElementById('update-card-form');
updateCardForm.addEventListener('submit', function (ev) {
    ev.preventDefault();
    card.update({
        'disabled': true
    });
    $("#update-button").attr('disabled', true);
    $("#loading-overlay").fadeToggle(100);
    const cardholderName = $('#cardholder-name').val();
    const clientSecret = updateCardForm.dataset.secret;
    stripe.confirmCardSetup(
        clientSecret,
        {payment_method: {
            card: card,
            billing_details: {
                name: cardholderName,
            },
        },
    })
    .then(function(result) {
        if (result.error) {
            // Display error.message in your UI.
            $('#card-errors').text(result.error);

            console.log(result.error)
        } else {
            // The setup has succeeded. Display a success message.
            const csrfToken = $("input[name=csrfmiddlewaretoken]").val();
            const url = '/portal/set_default_card/';
            const postData = {
                'csrfmiddlewaretoken': csrfToken,
                'payment_method_id': result['setupIntent']['payment_method'],
            };
            // Send data to set_default_card view for processing and then submit for to direct user
            // back to profile page
            $.post(url, postData).done(function(){
                updateCardForm.submit()
            })
        }
    })
    ;
}); 