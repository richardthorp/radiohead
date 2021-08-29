// Submit the Portal Subscription payment
var form = document.getElementById('signup-form');
form.addEventListener('submit', function(ev) {
    ev.preventDefault();

    // Block user interaction with the card element and form submit button
    card.update({
        'disabled': true
    });
    $("#card-button").attr('disabled', true);
    $("#loading-overlay").fadeToggle(100);

    const clientSecret = $("#id_client_secret").text().slice(1, -1);
    const csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    const subscriptionId = $("#subscription_id").text();

    customerDetails = {
        name: $.trim(form.name.value),
        phone: $.trim(form.phone_number.value),
        address: {
            city: $.trim(form.town_or_city.value),
            country: $.trim(form.country.value),
            line1: $.trim(form.address_line1.value),
            line2: $.trim(form.address_line2.value),
            postal_code: $.trim(form.postcode.value),
            state: $.trim(form.county.value)
        }
    };

    // Send the customer details to the save-customer-details view where they are added to 
    // the subscription object metadata, and if the user selected 'save-details' checked, saved 
    // to the user profile
    const saveDetails = form.save_details.checked;
    const url = '/portal/save-customer-details/';
    const postData = {
        'csrfmiddlewaretoken': csrfToken,
        'customer_details': customerDetails,
        'save_details': saveDetails,
        'subscription_id': subscriptionId,
    };
    $.post(url, postData).done(function() {
        stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: customerDetails
                }
            })
            .then(function(result) {
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
                        form.submit();
                    }
                }
            });
    }).fail(function() {
        // Error charging customer, reload the page
        location.reload();
    });
});