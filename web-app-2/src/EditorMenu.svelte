<script>
    import Button from "./components/Button.svelte";
    import Checkbox from "./components/Checkbox.svelte";
    import { boardControlEvents, boardControlState } from "./store";

    let movePlayer = false;
    let addObstacle = false;

    $: $boardControlState.movePlayer = movePlayer;
    $: $boardControlState.addObstacle = addObstacle;
</script>

<div class="menu">
    <div class="commands">
        <Button onClick={() => boardControlEvents.addEvent("train")}
            >Train</Button
        >
        <Button onClick={() => boardControlEvents.addEvent("run")}
            >Rulare</Button
        >
        <Button onClick={() => boardControlEvents.addEvent("reset", 2)}
            >Reset</Button
        >
        <div class="options">
            <Checkbox
                isChecked={movePlayer}
                onChange={(value) => {
                    movePlayer = value;
                }}
                text={"Misca agentul"}
            />
            <Checkbox
                isChecked={addObstacle}
                onChange={(value) => {
                    addObstacle = value;
                }}
                text={"Adauga Obstacol"}
            />
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

            .options {
                display: inline-flex;
            }
        }
    }
</style>
