// Submit the Portal Subscription payment
var form = document.getElementById('signup-form');
form.addEventListener('submit', function (ev) {
    ev.preventDefault();

    // Block user interaction with the card element and form submit button
    card.update({
        'disabled': true
    });
    $("#card-button").attr('disabled', true);
    $("#loading-overlay").fadeToggle(100);

    const clientSecret = $("#id_client_secret").text().slice(1, -1);
    const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    })
    .then(function (result) {
        if (result.error) {
            // Show error to your customer (e.g., insufficient funds)
            $("#card-errors").text(result.error.message);
            // Unblock the card element and form submit button to allow user to fix error
            card.update({
                'disabled': false
            });
            $("#card-button").attr('disabled', false);
            $("#loading-overlay").fadeToggle(100);
        } else {
            // The payment has been processed!
            // Hold the user on the loading screen for 8 seconds to allow stripe WH to be sent
            if (result.paymentIntent.status === 'succeeded') {
                setTimeout(function(){
                    form.submit();
                }, 8000)
            }
        }
    })
});
