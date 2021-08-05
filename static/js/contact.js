$('#contact-form').submit(function (e) {
    e.preventDefault();
    if ($('#contact-form')[0].reportValidity()) {
        let formData = {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'name': $('#id_name').val(),
            'email': $('#id_email').val(),
            'subject': $('#id_subject').val(),
            'message': $('#id_message').val(),
        };
        $.post("/contact/", postData).done(function () {
            $('#contact-form').parent().prepend('<p class="text-center">Thank you for your message. A member of the team will be in touch shortly.</p>');
            $('#contact-form').remove();
        });
    }
});

function initMap() {
    const location = {
        lat: 53.3873753,
        lng: -2.3542039
    };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: location,
    });
    new google.maps.Marker({
        position: location,
        map: map,
    });
}