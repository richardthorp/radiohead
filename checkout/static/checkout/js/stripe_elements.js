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

// Listen to change events on the card Element and display any errors in the
// card-errors div
card.on('change', function ({error}) {
    if (error) {
        $('#card-errors').text(error.message);
    } else {
        $('#card-errors').text("");
    }
});

var form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
    ev.preventDefault();

    // Block user interaction with the card element and form submit button
    card.update({
        'disabled': true
    });
    $("#card-button").attr('disabled', true)

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
            // Unblock the card element and form submit button to allow user to fix error
            card.update({'disabled': false});
            $("#card-button").attr('disabled', false);
        } else {
            // The payment has been processed!
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});