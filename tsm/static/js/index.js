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
                    let info = '';
                    switch (this.rel) {
                        case 'self':
                            info = 'is you';
                            break;
                        case 'brother':
                            info = 'is your brother';
                            break;
                        case 'father':
                            info = 'is your father';
                            break;
                        case 'mother':
                            info = 'is your mother';
                            break;
                        case 'grandmother':
                            info = 'is your grandmother';
                            break;
                        case 'grandfather':
                            info = 'is your grandfather';
                            break;
                        case 'badapappa':
                            info = 'is your badapappa';
                            break;
                        case 'acquaintance_m':
                            info = 'is your mutual acquaintance';
                            break;
                    }

                    return '<b>' + this.key + '</b> ' + info;
                }
            },

            plotOptions: {
                networkgraph: {
                    keys: ['from', 'to'],
                    layoutAlgorithm: {
                        enableSimulation: true,
                        integration: 'verlet',
                        linkLength: 100
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