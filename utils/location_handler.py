import pycountry


def location_setter(country_name):
    input_val = country_name.strip()

    country_obj = None
    if len(input_val) == 2:   # alpha_2
        country_obj = pycountry.countries.get(alpha_2=input_val.upper())
    elif len(input_val) == 3:  # alpha_3
        country_obj = pycountry.countries.get(alpha_3=input_val.upper())

    if country_obj:
        country_name = getattr(country_obj, "official_name", country_obj.name)
        return country_name
    else:
        country_name = input_val.title()
        return country_name
