document.addEventListener('DOMContentLoaded', () => {
    fetch('api/network-data/')
    .then(response => response.json())
    .then(data => {
            Highcharts.chart('container', {
            chart: {
                type: 'networkgraph',
                style: {
                    fontSize: '115%',
                },
                height: (6 / 13 * 100) + '%',
            },

            title: {
                text: 'Network Graph'
            },

            tooltip: {
                formatter: function () {
                    return '<b>' + this.key + '</b> ' + this.point.rel_info;
                }
            },

            plotOptions: {
                networkgraph: {
                    draggable: false,
                    keys: ['from', 'to'],
                    layoutAlgorithm: {
                        enableSimulation: false,
                        integration: 'verlet',
                        linkLength: 150
                    },
                    point: {
                        events: {
                            click() {
                                collapseNode(this);
                            }
                        }
                    }
                }
            },

            series: [
                {
                    marker: {
                        radius: 13
                    },
                    dataLabels: {
                        enabled: true,
                        linkFormat: '',
                        allowOverlap: true,
                        style: {
                            textOutline: false
                        }
                    },
                    data: data.links,
                    nodes: data.nodes
                }
            ],
        });
    })
    .catch(error => console.error('Error fetching graph data: ', error));
})

document.addEventListener('contextmenu', (e) => {
    if (e.button == 2) {
        e.preventDefault();
        const url = `${window.location.protocol}//${window.location.host}/tsm/profile/${encodeURIComponent(e.target.point.id)}`;
        window.location.replace(url);
    }
});

const collapseNode = (node, visible = false) => {
    const setVisibility = (hide) => {
    const display = hide ? 'none' : 'block';
    
    node.linksFrom.forEach(link => {
      hide ? link.graphic.hide() : link.graphic.show();
      link.toNode.graphic.css({
        display: display
      });
      link.toNode.dataLabel.css({
        display: display
      });

      if (hide)
        collapseNode(link.toNode, true);
    });
    node.childNodesVisible = hide ? false : true;
  }

  if (visible)
    node.childNodesVisible = true;

  if (node.linksFrom) {
    setVisibility(node.childNodesVisible ? true : false);
  }
}