<script>
    import { onMount } from "svelte";
    import * as echarts from "echarts/core";
    import {
        TitleComponent,
        TooltipComponent,
        GridComponent,
    } from "echarts/components";
    import { BarChart } from "echarts/charts";
    import { CanvasRenderer } from "echarts/renderers";

    echarts.use([
        TitleComponent,
        TooltipComponent,
        GridComponent,
        BarChart,
        CanvasRenderer,
    ]);

    onMount(() => {});

    let chartLocation;
</script>

<div class="container">
    <div bind:this={chartLocation} id="main" />
</div>

<style lang="scss">
</style>
