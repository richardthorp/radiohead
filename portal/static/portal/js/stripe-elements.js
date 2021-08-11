// const emailInput = document.querySelector('#email');
var stripe_public_key = $("#id_stripe_public_key").text().slice(1, -1);
var stripe = Stripe(stripe_public_key)
var elements = stripe.elements();

var form = document.getElementById('signup-form');
let card = elements.create('card');
let submitBtn = document.getElementById('card-button');

card.mount('#card-element');
card.on('change', function (event) {
    displayError(event);
});

function displayError(event) {
    let displayError = document.getElementById('card-errors');
    if (event.error) {
        displayError.textContent = event.error.message;
    } else {
        displayError.textContent = '';
    }
}



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
