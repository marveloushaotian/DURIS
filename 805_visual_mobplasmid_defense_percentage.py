import pandas as pd
import matplotlib.pyplot as plt

# 1. Read the CSV file
df = pd.read_csv('Results/05_Plasmid_Enrich/mobility_defense_stats.csv')

# 2. Group by Mobility and calculate percentages
grouped = df.groupby('Mobility').agg({
    'Total': 'sum',
    'Defense': 'sum'
}).reset_index()

grouped['Offense'] = grouped['Total'] - grouped['Defense']
grouped['Defense_Percentage'] = grouped['Defense'] / grouped['Total'] * 100
grouped['Offense_Percentage'] = grouped['Offense'] / grouped['Total'] * 100

# 3. Define the desired order of mobility types
mobility_order = ['Non-mobilizable', 'Mobilizable', 'Conjugative']

# 4. Sort the dataframe based on the defined order
grouped = grouped.set_index('Mobility').loc[mobility_order].reset_index()

# 5. Create the stacked bar plot
fig, ax = plt.subplots(figsize=(7, 6))  # Increased width to accommodate legend

ax.bar(grouped['Mobility'], grouped['Defense_Percentage'], label='Defense', color='#6566aa')
ax.bar(grouped['Mobility'], grouped['Offense_Percentage'], bottom=grouped['Defense_Percentage'], label='Offense', color='#8fced1')

# 6. Customize the plot
ax.set_ylabel('Percentage of Defense (%)', fontsize=14, fontweight='bold')

# 7. Add percentage labels on the bars
for i, mobility in enumerate(grouped['Mobility']):
    defense_pct = grouped.loc[i, 'Defense_Percentage']
    offense_pct = grouped.loc[i, 'Offense_Percentage']
    ax.text(i, defense_pct/2, f'{defense_pct:.1f}%', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(i, defense_pct + offense_pct/2, f'{offense_pct:.1f}%', ha='center', va='center', fontsize=12, fontweight='bold')

# 8. Set y-axis to percentage scale
ax.set_ylim(0, 100)
ax.set_yticks(range(0, 101, 20))
ax.set_yticklabels([f'{x}' for x in range(0, 101, 20)])

# 9. Improve overall appearance
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 10. Set x-axis labels with the desired order
ax.set_xticks(range(len(mobility_order)))
ax.set_xticklabels(mobility_order, fontsize=12)

# 11. Move legend outside the plot
plt.legend(fontsize=12, bbox_to_anchor=(1.05, 1), loc='upper left')

# 12. Save the plot as PDF
plt.tight_layout()
plt.savefig('mobility_defense_offense_percentage.pdf', bbox_inches='tight')
plt.close()
