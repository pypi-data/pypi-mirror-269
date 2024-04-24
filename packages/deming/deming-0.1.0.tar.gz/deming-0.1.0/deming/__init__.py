import matplotlib.pyplot as plt


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
