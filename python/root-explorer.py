# test
#
#

__all__ = []
__author__ = ["name"]
__email__ = ["email"]


import argparse

import matplotlib.pyplot as plt
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

    if args["tbranch"]:
        tbranch = args['tbranch'].split(' :: ')
        if len(tbranch) > 1:
            ttree, tbranch = tbranch
        else:
            ttree, tbranch = args['ttree'], tbranch[0]
        arr = np.array(tfile[ttree].array(tbranch))
        filename = "/tmp/root-browser-plot.png"
        hist2plot(arr, tbranch, filename)
        print(filename)
    else:
        if not args['ttree'] or args['ttree'] == '0':
            ttrees = [t.decode().split(';')[0] for t in list(tfile.keys())]
        else:
            ttrees = [args['ttree']]
        all_branches = []
        for t in ttrees:
            _branches = [k.decode() for k in tfile[t].keys()]
            all_branches.append([f"{t} :: {b}" for b in _branches])
        print("\n".join(sum(all_branches, [])))


# vim: fdm=marker ts=2 sw=2 sts=2 sr et
