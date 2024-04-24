import matplotlib as mpl
import matplotlib.pyplot as plt


crimson_dict = {
    "red": [
        [0.0, 1.0, 1.0],
        [1.0, 163 / 256, 1.0],
    ],
    "green": [
        [0.0, 1.0, 1.0],
        [1.0, 38 / 256, 1.0],
    ],
    "blue": [
        [0.0, 1.0, 1.0],
        [1.0, 56 / 256, 1.0],
    ],
}

cerulean_dict = {
    "red": [
        [0.0, 1.0, 1.0],
        [1.0, 38 / 256, 1.0],
    ],
    "green": [
        [0.0, 1.0, 1.0],
        [1.0, 84 / 256, 1.0],
    ],
    "blue": [
        [0.0, 1.0, 1.0],
        [1.0, 124 / 256, 1.0],
    ],
}

kellygreen_dict = {
    "red": [
        [0.0, 1.0, 1.0],
        [1.0, 86 / 256, 1.0],
    ],
    "green": [
        [0.0, 1.0, 1.0],
        [1.0, 170 / 256, 1.0],
    ],
    "blue": [
        [0.0, 1.0, 1.0],
        [1.0, 28 / 256, 1.0],
    ],
}

flame_dict = {
    "red": [
        [0.0, 1.0, 1.0],
        [1.0, 233 / 256, 1.0],
    ],
    "green": [
        [0.0, 1.0, 1.0],
        [1.0, 109 / 256, 1.0],
    ],
    "blue": [
        [0.0, 1.0, 1.0],
        [1.0, 7 / 256, 1.0],
    ],
}

drab_dict = {
    "red": [
        [0.0, 1.0, 1.0],
        [1.0, 169 / 256, 1.0],
    ],
    "green": [
        [0.0, 1.0, 1.0],
        [1.0, 162 / 256, 1.0],
    ],
    "blue": [
        [0.0, 1.0, 1.0],
        [1.0, 141 / 256, 1.0],
    ],
}

CRIMSON = (163 / 256, 38 / 256, 56 / 256)
CERULEAN = (38 / 256, 84 / 256, 124 / 256)
KELLYGREEN = (86 / 256, 170 / 256, 28 / 256)
FLAME = (233 / 256, 109 / 256, 7 / 256)
DRAB = (169 / 256, 162 / 256, 141 / 256)

crimson_cm = mpl.colors.LinearSegmentedColormap("crimson", crimson_dict)
cerulean_cm = mpl.colors.LinearSegmentedColormap("cerulean", cerulean_dict)
kellygreen_cm = mpl.colors.LinearSegmentedColormap("kellygreen", kellygreen_dict)
flame_cm = mpl.colors.LinearSegmentedColormap("flame", flame_dict)
drab_cm = mpl.colors.LinearSegmentedColormap("drab", drab_dict)


if __name__ == "__main__":
    fig, ax = plt.subplots(layout="constrained")

    fig.colorbar(
        mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(0, 1), cmap=flame_cm),
        ax=ax,
        orientation="vertical",
        label="a colorbar label",
    )

    plt.show()
