// Get Stripe keys, mount card element to page and render card errors 
var stripe_public_key = $("#id_stripe_public_key").text().slice(1, -1);
var stripe = Stripe(stripe_public_key);
var elements = stripe.elements();

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