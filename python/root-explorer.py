# test
#
#

__all__ = []
__author__ = ["name"]
__email__ = ["email"]


import argparse
# import complot

import matplotlib.pyplot as plt
# import numpy as np
import uproot3 as uproot
import numpy as np

plt.rcParams["figure.figsize"] = (8, 6)


def hist2plot(arr, branch, filename):
    # remove null values
    _arr = arr[arr != -99999.]
    if len(_arr) > 0:
        lower_limit, upper_limit = np.min(_arr), np.max(_arr)
        plt.hist(_arr, 100, range=(lower_limit, upper_limit))
    plt.xlabel(branch)
    # add info
    # fig.set_size_inches(18.5, 10.5)
    plt.tight_layout()
    plt.gcf().text(0.1, 0.08+2e-2, f"Mean: {np.mean(_arr):.8e}")
    plt.gcf().text(0.1, 0.04+2e-2, f"Standard: {np.std(_arr)}")
    plt.gcf().text(0.1, 0.00+2e-2, f"Lenght: {len(_arr)}")
    plt.subplots_adjust(bottom=0.2)
    plt.savefig(filename, dpi=200, transparent=False)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--tfile")
    p.add_argument("--ttree", default=False)
    p.add_argument("--tbranch", default=False)
    args = vars(p.parse_args())

    tfile = uproot.open(args["tfile"])

    if not args['ttree'] or args['ttree'] == '0':
        ttree = list(tfile.keys())[0]
    else:
        ttree = args['ttree']

    if args["tbranch"]:
        arr = np.array(tfile[ttree].array(args["tbranch"]))
        filename = "/tmp/root-browser-plot.png"
        hist2plot(arr, args["tbranch"], filename)
        print(filename)
    else:
        arr = tfile[ttree].keys()
        print("\n".join([k.decode() for k in arr]))


# vim: fdm=marker ts=2 sw=2 sts=2 sr et