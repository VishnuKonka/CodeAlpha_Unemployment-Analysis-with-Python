import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

DATA_FILE = "Unemployment in India.csv"


def load_dataset(path=DATA_FILE):
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Dataset not found. Place '{path}' in the same folder as this script."
        )
    df.columns = df.columns.str.strip()
    return df


def clean_dataset(df):
    df = df.dropna()
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.month_name()
    df = df.rename(columns={
        "Estimated Unemployment Rate (%)": "Unemployment_Rate",
        "Estimated Employed": "Employed",
        "Estimated Labour Participation Rate (%)": "Labour_Rate",
    })
    return df


def print_summary(df):
    print("=" * 60)
    print("UNEMPLOYMENT ANALYSIS PROJECT")
    print("=" * 60)
    print("Columns:", list(df.columns))
    print("Shape:", df.shape)
    print("\nFirst five rows:")
    print(df.head())
    print("\nMissing values:")
    print(df.isnull().sum())
    print("\nSummary statistics:")
    print(df.describe())


def print_top_extremes(df, n=10):
    print("\nTop records by unemployment rate:")
    print(df.sort_values("Unemployment_Rate", ascending=False).head(n)[[
        "Region", "Date", "Area", "Unemployment_Rate", "Employed", "Labour_Rate"
    ]])


def plot_average_unemployment_by_region(df):
    state_data = df.groupby("Region")["Unemployment_Rate"].mean().sort_values()
    plt.figure(figsize=(14, 10))
    state_data.plot(kind="barh", color="#2E86AB")
    plt.title("Average Unemployment Rate by Region")
    plt.xlabel("Unemployment Rate (%)")
    plt.tight_layout()
    plt.savefig("average_unemployment_by_region.png")
    plt.show()
    plt.close()


def plot_monthly_trend(df):
    monthly = df.groupby("Date")["Unemployment_Rate"].mean()
    plt.figure(figsize=(14, 6))
    plt.plot(monthly.index, monthly.values, marker="o", linestyle="-", color="#D35400")
    plt.title("Monthly Unemployment Rate Trend")
    plt.xlabel("Date")
    plt.ylabel("Unemployment Rate (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("monthly_unemployment_trend.png")
    plt.show()
    plt.close()


def plot_yearly_trend(df):
    yearly = df.groupby("Year")["Unemployment_Rate"].mean()
    plt.figure(figsize=(10, 5))
    yearly.plot(kind="bar", color="#117A65")
    plt.title("Average Yearly Unemployment Rate")
    plt.xlabel("Year")
    plt.ylabel("Unemployment Rate (%)")
    plt.tight_layout()
    plt.savefig("yearly_unemployment_trend.png")
    plt.show()
    plt.close()


def print_covid_impact(df):
    print("\n" + "=" * 60)
    print("COVID IMPACT ANALYSIS")
    print("=" * 60)
    before_covid = df[df["Date"] < "2020-03-01"]
    after_covid = df[df["Date"] >= "2020-03-01"]
    before_avg = before_covid["Unemployment_Rate"].mean()
    after_avg = after_covid["Unemployment_Rate"].mean()
    print(f"Average unemployment before Covid: {before_avg:.2f}%")
    print(f"Average unemployment after Covid:  {after_avg:.2f}%")
    print(f"Change in average unemployment: {after_avg - before_avg:+.2f}%")


def print_area_comparison(df):
    if "Area" in df.columns:
        print("\nAverage unemployment by Area:")
        print(df.groupby("Area")["Unemployment_Rate"].mean())


def main():
    df = load_dataset()
    df = clean_dataset(df)
    print_summary(df)
    print_top_extremes(df, n=10)
    print_area_comparison(df)
    plot_average_unemployment_by_region(df)
    plot_monthly_trend(df)
    plot_yearly_trend(df)
    print_covid_impact(df)


if __name__ == "__main__":
    main()
# HEATMAP
# ==================================================

plt.figure(figsize=(12,8))

pivot=df.pivot_table(

values='Unemployment_Rate',

index='Region',

columns='Year'

)

sns.heatmap(
pivot,
cmap='YlOrRd'
)

plt.title(
"Regional Unemployment Heatmap"
)

plt.savefig(
"heatmap.png"
)

plt.show()


# ==================================================
# INSIGHTS
# ==================================================

print("\n")
print("="*60)
print("KEY INSIGHTS")
print("="*60)

if after_avg > before_avg:

    print(
"\n1. Covid-19 caused a rise in unemployment."
)

else:

    print(
"\n1. Covid impact appears minimal."
)

print(
"\n2. Some states consistently show higher unemployment."
)

print(
"\n3. Monthly trend reveals fluctuations and possible seasonal patterns."
)

print(
"\n4. Policy focus can target vulnerable regions."
)

print(
"\n5. Employment schemes can be designed during high unemployment periods."
)

print(
"\n6. Skill development programs may reduce unemployment."
)

print(
"\nGraphs saved successfully."
)

print("\nProject Completed")
