import matplotlib.pyplot as plt

fig = plt.figure()
ax = plt.axes()


points_with_annotation = []
for i in range(10):
    point, = plt.plot(i, i, 'o', markersize=10)

    annotation = ax.annotate("Mouseover point %s" % i,
        xy=(i, i), xycoords='data',
        xytext=(i + 1, i), textcoords='data',
        horizontalalignment="left",
        arrowprops=dict(arrowstyle="simple",
                        connectionstyle="arc3,rad=-0.2"),
        bbox=dict(boxstyle="round", facecolor="w", 
                  edgecolor="0.5", alpha=0.9)
        )
    # by default, disable the annotation visibility
    annotation.set_visible(False)

    points_with_annotation.append([point, annotation])


def on_move(event):
    visibility_changed = False
    for point, annotation in points_with_annotation:
        should_be_visible = (point.contains(event)[0] == True)

        if should_be_visible != annotation.get_visible():
            visibility_changed = True
            annotation.set_visible(should_be_visible)

    if visibility_changed:        
        plt.draw()

on_move_id = fig.canvas.mpl_connect('motion_notify_event', on_move)

plt.show()