document.addEventListener('DOMContentLoaded', function() {
    const safeJSONParse = (jsonString) => {
        if (!jsonString) return null;
        try {
            return JSON.parse(jsonString);
        } catch (e) {
            console.error("Error parsing JSON:", e);
            return null;
        }
    }

    const generateBranchGPAChart = () => {
        const container = document.getElementById('branch-gpa-chart');
        if (!container) return;
        
        const rawData = container.querySelector('pre').textContent;
        container.innerHTML = '';
        
        const branchGpaData = safeJSONParse(rawData);
        if (!branchGpaData || !branchGpaData.length) return;
        
        const traces = branchGpaData.map(branch => ({
            x: branch.semesters,
            y: branch.gpas,
            mode: 'lines+markers',
            name: branch.name
        }));
        
        const layout = {
            modebar: {
                remove: [
                    "pan",
                    "zoom",
                    "zoomIn",
                    "zoomOut",
                    "lasso2d",
                    "resetScale2d"
                ]
            },
            yaxis: { title: "GPA" },
            template: "plotly_white",
            autosize: true,
            height: 400,
            margin: { l: 50, r: 50, b: 80, t: 30, pad: 4 }
        };
        
        Plotly.newPlot(container, traces, layout);
    }
    
    const generateCombinedGPACGPAChart = () => {
        const container = document.getElementById('combined-chart-data');
        if (!container) return;
        
        const rawData = container.querySelector('pre').textContent;
        container.innerHTML = '';
        
        const combinedData = safeJSONParse(rawData);
        if (!combinedData || !combinedData.semesters) return;
        
        const traces = [
            {
                x: combinedData.semesters,
                y: combinedData.gpa.values,
                mode: 'lines+markers',
                name: combinedData.gpa.name,
                line: { color: combinedData.gpa.color || 'blue' }
            },
            {
                x: combinedData.semesters,
                y: combinedData.cgpa.values,
                mode: 'lines+markers',
                name: combinedData.cgpa.name,
                line: { color: combinedData.cgpa.color || 'orange' }
            }
        ];
        
        const layout = {
            modebar: {
                remove: [
                    "pan",
                    "zoom",
                    "zoomIn",
                    "zoomOut",
                    "lasso2d",
                    "resetScale2d"
                ]
            },
            yaxis: { title: "Value" },
            template: "plotly_white",
            autosize: true,
            height: 400,
            margin: { l: 50, r: 50, b: 80, t: 30, pad: 4 }
        };
        
        Plotly.newPlot(container, traces, layout);
    }

    const generateLevelBoxplot = () => {
        const container = document.getElementById('level-boxplot-data');
        if (!container) return;
        
        const rawData = container.querySelector('pre').textContent;
        container.innerHTML = '';
        
        const boxplotData = safeJSONParse(rawData);
        if (!boxplotData || !boxplotData.data) return;
        
        Plotly.newPlot(container, boxplotData.data, boxplotData.layout);
    }

    const generateSemesterBoxplot = () => {
        const container = document.getElementById('semester-boxplot-data');
        if (!container) return;
        
        const rawData = container.querySelector('pre').textContent;
        container.innerHTML = '';
        
        const boxplotData = safeJSONParse(rawData);
        if (!boxplotData || !boxplotData.data) return;

        Plotly.newPlot(container, boxplotData.data, boxplotData.layout);
    }

    const generateAllScoresBoxplot = () => {
        const container = document.getElementById('all-boxplot-data');
        if (!container) return;
        
        const rawData = container.querySelector('pre').textContent;
        container.innerHTML = '';
        
        const boxplotData = safeJSONParse(rawData);
        if (!boxplotData || !boxplotData.data) return;
        
        Plotly.newPlot(container, boxplotData.data, boxplotData.layout);
    }

    const generateSemesterAvgChart = () => {
        const container = document.getElementById('semester-avg-data');
        const container2 = document.getElementById('semester-avg-data2');
    
        const sourceContainer = container || container2;
        if (!sourceContainer) return;
    
        const pre = sourceContainer.querySelector('pre');
        if (!pre) return;
    
        const rawData = pre.textContent;
        const semesterAvgData = safeJSONParse(rawData);
        if (!semesterAvgData || !semesterAvgData.type) return;
    
        const trace = {
            x: semesterAvgData.data.x,
            y: semesterAvgData.data.y,
            mode: semesterAvgData.data.mode || 'lines+markers',
            name: semesterAvgData.data.name,
            marker: semesterAvgData.data.marker
        };
    
        const layout = {
            modebar: semesterAvgData.layout.modebar,
            yaxis: { title: semesterAvgData.layout.yaxis_title },
            template: "plotly_white",
            autosize: true,
            height: 400,
            margin: { l: 50, r: 50, b: 80, t: 30, pad: 4 }
        };
    
        if (container) {
            container.innerHTML = '';
            Plotly.newPlot(container, [trace], layout);
        }
    
        if (container2) {
            container2.innerHTML = '';
            Plotly.newPlot(container2, [trace], layout);
        }
    };

    const generateBranchAvgChart = () => {
        const container = document.getElementById('branch-avg-data');
        if (!container) return;
        
        const rawData = container.querySelector('pre').textContent;
        container.innerHTML = '';
        
        const branchAvgData = safeJSONParse(rawData);
        if (!branchAvgData || !branchAvgData.type || branchAvgData.type !== 'multi_scatter') return;
    
        const traces = branchAvgData.data.map(branch => ({
            x: branch.x,
            y: branch.y,
            mode: branch.mode || 'lines+markers',
            name: branch.name,
            marker: branch.marker,
            connectgaps: branch.connectgaps
        }));

        const layout = {
            modebar: branchAvgData.layout.modebar,
            yaxis: { title: branchAvgData.layout.yaxis_title },
            legend: { title: branchAvgData.layout.legend_title },
            template: "plotly_white",
            autosize: true,
            height: 400,
            margin: { l: 50, r: 50, b: 80, t: 30, pad: 4 }
        };
    
        Plotly.newPlot(container, traces, layout);
    }

    const generateScatterPlot = () => {
      const container = document.getElementById('scatter-plot-container');
      if (!container) return;
        
      const rawData = container.querySelector('pre').textContent;
      container.innerHTML = '';
        
      const scatterData = safeJSONParse(rawData);
      if (!scatterData || !scatterData.data) return;
      
      const trace = {
          x: scatterData.data.x,
          y: scatterData.data.y,
          mode: scatterData.data.mode || 'markers',
          marker: scatterData.data.marker || {
              size: 7,
              color: 'red',
              opacity: 0.6
          },
          text: scatterData.data.text,
          type: scatterData.type || 'scatter'
      };
        
      const layout = {
          yaxis: { title: scatterData.layout.yaxis_title || 'Scores' },
          template: scatterData.layout.template || 'plotly_white',
          xaxis: scatterData.layout.xaxis || {
              tickangle: 60,
              tickfont: { size: 11, style: 'italic' }
          },
          modebar: scatterData.layout.modebar || {
                remove: ["pan", "zoom", "zoomIn", "zoomOut", "lasso2d", "resetScale2d"]
          },
          autosize: true,
          height: 400,
          margin: { l: 50, r: 50, b: 120, t: 30, pad: 4 }
      };
        
      Plotly.newPlot(container, [trace], layout);
    }

    const generatePassRateChart = () => {
        const container = document.getElementById('pass-rate-data');
        if (!container) return;
        
        const rawData = container.querySelector('pre').textContent;
        container.innerHTML = '';
        
        const passRateData = safeJSONParse(rawData);
        if (!passRateData || !passRateData.semesters || !passRateData.branches) return;
        
        const semesters = passRateData.semesters;
        const branches = passRateData.branches;
        
        const traces = [];
        
        Object.entries(branches).forEach(([branchName, branchData]) => {
            traces.push({
                x: semesters,
                y: branchData.total,
                type: 'bar',
                name: `${branchName} (Total)`,
                marker: {
                    color: branchData.color,
                    opacity: 0.7
                },
                hoverinfo: 'none',
            });
            
            traces.push({
                x: semesters,
                y: branchData.passed,
                type: 'bar',
                name: `${branchName} (Passed)`,
                marker: {
                    color: branchData.color,
                    opacity: 1.0
                },
                hoverinfo: 'none',
            });
        });
        
        const layout = {
            barmode: passRateData.chart_settings.barmode || 'group',
            yaxis: { 
                title: passRateData.chart_settings.yaxis_title || "Number of Courses" 
            },
            xaxis: {
                tickangle: 20,
                fontsize: 8,
            },
            plot_bgcolor: passRateData.chart_settings.plot_bgcolor || '#ffffcc',
            height: passRateData.chart_settings.height || 500,
            template: "plotly_white",
            legend: {
                orientation: "h",
                yanchor: "bottom",
                y: 1.02,
                xanchor: "right",
                x: 1
            },
            modebar: {
                remove: [
                    "pan",
                    "zoom",
                    "zoomIn",
                    "zoomOut",
                    "lasso2d",
                    "resetScale2d"
                ]
            },
            margin: { l: 60, r: 30, b: 100, t: 30, pad: 4 },
        };
        
        Plotly.newPlot(container, traces, layout);
    }

    const generateBranchDistributionChart = () => {
        const container = document.getElementById('branch-distribution-chart');
        if (!container) return;
        
        const rawData = container.querySelector('pre').textContent;
        container.innerHTML = '';
        
        const branchData = safeJSONParse(rawData);
        if (!branchData || !branchData.semesters.length === 0) return;
        
        const traces = branchData.branches.map(branch => ({
            x: branchData.semesters,
            y: branch.counts,
            type: 'bar',
            name: branch.name,
            marker: {
                color: branch.color
            }
        }));
        
        const layout = {
            modebar: {
                remove: [
                    "pan",
                    "zoom",
                    "zoomIn",
                    "zoomOut",
                    "lasso2d",
                    "resetScale2d"
                ]
            },
            yaxis: { title: branchData.layout.yaxis_title },
            xaxis: { title: "Semester" },
            barmode: branchData.layout.barmode,
            bargap: branchData.layout.bargap,
            template: branchData.layout.template,
            autosize: true,
            height: branchData.layout.height,
            margin: { l: 50, r: 50, b: 80, t: 30, pad: 4 }
        };
        
        Plotly.newPlot(container, traces, layout);
    }

    const generateOverallBranchPieChart = () => {
        const container = document.querySelector('.branch-pie-chart .raw-data pre');
        if (!container) return;
        
        const containerParent = container.parentElement.parentElement;
        
        const rawData = container.textContent;
        containerParent.removeChild(container.parentElement);
        
        const chartDiv = document.createElement('div');
        chartDiv.id = 'branch-pie-chart';
        containerParent.appendChild(chartDiv);
        
        const pieData = safeJSONParse(rawData);
        if (!pieData || !pieData.data || !pieData.data.length) return;
        
        const trace = {
            type: 'pie',
            labels: pieData.data[0].labels,
            values: pieData.data[0].values,
            marker: {
                colors: pieData.data[0].marker.colors
            }
        };
        
        const layout = {
            template: pieData.layout.template || 'plotly_white',
            height: pieData.layout.height || 580,
            margin: pieData.layout.margin || { l: 40, r: 40, t: 50, b: 5 },
            legend: {
                orientation: 'h',
                yanchor: 'bottom',
                y: -0.2,
                xanchor: 'center',
                x: 0.5
            }
        };
        
        Plotly.newPlot('branch-pie-chart', [trace], layout);
    }

    const generateSemesterDistributionPies = () => {
      const container = document.querySelector('.semester-distribution-inner');
      if (!container) return;
      
      const pieContainers = container.querySelectorAll('.semester-distribution-item');
      if (!pieContainers.length) return;
      
      pieContainers.forEach(function(pieContainer, index) {
          const rawData = pieContainer.querySelector('pre').textContent;
          const pieData = safeJSONParse(rawData);
          if (!pieData) return;
          
          pieContainer.innerHTML = '';
          
          const trace = {
              type: 'pie',
              labels: pieData.data.labels,
              values: pieData.data.values,
              marker: {
                  colors: pieData.data.marker.colors
              }
          };
          
          const layout = {
              title: pieData.layout.title,
              template: "plotly_white",
              height: pieData.layout.height || 300,
              margin: pieData.layout.margin,
              showlegend: pieData.layout.showlegend
          };
          
          Plotly.newPlot(pieContainer, [trace], layout);
      });
    }

    const adjustChartsForSmallScreens = () => {
        if (window.innerWidth < 767) { 
            document.querySelectorAll('.js-plotly-plot').forEach(plot => {
              Plotly.relayout(plot, {
                showlegend: false,
                width: window.innerWidth * 0.95, 
                height: 400 ,
                xaxis: {
                  title: ''
                },
              });
            });
          }
    }

    const initializeCharts = () => {
        generateBranchGPAChart();
        generateCombinedGPACGPAChart();
        
        generateLevelBoxplot();
        generateSemesterBoxplot();
        generateAllScoresBoxplot();

        generateSemesterAvgChart();
        generateBranchAvgChart();

        generateScatterPlot();
        generatePassRateChart();
        generateBranchDistributionChart()
        generateOverallBranchPieChart()
        generateSemesterDistributionPies()
    }

    initializeCharts()
    adjustChartsForSmallScreens()
});