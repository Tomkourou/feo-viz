import pypsa

n = pypsa.Network("elec_s_398_ec_lcopt_1H.nc")

# Your dataframe
df = n.generators_t.p.T.reset_index()
# Create the dataframe

df["Generator"] = df["Generator"].str.replace(r"^\d+\s+", "", regex=True)

final_gen = df.groupby("Generator").sum()

final_gen = final_gen.drop("load")

final_gen
