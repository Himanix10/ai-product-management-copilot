import re

import pandas as pd
import streamlit as st

from backend.database.db import fetch_roadmap_db


def normalize_quarter(value):

    if pd.isna(value):
        return ""

    text = str(value).strip().upper()

    match = re.search(
        r"(Q[1-4])",
        text
    )

    if not match:
        return text

    quarter = match.group(1)

    year_match = re.search(
        r"(20\d{2})",
        text
    )

    if year_match:
        return f"{quarter} {year_match.group(1)}"

    return quarter


def render_roadmap():

    st.title("Roadmap Planner")

    st.caption(
        "Plan quarters and track initiative execution status."
    )

    df = fetch_roadmap_db()

    if df.empty:

        st.info(
            "No roadmap records were found in the database."
        )

        return

    # Normalize database quarter values.
    df["Normalized Quarter"] = (
        df["Quarter"]
        .apply(normalize_quarter)
    )

    # Determine the year from the data.
    years = []

    for value in df["Normalized Quarter"]:

        match = re.search(
            r"(20\d{2})",
            str(value)
        )

        if match:
            years.append(
                int(match.group(1))
            )

    if years:
        selected_year = max(years)
    else:
        selected_year = 2026

    quarters = [
        f"Q1 {selected_year}",
        f"Q2 {selected_year}",
        f"Q3 {selected_year}",
        f"Q4 {selected_year}",
    ]

    cols = st.columns(4)

    for index, quarter in enumerate(quarters):

        with cols[index]:

            st.subheader(quarter)

            q_items = df[
                df["Normalized Quarter"] == quarter
            ]

            # Also support records stored only as Q1/Q2/Q3/Q4.
            if q_items.empty:

                short_quarter = quarter.split()[0]

                q_items = df[
                    df["Normalized Quarter"] ==
                    short_quarter
                ]

            if q_items.empty:

                st.info(
                    "No items scheduled"
                )

                continue

            for _, row in q_items.iterrows():

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"**{row['Initiative']}**"
                    )

                    if pd.notna(
                        row.get("Priority")
                    ):
                        st.caption(
                            f"Priority: {row['Priority']}"
                        )

                    if pd.notna(
                        row.get("Status")
                    ):
                        st.caption(
                            f"Status: {row['Status']}"
                        )

                    progress = row.get(
                        "Progress",
                        0
                    )

                    try:
                        progress = int(progress)
                    except (TypeError, ValueError):
                        progress = 0

                    progress = max(
                        0,
                        min(
                            100,
                            progress
                        )
                    )

                    st.progress(
                        progress / 100
                    )

                    st.caption(
                        f"{progress}% completed"
                    )

                    if pd.notna(
                        row.get("Milestone")
                    ):

                        st.caption(
                            f"Milestone: "
                            f"{row['Milestone']}"
                        )