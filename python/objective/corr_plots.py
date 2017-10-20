import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt


corrs = pd.read_csv('./data/correlations.csv')

print(corrs.groupby(['experiment', 'metric', 'corr_type']).median())

fig, ax = plt.subplots(figsize=(3.39, 3.39))

red, blue = sb.xkcd_rgb["pale red"], sb.xkcd_rgb["denim blue"]

sb.boxplot(y='metric', x='corr', hue='experiment',
           order=['SAR', 'APS', 'TPS', 'SIR', 'IPS'],
           dodge=False,
           data=corrs.query("corr_type == 'spearman'"),
           whis=0,
           fliersize=0,
           ax=ax,
           )

# iterate over boxes
for i,box in enumerate(ax.artists):
    box.set_edgecolor('black')
    box.set_facecolor('white')

# Add some small jitter
corrs['corr'] += np.random.uniform(-0.01, 0.01, size=len(corrs))

sb.swarmplot(y='metric', x='corr',
             data=corrs.query("corr_type == 'spearman' & experiment == 'quality'"),
             order=['SAR', 'APS', 'TPS', 'SIR', 'IPS'],
             size=4,
             dodge=True,
             marker='o',
             ax=ax,
             color=red,
             label='Quality',
             )

sb.swarmplot(y='metric', x='corr',
             data=corrs.query("corr_type == 'spearman' & experiment == 'interferer'"),
             order=['SAR', 'APS', 'TPS', 'SIR', 'IPS'],
             size=4,
             dodge=True,
             marker='X',
             ax=ax,
             color=blue,
             label='Interference',
             )


handles, labels = ax.get_legend_handles_labels()
handles = [handles[2], handles[7]]
labels = [labels[2], labels[7]]
ax.legend(handles, labels, loc=(0.2, 0.99), ncol=2)

plt.ylabel('')
plt.xlabel('Spearman correlation')
sb.despine(left=True)
plt.tight_layout()
plt.savefig('./paper/images/spearman_boxplot.png', dpi=300)
plt.show()