let autocomplete;
let address1Field;
let address2Field;

function initAutocomplete() {
    address1Field = document.getElementById("id_address_line_1");
    address2Field = document.getElementById("id_address_line_2");
    autocomplete = new google.maps.places.Autocomplete(address1Field, {
        componentRestrictions: {
            country: ["gb"]
        },
        fields: ["address_components", "geometry"],
        types: ["address"],
    });
    address1Field.focus();
    autocomplete.addListener("place_changed", fillInAddress);
}

function fillInAddress() {
    const place = autocomplete.getPlace();
    let address1 = "";
    let address2 = "";
    console.log(place.address_components)

    for (const component of place.address_components) {
        const componentType = component.types[0];

        switch (componentType) {
            case "street_number": {
                address1 = `${component.long_name} ${address1}`;
                break;
            }

            case "route": {
                address1 += component.short_name;
                break;
            }

            case 'sublocality_level_1': {
                address2 = component.long_name;
                break;
            }

            case 'locality': {
                if (!address2) {
                    address2 = component.long_name;
                }
                break;
            }

            case 'postal_town': {
                $('#id_town_or_city').val(component.long_name);
                break;
            }

            case 'administrative_area_level_2': {
                $('#id_county').val(component.long_name);
                break;
            }

            case "country": {
                $(`#id_country option[value=${component.short_name}]`).prop('selected', true);
                break;
            }

            case "postal_code": {
                $('#id_postcode').val(`${component.long_name}`);
                break;
            }
        }
    }
    address1Field.value = address1;
    address2Field.value = address2;
    address2Field.focus();
}