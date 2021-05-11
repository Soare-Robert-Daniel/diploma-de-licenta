<script>
    import { onMount, onDestroy } from "svelte";
    import { analyticsData } from "./../store";

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

    const option = {
        title: {
            text: "Recompense acumulate",
        },
        tooltip: {
            trigger: "axis",
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
        },
        yAxis: {
            type: "value",
        },
    };

    let data = null;
    /**
     *
     * @param {Array} rawData
     */
    function extractData(rawData) {
        const legend = {
            data: Object.keys(rawData[0]?.episodeRewards || {}).map(
                (name) => `Env-${name}`
            ),
        };

        const xAxis = {
            data: Array.from({ length: rawData.length }, (x, i) => i + 1),
        };

        const series = Object.keys(rawData[0]?.episodeRewards || {}).map(
            (envName) => {
                return {
                    name: `Env-${envName}`,
                    type: "line",
                    data: rawData.map(
                        ({ episodeRewards }) => episodeRewards[envName]
                    ),
                };
            }
        );

        return { legend, xAxis, series };
    }

    const unsubscribe = analyticsData.subscribe(({ boardData }) => {
        //console.log("Anal store", s);
        data = boardData && extractData(boardData);
    });

    $: data && chart?.setOption(data);

    /**
     * @type {echarts.ECharts}
     */
    let chart;
    onMount(() => {
        chart = echarts.init(chartLocation);

        chart.setOption(option);
    });

    onDestroy(unsubscribe);

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
