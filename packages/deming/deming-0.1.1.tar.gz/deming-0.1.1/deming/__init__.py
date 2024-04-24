import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


def control_chart(df, x, y, goal=None, title="Control Chart"):
    df["Goal"] = goal
    df["Mean"] = df[y].mean()
    df["Upper Control Limit"] = df[y].mean() + df[y].std()
    df["Lower Control Limit"] = df[y].mean() - df[y].std()

    plt.figure(figsize=(12, 6))

    plt.plot(df[x], df[y], marker="x", linestyle="-", color="r", label=y)

    if goal is not None:
        plt.plot(df[x], df["Goal"], marker="x", linestyle="-", color="g", label="Goal")

    plt.plot(df[x], df["Mean"], marker="x", linestyle="-", color="orange", label="Mean")

    plt.plot(
        df[x],
        df["Upper Control Limit"],
        marker="x",
        linestyle="-",
        color="y",
        label="Upper Control Limit",
    )

    plt.plot(
        df[x],
        df["Lower Control Limit"],
        marker="x",
        linestyle="-",
        color="y",
        label="Lower Control Limit",
    )

    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.legend()
    plt.grid(False)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


def pareto_chart(data, x, y, hue=None, palette="viridis"):
    fig, ax = plt.subplots()
    cumsum = data[y].cumsum()
    ax.bar(data[x], data[y], color="C0")
    ax2 = ax.twinx()
    ax2.plot(data[x], cumsum, color="C1", marker="D", ms=7)
    ax2.yaxis.set_major_formatter(PercentFormatter())
    ax.tick_params(axis="y", colors="C0")
    ax2.tick_params(axis="y", colors="C1")

    for tick in ax.get_xticklabels():
        tick.set_rotation(90)

    plt.show()
