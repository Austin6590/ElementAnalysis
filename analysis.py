from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

data_path = Path(__file__).parent / "data" / "elements.csv"
elements = pd.read_csv(data_path)

print(elements.head())
print("Dataset dimensions:", elements.shape)

columns_to_view = ["number", "name", "symbol", "category"]

print(elements[columns_to_view].head())
print(elements[columns_to_view].tail())

confirmed_elements = elements[elements["number"].between(1, 118)].copy()

print("Confirmed-element dataset:", confirmed_elements.shape)

gold = confirmed_elements[confirmed_elements["symbol"] == "Ag"]

print(gold[["number", "name", "symbol", "atomic_mass", "category"]])

properties = ["atomic_mass", "density", "melt", "boil"]

missing_values = confirmed_elements[properties].isna().sum()

print("\nMissing values by property:")
print(missing_values)

missing_density = confirmed_elements[
    confirmed_elements["density"].isna()
]

print(missing_density[["number", "name", "symbol", "density"]])

print("\nElements by phase:")
print(confirmed_elements["phase"].value_counts(dropna=False))

# Preserve the original density and create a standardized column.
confirmed_elements["density_g_cm3"] = confirmed_elements["density"]

# Identify gas rows.
gas_rows = confirmed_elements["phase"] == "Gas"

# Convert only the gas densities from g/L to g/cm³.
confirmed_elements.loc[gas_rows, "density_g_cm3"] = (
    confirmed_elements.loc[gas_rows, "density"] / 1000
)

print(
    confirmed_elements.loc[
        gas_rows, ["name", "density", "density_g_cm3"]
    ].head()
)

densest_elements = confirmed_elements.nlargest(10, "density_g_cm3")

print(
    densest_elements[
        ["name", "symbol", "phase", "density_g_cm3"]
    ]
)

fig, ax = plt.subplots()

ax.scatter(
    confirmed_elements["number"],
    confirmed_elements["atomic_mass"],
    s=20
)

ax.set_title("Atomic Mass Across the Periodic Table")
ax.set_xlabel("Atomic number")
ax.set_ylabel("Atomic mass (u)")

figures_path = Path(__file__).parent / "figures"
figures_path.mkdir(exist_ok=True)

fig.savefig(
    figures_path / "atomic_mass_vs_atomic_number.png",
    dpi=300,
    bbox_inches="tight"
)

plt.tight_layout()

comparison_symbols = ["Cu", "Ag", "Au"]

comparison = confirmed_elements[
    confirmed_elements["symbol"].isin(comparison_symbols)
]



fig_density, ax_density = plt.subplots()

ax_density.bar(
    comparison["name"],
    comparison["density_g_cm3"],
    color=["#B87333", "#C0C0C0", "#D4AF37"]
)

ax_density.set_title("Density Comparison: Copper, Silver, and Gold")
ax_density.set_ylabel("Density (g/cm³)")

fig_density.tight_layout()
fig_density.savefig(
    figures_path / "copper_silver_gold_density.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

missing_counts = confirmed_elements[properties].isna().sum()

fig_missing, ax_missing = plt.subplots()

ax_missing.bar(
    ["Atomic mass", "Density", "Melting point", "Boiling point"],
    missing_counts,
    color="steelblue"
)

ax_missing.set_title("Missing Property Values Across 118 Elements")
ax_missing.set_ylabel("Number of elements")

fig_missing.tight_layout()
fig_missing.savefig(
    figures_path / "missing_property_values.png",
    dpi=300,
    bbox_inches="tight"
)

comparison_symbols = ["Cu", "Ag", "Au"]

comparison = confirmed_elements[
    confirmed_elements["symbol"].isin(comparison_symbols)
]

print(comparison[["name", "symbol", "density_g_cm3"]])

output_path = (
    Path(__file__).parent / "data" / "elements_prepared.csv"
)

confirmed_elements.to_csv(output_path, index=False)

print(f"Prepared dataset saved to: {output_path}")