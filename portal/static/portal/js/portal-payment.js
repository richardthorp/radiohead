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

    // Get the client secret from the form data-secret attribute
    const clientSecret = form.dataset.secret;

    const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    });
});