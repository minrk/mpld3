"""
Draggable Points Example
========================
This example shows how a D3 plugin can be created to make plot elements
draggable.  A stopPropagation command is used to allow the drag behavior
and pan/zoom behavior to work in tandem.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

import mpld3
from mpld3 import plugins, utils


class DragPlugin(plugins.PluginBase):
    JAVASCRIPT = r"""
    var DragPlugin = function(fig, prop){
      this.fig = fig;
      this.prop = mpld3.process_props(this, prop, {}, ["id"]);

      mpld3.insert_css("#" + fig.figid + " path.dragging",
                       {"fill-opacity": "1.0 !important",
                        "stroke-opacity": "1.0 !important"});
    }

    DragPlugin.prototype.draw = function(){
        var obj = mpld3.get_element(this.prop.id);

        var drag = d3.behavior.drag()
            .origin(function(d) { return {x:obj.ax.x(d[0]),
                                          y:obj.ax.y(d[1])}; })
            .on("dragstart", dragstarted)
            .on("drag", dragged)
            .on("dragend", dragended);

        obj.elements()
           .data(obj.data)
           .style("cursor", "default")
           .call(drag);

        function dragstarted(d) {
          d3.event.sourceEvent.stopPropagation();
          d3.select(this).classed("dragging", true);
        }

        function dragged(d, i) {
          d[0] = obj.ax.x.invert(d3.event.x);
          d[1] = obj.ax.y.invert(d3.event.y);
          d3.select(this)
            .attr("transform", "translate(" + [d3.event.x,d3.event.y] + ")");
        }

        function dragended(d) {
          d3.select(this).classed("dragging", false);
        }
    }

    mpld3.register_plugin("drag", DragPlugin);
    """

    def __init__(self, points):
        if isinstance(points, mpl.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None

        self.dict_ = {"type": "drag",
                      "id": utils.get_id(points, suffix)}


fig, ax = plt.subplots()
np.random.seed(0)
points = ax.plot(np.random.normal(size=20),
                 np.random.normal(size=20), 'or', alpha=0.5,
                 markersize=50, markeredgewidth=1)
ax.set_title("Click and Drag", fontsize=18)

plugins.connect(fig, DragPlugin(points[0]))

mpld3.show()
