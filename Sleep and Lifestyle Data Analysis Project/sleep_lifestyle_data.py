
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Sleep Analytics: Insights from Lifestyle Data", layout="wide")

df = pd.read_csv('Sleep_health_and_lifestyle_dataset.csv',index_col="Person ID")

st.title(":zzz: Insights from Sleep and Lifestyle Data")

#Dataset reference:  https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset
st.info("The following dataset includes data on each individual with a Person ID. Columns of "
         "data provide information on each individual's gender, age, occupation, sleep duration (hours), "
         "quality of sleep (scale: 1-10), physical activity level (minutes/day), stress level (scale 1-10), "
         "BMI category, blood pressure, heart rate (bpm), daily steps, and sleep disorder (None, insomnia, sleep apnea). ")
st.dataframe(df)
st.caption("Dataset: Sleep Health and Lifestyle data from Kaggle")

st.subheader("Age vs. Hours of Sleep")

#Creates a dataframe based on filtered revenue using slider
min_sleep = df["Sleep Duration"].min()
max_sleep = df["Sleep Duration"].max()
average_sleep = df["Sleep Duration"].mean()


st.info("The scatterplot highlights the correlation between an individual's age "
         "and number of hours of sleep. There is a strong, positive correlation between "
         "age and hours of sleep amongst individuals who are 50 and older. Individuals "
         "who are older than 50 tend get 8 or more hours of sleep. In contrast, individuals "
         "who are between the ages of 25-45 tend to between 6-8 hours of sleep with more individuals "
         "getting around 6-7.5 hours of sleep. ")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Maximum number of hours of sleep of individual in dataset", value=max_sleep)

with col2:
    st.metric(label="Minimum number of hours of sleep of individual in dataset", value=min_sleep)

with col3:
    st.metric(label="Average hours of sleep", value=round(average_sleep,1))


sleep_range = st.slider(
    "Select hours of sleep range:",
    min_value = min_sleep,
    max_value = max_sleep,
    value=(min_sleep, max_sleep),
)

#[DA5] - Filter data by two or more conditions
filtered_rev_df = df[(df["Sleep Duration"] >= sleep_range[0]) & (df["Sleep Duration"] <= sleep_range[1])]

#[VIZ3] - Scatter plot
plt.figure(figsize=(10, 4))
plt.scatter(filtered_rev_df['Sleep Duration'], filtered_rev_df['Age'])
plt.xlabel('Sleep Duration')
plt.ylabel('Age')
plt.title('Sleep Duration vs. Age')
plt.grid(True)
plt.show()
st.pyplot(plt)


st.subheader("Sleep Duration vs. Quality of Sleep")
st.info("The line chart compares each individual's sleep duration to his/her reported "
        "quality of sleep on a scale from 1-10. It highlights how some individuals got "
        "many hours of sleep, but did not get good quality sleep. ")

df_top_200 = df.sort_values("Person ID").head(200)
chart_data = pd.DataFrame(df, columns=["Sleep Duration", "Quality of Sleep", "Person ID"])
chart_data["Sleep Duration"] = pd.to_numeric(chart_data["Sleep Duration"])
chart_data["Quality of Sleep"] = pd.to_numeric(chart_data["Quality of Sleep"])
chart_data["Person ID"] = pd.to_numeric(chart_data["Person ID"])

#[VIZ2] - Line chart
#Displays the line chart
st.line_chart(chart_data, x="Sleep Duration", y=["Quality of Sleep"])


st.subheader("Data by Occupation")
st.info("The data tables show the different occupations, the number of people in the original data set "
         "with that occupation, and the average sleep duration of people with certain occupations. ")

acol1, acol2 = st.columns(2)

with acol1:
    if "Occupation" in df.columns:
        occupation_names = [occupation for occupation in df["Occupation"]]  # Uses list comprehension to extract city names
        occupation_counts = {occupation: occupation_names.count(occupation) for occupation in set(occupation_names)}
        occupation_counts_df = pd.DataFrame(occupation_counts.items(), columns=["Occupation", "Individuals"]).sort_values(
            by="Individuals", ascending=False)

        st.dataframe(occupation_counts_df)

with acol2:
    results = []
    unique_occupations = df["Occupation"].unique()

    #Loop through each occupation and calculate the average sleep duration
    for occupation in unique_occupations:
        avg_sleep = df[df["Occupation"] == occupation]["Sleep Duration"].mean()
        results.append({"Occupation": occupation, "Avg Sleep Duration": round(avg_sleep,2)})

    avg_sleep_df = pd.DataFrame(results)
    avg_sleep_df_sorted = avg_sleep_df.sort_values(by="Avg Sleep Duration", ascending=False)
    st.dataframe(avg_sleep_df_sorted)


