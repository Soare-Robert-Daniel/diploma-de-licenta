<script>
    import { onMount } from "svelte";
    import * as echarts from "echarts/core";
    import {
        TitleComponent,
        ToolboxComponent,
        TooltipComponent,
        GridComponent,
        LegendComponent,
    } from "echarts/components";
    import { LineChart } from "echarts/charts";
    import { CanvasRenderer } from "echarts/renderers";

    echarts.use([
        TitleComponent,
        ToolboxComponent,
        TooltipComponent,
        GridComponent,
        LegendComponent,
        LineChart,
        CanvasRenderer,
    ]);

    /**
     * @type {echarts.ECharts}
     */
    let chart;
    onMount(() => {
        chart = echarts.init(chartLocation);

        const option = {
            title: {
                text: "Recompense",
            },
            tooltip: {
                trigger: "axis",
            },
            legend: {
                data: ["Env 1", "Env 2", "Env 3", "Env 4", "Env 5"],
            },
            grid: {
                left: "3%",
                right: "4%",
                bottom: "3%",
                containLabel: true,
            },
            toolbox: {
                feature: {
                    saveAsImage: {},
                },
            },
            xAxis: {
                type: "category",
                boundaryGap: false,
                data: [1, 2, 3, 4, 5, 6, 7],
            },
            yAxis: {
                type: "value",
            },
            series: [
                {
                    name: "邮件营销",
                    type: "line",
                    stack: "总量",
                    data: [
                        120,
                        132,
                        101,
                        134,
                        90,
                        230,
                        210,
                        132,
                        101,
                        134,
                        90,
                        230,
                        210,
                    ],
                },
                {
                    name: "联盟广告",
                    type: "line",
                    stack: "总量",
                    data: [
                        220,
                        182,
                        191,
                        234,
                        290,
                        330,
                        310,
                        132,
                        101,
                        134,
                        90,
                        230,
                        210,
                    ],
                },
                {
                    name: "视频广告",
                    type: "line",
                    stack: "总量",
                    data: [
                        150,
                        232,
                        201,
                        154,
                        190,
                        330,
                        410,
                        132,
                        101,
                        134,
                        90,
                        230,
                        210,
                    ],
                },
                {
                    name: "直接访问",
                    type: "line",
                    stack: "总量",
                    data: [
                        320,
                        332,
                        301,
                        334,
                        390,
                        330,
                        320,
                        132,
                        101,
                        134,
                        90,
                        230,
                        210,
                    ],
                },
                {
                    name: "搜索引擎",
                    type: "line",
                    stack: "总量",
                    data: [
                        820,
                        932,
                        901,
                        934,
                        1290,
                        1330,
                        1320,
                        132,
                        101,
                        134,
                        90,
                        230,
                        210,
                    ],
                },
            ],
        };

        chart.setOption(option);
    });

    let chartLocation;
</script>

<div class="container">
    <div bind:this={chartLocation} class="chart" id="main" />
</div>

<style lang="scss">
    .container {
        margin-top: 50px;
        .chart {
            box-shadow: rgb(0 0 0 / 10%) 0px 0px 20px;
            padding: 10px;
            width: 800px;
            height: 400px;
        }
    }
</style>
