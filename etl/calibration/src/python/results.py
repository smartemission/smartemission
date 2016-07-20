from os import path
from time import mktime, gmtime

import matplotlib.pyplot as plt


def save_fit_plot(x, y, fit, folder):
    predicted = fit.predict(x)
    fig, ax = plt.subplots()
    ax.scatter(y, predicted)
    ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
    ax.set_xlabel('Measured')
    ax.set_ylabel('Predicted')
    ax.text(y.min(), y.max() - (y.max() - y.min()) * .2, str(fit))
    plt.savefig(path.join(folder, 'scatter_%s.pdf' % str(mktime(gmtime()))))