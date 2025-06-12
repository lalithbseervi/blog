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
                    keys: ['from', 'to'],
                    layoutAlgorithm: {
                        enableSimulation: false,
                        integration: 'verlet',
                        linkLength: 150
                    },
                    point: {
                        events: {
                            click(e) {
                                handlePointClick(e);
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
            ]
        });
    })
    .catch(error => console.error('Error fetching graph data: ', error));
})

function handlePointClick(e) {
    const url = `${window.location.protocol}//${window.location.host}/tsm/profile/${encodeURIComponent(e.point.id)}`;
    window.location.replace(url);
}