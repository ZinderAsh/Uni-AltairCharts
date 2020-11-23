import pandas as pd
import altair as alt
from flask import Flask, render_template, request

"""
List of all counties with their respective csv file names.
"""
counties = {
    "all": "alle_fylker",
    "agder": "agder",
    "innlandet": "innlandet",
    "møre og romsdal": "more_og_romsdal",
    "nordland": "nordland",
    "oslo": "oslo",
    "rogaland": "rogaland",
    "troms og finnmark": "troms_og_finnmark",
    "trøndelag": "trondelag",
    "vestfold og telemark": "vestfold_og_telemark",
    "vestland": "vestland",
    "viken": "viken"
}

def get_county_file(county):
    """
    Gets the filename for a csv file of corona statistic for a given county.
    Args:
        county (string): Name of the county, case-insensitive.
    Returns:
        (string): The filename of the county's data.
    """
    f = counties.get(county.lower(), None)
    if not f:
        print("Invalid county passed as argument.")
        exit(-1)
    return "reports/%s.csv" % f

def make_dataframe(county="all", fromdate=None, todate=None):
    """
    Creates a pandas dataframe on corona statistics based on county and min/max dates.
    Args:
        [county] (string): The county to use data from. Default: All counties
        [fromdate] (string): The date to start data from in the format YYYY-MM-DD. Default: Start of statistics
        [todate] (string): The date to end data at in the format YYYY-MM-DD. Default: End of statistics
    Returns:
        (Dataframe): Pandas dataframe with the requested data.
    """
    csv_file = get_county_file(county)
    df = pd.read_csv(csv_file)
    if fromdate:
        df = df[df["Prøvetakingsdato"] >= fromdate]
    if todate:
        df = df[df["Prøvetakingsdato"] <= todate]
    return df

def plot_reported_cases(county="all", fromdate=None, todate=None):
    """
    Creates an altair chart on corona statistics by new reported cases based on county and min/max dates.
    Args:
        [county] (string): The county to use data from. Default: All counties
        [fromdate] (string): The date to start data from in the format YYYY-MM-DD. Default: Start of statistics
        [todate] (string): The date to end data at in the format YYYY-MM-DD. Default: End of statistics
    Returns:
        (Chart): Altair bar-chart with the requested data.
    """
    df = make_dataframe(county, fromdate, todate)
    chart = alt.Chart(df).mark_bar().encode(
        y="Nye tilfeller:Q",
        x="Prøvetakingsdato:T",
        tooltip=["Prøvetakingsdato:T", "Nye tilfeller:Q", "Kumulativt antall:Q"]
    )
    return chart

def plot_cumulative_cases(county="all", fromdate=None, todate=None):
    """
    Creates an altair chart on corona statistics by cumulative cases based on county and min/max dates.
    Args:
        [county] (string): The county to use data from. Default: All counties
        [fromdate] (string): The date to start data from in the format YYYY-MM-DD. Default: Start of statistics
        [todate] (string): The date to end data at in the format YYYY-MM-DD. Default: End of statistics
    Returns:
        (Chart): Altair line-chart with the requested data.
    """
    df = make_dataframe(county, fromdate, todate)
    chart = alt.Chart(df).mark_line().encode(
        y="Kumulativt antall:Q",
        x="Prøvetakingsdato:T",
        tooltip=["Prøvetakingsdato:T", "Nye tilfeller:Q", "Kumulativt antall:Q"]
    )
    return chart

def plot_both(county="all", fromdate=None, todate=None):
    """
    Creates an altair chart on corona statistics by cumulative and reported cases based on county and min/max dates.
    Args:
        [county] (string): The county to use data from. Default: All counties
        [fromdate] (string): The date to start data from in the format YYYY-MM-DD. Default: Start of statistics
        [todate] (string): The date to end data at in the format YYYY-MM-DD. Default: End of statistics
    Returns:
        (Chart): Layered altair bar & line-chart with the requested data.
    """
    reported = plot_reported_cases(county, fromdate, todate).encode(
        opacity=alt.value(0.4)
    )
    cumulative = plot_cumulative_cases(county, fromdate, todate).encode(
        color=alt.value('#E43E0C')
    )
    chart = alt.layer(reported, cumulative).resolve_scale(
        y="independent"
    )
    return chart

def main():
    """
    Starts the Flask web page to view corona statistics.
    """
    app = Flask(__name__)

    @app.route("/")
    def plot_stats():
        """
        Flask method to load the base web page with a chart of all counties.
        """
        return render_template("template.html", counties=counties)

    @app.route("/<chart>/<county>")
    def get_both_chart(chart="both", county="all"):
        """
        Flask method to fetch the json for a requested chart filtered by county.
        Returns:
            (string) The chart in json format.
        """
        if chart == "cumulative":
            return plot_cumulative_cases(county=county).to_json()
        elif chart == "reported":
            return plot_reported_cases(county=county).to_json()
        else:
            return plot_both(county=county).to_json()

    @app.route("/help")
    def help_page():
        """
        Flask method to load the help page.
        """
        return render_template("help_page.html")

    app.run(debug=True)

if __name__ == "__main__":
    main()