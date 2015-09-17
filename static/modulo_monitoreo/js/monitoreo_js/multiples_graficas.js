        

        var chart;
           var chartData = [];

           AmCharts.ready(function () {
               // generate some random data first
               generateChartData();

               // SERIAL CHART
               chart = new AmCharts.AmSerialChart();
               //chart.pathToImages = "http://www.amcharts.com/lib/images/";
              chart.pathToImages = "{%static 'modulo_monitoreo/amcharts/images/' %}";
               chart.dataProvider = datachart;
               chart.categoryField = "fecha";
               chart.dataDateFormat= "YYYY-MM-DD JJ:NN:SS";

               // listen for "dataUpdated" event (fired when chart is inited) and call zoomChart method when it happens
               chart.addListener("dataUpdated", zoomChart);

               // AXES
               // category
               var categoryAxis = chart.categoryAxis;
               categoryAxis.parseDates = true; // as our data is date-based, we set parseDates to true
               categoryAxis.minPeriod = "ss"; // our data is daily, so we set minPeriod to DD
               categoryAxis.minorGridEnabled = true;
               categoryAxis.axisColor = "#DADADA";
               categoryAxis.twoLineMode = true;
               categoryAxis.dateFormats = [
               {
                    period: 'fff',
                    format: 'JJ:NN:SS'
                }, {
                    period: 'ss',
                    format: 'JJ:NN:SS'
                }, {
                    period: 'mm',
                    format: 'JJ:NN'
                }, {
                    period: 'hh',
                    format: 'JJ:NN'
                }, {
                    period: 'DD',
                    format: 'DD'
                }, {
                    period: 'WW',
                    format: 'DD'
                }, {
                    period: 'MM',
                    format: 'MMM'
                }, {
                    period: 'YYYY',
                    format: 'YYYY'
                }];
                var color;
                var offset  = 0;
                var graph;
           {% for grafica in graficas%}
               color = '#'+Math.floor(Math.random()*16777215).toString(16);
               // first value axis (on the left)
               var valueAxis{{grafica}} = new AmCharts.ValueAxis();
               valueAxis{{grafica}}.offset=offset;
               valueAxis{{grafica}}.axisColor =color;
               valueAxis{{grafica}}.axisThickness = 2;
               valueAxis{{grafica}}.gridAlpha = 0;
               chart.addValueAxis(valueAxis{{grafica}});

                // GRAPHS
               // first graph
               var graph{{grafica}} = new AmCharts.AmGraph();
               graph{{grafica}}.valueAxis = valueAxis{{grafica}}; // we have to indicate which value axis should be used
               graph{{grafica}}.title = "{{grafica}}";
               graph{{grafica}}.lineColor=color;
               graph{{grafica}}.valueField = "{{grafica}}";
               graph{{grafica}}.bullet = "round";
               graph{{grafica}}.hideBulletsCount = 30;
               graph{{grafica}}.bulletBorderThickness = 1;
               chart.addGraph(graph{{grafica}});
               graph ="graph{{grafica}}"
                offset = offset + 50;
           {% endfor %}


               // CURSOR
               var chartCursor = new AmCharts.ChartCursor();
               chartCursor.cursorAlpha = 0.1;
               chartCursor.fullWidth = true;
               chart.addChartCursor(chartCursor);

               // SCROLLBAR
               var chartScrollbar = new AmCharts.ChartScrollbar();
               chartScrollbar.graph = graph;
               chartScrollbar.scrollbarHeight = 40;
               chartScrollbar.color = "#FFFFFF";
               chartScrollbar.autoGridCount = true;
               chart.addChartScrollbar(chartScrollbar);

               // LEGEND
               var legend = new AmCharts.AmLegend();
               legend.marginLeft = 110;
               legend.useGraphSettings = true;
               chart.addLegend(legend);

                chart.amExport = {
                    top		: 0,
                    right		: 0,
                };



               // WRITE
               chart.write("chartdiv");
           });

           // generate some random data, quite different range
           function generateChartData() {
               var firstDate = new Date();
               firstDate.setDate(firstDate.getDate() - 50);

               for (var i = 0; i < 50; i++) {
                   // we create date objects here. In your data, you can have date strings
                   // and then set format of your dates using chart.dataDateFormat property,
                   // however when possible, use date objects, as this will speed up chart rendering.
                   var newDate = new Date(firstDate);
                   newDate.setDate(newDate.getDate() + i);

                   var visits = Math.round(Math.random() * 40) + 100;
                   var hits = Math.round(Math.random() * 80) + 500;
                   var views = Math.round(Math.random() * 6000);

                   chartData.push({
                       date: newDate,
                       temperatura: visits,
                       humedad: hits,
                       views: views
                   });
               }
           }

           // this method is called when chart is first inited as we listen for "dataUpdated" event
           function zoomChart() {
               // different zoom methods can be used - zoomToIndexes, zoomToDates, zoomToCategoryValues
               chart.zoomToIndexes(10, 20);
           }
   