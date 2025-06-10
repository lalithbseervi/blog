// let network_data = fetch('api/network-data/')
//   .then(response => response.json())
//   .then(data => {
//     console.log(`nodes: ${data.nodes}`);
//     console.log(`links: ${data.links}`);
    
//     let nodes = data.nodes;
//     let links = data.links;
//   })
//   .catch(error => console.error('Error fetching graph data:', error));

// console.log(`nodes: ${network_data.nodes}`);
// console.log(`links: ${network_data.links}`);

document.addEventListener('DOMContentLoaded', () => {
    fetch('api/network-data/')
    .then(response => response.json())
    .then(data => {
            Highcharts.chart('container', {
            chart: {
                type: 'networkgraph',
                marginTop: 80
            },

            title: {
                text: 'Network Graph - Lalith B Seervi'
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
                        linkLength: 100
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
    .catch(error => console.error('Error fetching graph data:', error));
})

function handlePointClick(e) {
    const url = `${window.location.protocol}//${window.location.host}/tsm/profile?id=${encodeURIComponent(e.point.id)}`;
    window.location.replace(url);
}