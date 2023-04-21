import pandas as pd
df=pd.read_excel('Medals_List.xlsx',sheet_name=None)

print("_______________________________")
df_all = pd.concat (df.values(),ignore_index=True)
obtained_Medals = df_all.loc[df_all['Obtained']==0]


dfmedals = obtained_Medals['Acquirement Method 1']


#produces list of medal locations with count of how many to obtain
df_Medals_groups=obtained_Medals.groupby("Acquirement Method 1")
print(df_Medals_groups.sum())
