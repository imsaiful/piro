
from math import pi, cos

from numpy.core.multiarray import arange

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from django.http import HttpResponse
from matplotlib import pylab
from pylab import *
import PIL, PIL.Image

def index(request):
    print("hello graph")
    # Construct the graph
    x = arange(0, 2*pi, 0.01)
    s = cos(x)**2
    plot(x, s)

    xlabel('xlabel(X)')
    ylabel('ylabel(Y)')
    title('Simple Graph!')
    grid(True)

    # Store image in a string buffer
    buffer = StringIO.StringIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    pilImage = PIL.Image.fromstring("RGB", canvas.get_width_height(), canvas.tostring_rgb())
    pilImage.save(buffer, "PNG")
    pylab.close()

    # Send buffer in a http response the the browser with the mime type image/png set
    return HttpResponse(buffer.getvalue(), mimetype="image/png")

