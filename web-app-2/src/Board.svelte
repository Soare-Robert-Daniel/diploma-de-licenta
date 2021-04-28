<script>
    import { onDestroy, onMount } from "svelte";
    import Konva from "konva";
    import Board from "./board/board";
    import BoardUI from "./board/boardUI";
    import { boardControlEvents, boardControlState } from "./store";
    /**
     * @type {Konva.Stage}
     */
    let stage;
    const board = new Board(10, 10);
    /**
     * @type {BoardUI}
     */
    let boardUI;

    $: console.log($boardControlEvents, $boardControlState);
    $: $boardControlEvents.forEach((event) => {
        if (event.eventName === "move") {
            board.move("DOWN");
            boardControlEvents.consumeEvent(event.id);
        }
    });

    const unsubscribeBoardControl = boardControlEvents.subscribe((events) => {
        events.forEach((event) => {
            if (event.eventName === "move") {
                console.log(event);
                console.log(board.move(event.payload.action));
                boardControlEvents.consumeEvent(event.id);
            } else if (event.eventName === "reset") {
                board.reset();
                boardControlEvents.consumeEvent(event.id);
            }
        });
    });

    onMount(() => {
        stage = new Konva.Stage({
            container: "container",
            width: 600,
            height: 600,
        });

        boardUI = new BoardUI(board, stage);
        boardUI.createBoard();

        stage.on("click", () => {
            const { x, y } = stage.getPointerPosition();
            const [posX, posY] = [
                Math.floor(x / boardUI.cellWidth),
                Math.floor(y / boardUI.cellHeight),
            ];
            if ($boardControlState.movePlayer) {
                console.log("Pos", posX, posY);
                board.setPlayerPos(posX, posY);
            } else if ($boardControlState.addObstacle) {
                console.log("Obs Pos", posX, posY);
                board.setObstacle(posX, posY);
            }
        });
    });

    onDestroy(unsubscribeBoardControl);
</script>

<div id="container" class="container" />

<style>
    .container {
        max-width: 100%;
        border: 1px solid #aaa;
    }
</style>
