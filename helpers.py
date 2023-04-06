# helper to apply to data to assign region
def helper_assign_region(data, row):
    # divide countries by continent/region
    all_countries = data["country"].unique()
    all_countries.sort()
    OCEANIA = ["Australia", "New Zealand"]
    AMERICA = ["Argentina", "Barbados", "Bolivia", "Brazil", "Canada", "Chile",
               "Colombia", "Costa Rica" , "Cuba", "Curacao", "Dominican Republic",
               "El Salvador", "Grenada", "Guatemala", "Ecuador", "Guyana", "Haiti",
               "Honduras", "Jamaica", "Mexico", "Montserrat", "Panama", "Paraguay",
               "Peru", "Puerto Rico", "Saint Kitts and Nevis", "Suriname", "Trinidad and Tobago",
               "United States", "Uruguay", "Venezuela"
              ]
    ASIA = ["Armenia", "Azerbaijan", "China PR", "Cyprus", "Hong Kong", "India", "Indonesia",
            "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan", "Korea DPR",
            "Korea Republic", "Malaysia", "Nepal", "Palestine", "Philippines", "Saudi Arabia",
            "Thailand", "United Arab Emirates", "Uzbekistan"
           ]
    AFRICA = ["Algeria", "Angola", "Benin", "Burkina Faso", "Burundi", "Cameroon",
             "Cape Verde Islands", "Central African Republic", "Comoros", "Congo",
              "Congo DR", "Côte d'Ivoire", "Egypt", "Equatorial Guinea", "Gabon", 
              "Gambia", "Ghana", "Guinea", "Guinea Bissau", "Kenya", "Liberia",
              "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Morocco",
              "Mozambique", "Namibia", "Niger", "Nigeria", "Senegal", "Sierra Leone",
              "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia",
              "Uganda", "Zambia", "Zimbabwe"
             ]
    EUROPE = sorted(list(set(all_countries) - set(OCEANIA) - set(AMERICA) - set(ASIA) - set(AFRICA)))
    # check size equiavalent to guarantee partition correct
    assert(len(OCEANIA) + len(AMERICA) + len(ASIA) + len(AFRICA) + len(EUROPE) == len(all_countries))
    
    country = row["country"]
    if country in OCEANIA:
        return "Oceania"
    if country in AMERICA:
        return "America"
    if country in ASIA:
        return "Asia"
    if country in AFRICA:
        return "Africa"
    return "Europe"


def preprocessing(data):
    # Apply the function with the original data
    data["region"] = data.apply(lambda row: helper_assign_region(data, row), axis=1)
    # select subset of columns of interests
    columns_interests = ["name", "country", "region", "age", "overall", "potential", 
                         "preferred_foot", "skill_move", "height", "wage", "dribbling",
                         "ball_control", "sprint_speed", "strength", "shot_power", "stamina",
                         "aggression"
                        ]
    # assign to new variable
    fifa_subset = data[columns_interests]
    return fifa_subset