import matplotlib.pyplot as plt
import json
import numpy as np

with open('lingling40hrs_data.json', 'r') as data_f:
    sub_data = json.load(data_f)


flair_points = {}
flair_posts = {}
flair_posts_ind = {}

link_flair_posts = {}
link_flair_points = {}

for user, data in sub_data.items():
    if data['flair'] not in flair_points:
        flair_points[data['flair']] = 0
        flair_posts[data['flair']] = 0
        flair_posts_ind[data['flair']] = []

    for sub_id, submission in data['submissions'].items():
        flair_posts[data['flair']] += 1
        flair_points[data['flair']] += submission['score']
        flair_posts_ind[data['flair']].append(submission['score'])

        if submission['link_flair_text'] not in link_flair_posts:
            link_flair_posts[submission['link_flair_text']] = 0
            link_flair_points[submission['link_flair_text']] = 0

        link_flair_posts[submission['link_flair_text']] += 1
        link_flair_points[submission['link_flair_text']] += submission['score']



box_data = [item for item in flair_posts_ind.values()]
labels = [label.strip() for label in flair_posts_ind.keys()]
labels[1] = 'Unflaired'


fig, axes = plt.subplots()

bplot = axes.boxplot(box_data,
                     labels=labels,
                     patch_artist=True)

axes.tick_params(axis='both', labelsize=15)

cmap = plt.cm.ScalarMappable(cmap='rainbow')
colors = np.arange(len(box_data))
colors = colors/len(box_data)
for patch, color in zip(bplot['boxes'], cmap.to_rgba(colors)):
    patch.set_facecolor(color)

plt.xticks(rotation=90)
plt.ylabel('Karma', fontsize=20)

plt.show()