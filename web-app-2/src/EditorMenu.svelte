<script>
    import Button from "./components/Button.svelte";
    import { boardControlEvents, boardControlState } from "./store";

    let movePlayer = false;
    let addObstacle = false;

    $: $boardControlState.movePlayer = movePlayer;
    $: $boardControlState.addObstacle = addObstacle;
</script>

<div class="menu">
    <div class="commands">
        <Button
            onClick={() =>
                boardControlEvents.addEvent("move", { action: "UP" })}
            >Sus</Button
        >
        <Button
            onClick={() =>
                boardControlEvents.addEvent("move", { action: "DOWN" })}
            >Jos</Button
        >
        <Button
            onClick={() =>
                boardControlEvents.addEvent("move", { action: "LEFT" })}
            >Stânga</Button
        >
        <Button
            onClick={() =>
                boardControlEvents.addEvent("move", { action: "RIGHT" })}
            >Dreapta</Button
        >
        <Button onClick={() => boardControlEvents.addEvent("reset", 2)}
            >Reset</Button
        >
        <div>
            <label>
                <input type="checkbox" bind:checked={movePlayer} />
                Misca agentul
            </label>
            <label>
                <input type="checkbox" bind:checked={addObstacle} />
                Adauga Obstacol
            </label>
        </div>
    </div>
</div>

<style lang="scss">
    .menu {
        width: 100%;
        padding: 10px;
        margin: 3px;

        .commands {
            padding: 15px;
            border: 1px dashed #aaa;
        }
    }
</style>
