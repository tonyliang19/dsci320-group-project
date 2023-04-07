import altair as alt
import pandas as pd

def get_data(data_path, preprocess=False):
    data = pd.read_csv(data_path)
    if preprocess is True:
        fifa_subset = preprocessing(data)
        # store to data
        data = fifa_subset
    return data

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


# helper to generate task five viz
def task_five_viz(data):
    # slider
    brush = alt.selection_interval(
        encodings=["x"],
        resolve="intersect"
    )

    # histogram for height and overall
    base_hist = alt.Chart(data).mark_bar().encode(
        x = alt.X(alt.repeat("row"), type="quantitative",
                  bin=alt.Bin(maxbins=100, minstep=1)
                 ),
        y = alt.Y('count():Q', title=None)

    )
    # adding these by layers and render it
    ovr_height_hist = alt.layer(
        base_hist.add_selection(brush).encode(
            color=alt.value('lightgrey')
        ),
        base_hist.transform_filter(brush)
    ).properties(
        width=900,
        height=100
    ).repeat(
        row=['overall', 'height'],
        data=subset
    ).configure_view(
        stroke='transparent' # no outline
    )
    return ovr_height_hist