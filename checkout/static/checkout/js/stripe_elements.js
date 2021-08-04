// Stripe checkout proccess Boutique Ado walkthrough project and Stripe documentation
// https://stripe.com/docs/payments/accept-a-payment?platform=web&ui=elements

var stripe_public_key = $("#id_stripe_public_key").text().slice(1, -1);
var stripe = Stripe(stripe_public_key)
var elements = stripe.elements();
// var style = {
//     base: {
//       color: "#32325d",
//     }
//   };

var style = {
    base: {},
    invalid: {}
};

var card = elements.create("card"); // ADD STYLE ELEMENTS AS OBJECT HERE '{ style: style }'
card.mount("#card-element");

// Listen to change events on the card Element and display any errors
card.on('change', ({
    error
}) => {
    let displayError = $('#card-errors');
    if (error) {
        displayError.text(error.message);
    } else {
        displayError.text("");
    }
});

var form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    // Get the client secret from the form data-secret attribute
    const clientSecret = form.dataset.secret;
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
            billing_details: {
                name: $.trim(form.name.value),
                email: $.trim(form.email.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    line1: $.trim(form.address_line1.value),
                    line2: $.trim(form.address_line2.value),
                    postal_code: $.trim(form.postcode.value),
                    state: $.trim(form.county.value)
                }
            }
        },
        shipping: {
            name: $.trim(form.name.value),
            phone: $.trim(form.phone_number.value),
            address: {
                city: $.trim(form.town_or_city.value),
                country: $.trim(form.country.value),
                line1: $.trim(form.address_line1.value),
                line2: $.trim(form.address_line2.value),
                postal_code: $.trim(form.postcode.value),
                state: $.trim(form.county.value),
            }
        }
    }).then(function (result) {
        if (result.error) {
            // Show error to your customer (e.g., insufficient funds)
            $("#card-errors").text(result.error.message);
            console.log(result.error.message);
        } else {
            // The payment has been processed!
            if (result.paymentIntent.status === 'succeeded') {
                // Show a success message to your customer
                // There's a risk of the customer closing the window before callback
                // execution. Set up a webhook or plugin to listen for the
                // payment_intent.succeeded event that handles any business critical
                // post-payment actions.
            }
        }
    });
});