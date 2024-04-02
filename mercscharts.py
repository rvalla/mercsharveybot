from io import BytesIO
import matplotlib.pyplot as plt

#The function to store the Figure object in a byte stream...
def create_image(figure):
    file = BytesIO()
    figure.savefig(file, dpi=250, format="jpeg")
    file.name = "mercsharveybot_chart.jpg"
    file.seek(0)
    return file

def lines_chart(w, h, resolution, data, error):
    f = plt.figure(num=None, figsize=(w, h), dpi=resolution, facecolor="white", edgecolor="k")
    colors = ["darkorange", "tab:blue"]
    for r in range(len(data)):
        plt.fill_between(range(1, len(data[0])+1), error[r*2], error[r*2+1], facecolor=colors[r], alpha=0.3, zorder=1)
        plt.plot(range(1, len(data[0])+1), data[r], linewidth=2.75, color=colors[r], zorder=2)
    plt.grid(which='both', axis='both')
    plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgrey", alpha=0.9)
    plt.grid(True, "major", "x", ls="-", lw=0.8, c="dimgrey", alpha=0.9)
    plt.minorticks_on()
    if len(data[0]) > 23:
        plt.xticks(range(1,len(data[0])+1,6))
    elif len(data[0]) > 11:
        plt.xticks(range(1,len(data[0])+1,3))
    else:
        plt.xticks(range(1,len(data[0])+1,1))
    plt.grid(True, "minor", "y", ls="--", lw=0.3, c="dimgray", alpha=0.7)
    plt.grid(True, "minor", "x", ls="--", lw=0.3, c="dimgray", alpha=0.7)
    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.ylim(plt.ylim()[0],0)
    return create_image(f)

    