import pandas as pd
import plotly.express as px
import pypsa
import streamlit as st


def extract_generation(path):
    n = pypsa.Network(path)

    df = n.generators_t.p.T.reset_index()
    # Create the dataframe

    df["Generator"] = df["Generator"].str.replace(r"^\d+\s+", "", regex=True)

    final_gen = df.groupby("Generator").sum()

    final_gen = final_gen.drop("load")

    # Filter the dataframe to select the first 100 columns
    data = final_gen.T
    return data


def get_generation():
    gen = n.generators_t.p.T.reset_index()
    gen["Generator"] = gen["Generator"].str.replace(r"^\d+\s+", "", regex=True)
    hydro = n.storage_units_t.p.T.reset_index()
    hydro["StorageUnit"] = hydro["StorageUnit"].str.replace(r"^\d+\s+", "", regex=True)
    interim_hydro = hydro.groupby("StorageUnit").sum()
    interim_gen = gen.groupby("Generator").sum().drop("load")
    final_gen = pd.concat([interim_gen, interim_hydro]).T

    return final_gen


def main(data: pd.DataFrame):
    st.title("Stacked Area Chart with Snapshot Slider")

    # Slider to select snapshot index
    start, end = st.slider(
        "Select a snapshot index", min_value=0, max_value=len(data) - 1, value=(0, 100)
    )

    # Filter data for the selected snapshot index
    filtered_data = data.iloc[start:end]

    st.dataframe(filtered_data)
    # Create a list of energy sources for stacking
    energy_sources = data.columns

    # Create a dictionary for st.stacked_area_chart

    # Create a stacked area chart using st.stacked_area_chart

    color_dict = {
        "CCGT": "#9ABBCA",
        "coal": "#000000",
        "OCTG": "#9ABBCA",
        "solar": "#FFD744",
        "onwind": "#1F82C0",
        "ror": "#79A8CA",
        "oil": "#1D565C",
        "geothermal": "#d05094",
        "hydro": "#79A8CA",
    }
    fig = px.area(
        filtered_data,
        color_discrete_map=color_dict,
    )

    for trace in fig.data:
        trace.fill = "tonexty"  # This ensures the areas are filled up to the next trace (stacked)
        trace.opacity = 1  # Set the fill opacity
    st.plotly_chart(fig, use_container_width=True)
    # st.area_chart(
    #     filtered_data,
    # )


if __name__ == "__main__":
    data = pd.read_csv("hourly_generation.csv")
    main(data)
