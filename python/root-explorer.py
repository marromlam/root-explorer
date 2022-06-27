# test
#
#

__all__ = []
__author__ = ["name"]
__email__ = ["email"]


import argparse

import matplotlib.pyplot as plt
import uproot as uproot
import numpy as np

from os import listdir, remove
from os.path import isfile, join

plt.rcParams["figure.figsize"] = (8, 6)


def hist2plot(arr, color):
    # remove null values
    _arr = np.array(arr[:,0] if arr.ndim > 1 else arr)
    _arr = _arr[_arr != -99999.0]
    if len(_arr) > 0:
        lower_limit, upper_limit = np.min(_arr), np.max(_arr)
        plt.hist(_arr, 100, range=(lower_limit, upper_limit), color=color,
                 alpha=0.5)
    # add info
    # fig.set_size_inches(18.5, 10.5)
    plt.tight_layout()
    plt.gcf().text(0.1, 0.12 + 2e-2, f"Mean: {np.mean(_arr):.8e}")
    plt.gcf().text(0.1, 0.08 + 2e-2, f"Standard: {np.std(_arr)}")
    plt.gcf().text(0.1, 0.04 + 2e-2, f"Lenght: {len(_arr)}")
    plt.gcf().text(0.1, 0.00 + 2e-2, f"min, max: {min(_arr):.4e}, {max(_arr):.4e}")
    plt.subplots_adjust(bottom=0.3)
    return


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--tfile")
    p.add_argument("--ttree", default=False)
    p.add_argument("--tbranch", nargs="+", default=False)
    args = vars(p.parse_args())

    tfile = uproot.open(args["tfile"])

    if args["tbranch"]:
        label = " and ".join(args["tbranch"])
        plt.xlabel(label)
        onlyfiles = [f for f in listdir("/tmp") if isfile(join("/tmp", f))]
        for f in onlyfiles:
            if f.startswith("root-explorer"):
                remove(join("/tmp", f))
        filename = f"/tmp/root-explorer-{hash(label)}.png"
        for i, _branch in enumerate(args["tbranch"]):
            tbranch = _branch.split("::")
            if len(tbranch) > 1:
                ttree, tbranch = tbranch
            else:
                ttree, tbranch = args["ttree"], tbranch[0]
            arr = tfile[ttree].arrays(tbranch)
            hist2plot(arr[tbranch], f"C{i}")
            plt.savefig(filename, dpi=200, transparent=False)
        print(filename)
    else:
        if not args["ttree"] or args["ttree"] == "0":
            ttrees = [t.split(";")[0] for t in tfile.keys()]
        else:
            ttrees = [args["ttree"]]
        all_branches = []
        for t in ttrees:
            if "TTree" not in str(t):
                _branches = [k for k in tfile[t].keys()]
                all_branches.append([f"{t}::{b}" for b in _branches])
        all_branches = list(dict.fromkeys(sum(all_branches, [])))
        for i, b in reversed(list(enumerate(all_branches))):
            if ";" in b:
                all_branches.pop(i)
        print("\n".join(all_branches))


# vim: fdm=marker ts=2 sw=2 sts=2 sr et
