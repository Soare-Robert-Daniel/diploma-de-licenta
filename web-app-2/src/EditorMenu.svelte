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
        <div class="options">
            <Button onClick={() => boardControlEvents.addEvent("train")}
                >Train</Button
            >
            <Button
                variant="info"
                onClick={() => boardControlEvents.addEvent("run")}
                >Rulare</Button
            >
            <Button
                variant="warning"
                onClick={() => boardControlEvents.addEvent("reset", 2)}
                >Reset</Button
            >
        </div>
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
        justify-content: center;

        .commands {
            padding: 15px;
            border: 1px dashed #aaa;
            display: flex;
            flex-direction: column;
            align-items: center;

            .options {
                display: inline-flex;
            }
        }
    }
</style>
