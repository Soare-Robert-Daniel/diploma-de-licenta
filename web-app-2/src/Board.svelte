<script>
    import { onDestroy, onMount } from "svelte";
    import Konva from "konva";
    import Board from "./board/board";
    import BoardUI from "./board/boardUI";
    import RewardEnvChart from "./components/RewardEnvChart.svelte";
    import { boardControlEvents, boardControlState } from "./store";
    import Env from "./agents/env";
    import Agent from "./agents/agent";
    import Trainer from "./agents/trainer";
    import Memory from "./agents/memory";
    import { maxBy } from "lodash";
    /**
     * @type {Konva.Stage}
     */
    let stage;
    const board = new Board(10, 10);
    /**
     * @type {BoardUI}
     */
    let boardUI;
    /**
     * @type {Env}
     */
    const env = new Env(board);
    const agent = new Agent();
    const memory = new Memory();
    const trainer = new Trainer(env, agent, memory);

    let trainStatus = "idle";

    let actionsStat = [
        { name: "sus", value: 0 },
        { name: "jos", value: 0 },
        { name: "dreapta", value: 0 },
        { name: "stanga", value: 0 },
    ];
    let maxActionStat = {};

    let trainAnalytisc = [];

    $: console.log($boardControlEvents, $boardControlState, trainAnalytisc);

    const unsubscribeBoardControl = boardControlEvents.subscribe((events) => {
        events.forEach((event) => {
            if (event.eventName === "move") {
                // console.log(event);
                // board.move(event.payload.action)
                env._applyAction(1);
                boardControlEvents.consumeEvent(event.id);
            } else if (event.eventName === "reset") {
                board.reset();
                boardControlEvents.consumeEvent(event.id);
            } else if (event.eventName === "train") {
                trainStatus = "progress";
                trainer
                    .train(100, (data) => {
                        trainAnalytisc = [...trainAnalytisc, data];
                    })
                    .then((status) => {
                        trainStatus = status;
                    });
                boardControlEvents.consumeEvent(event.id);
            } else if (event.eventName === "run") {
                Trainer.run(env, agent);
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
            if ($boardControlState.movePlayer && trainStatus !== "progress") {
                // console.log("Pos", posX, posY);
                board.setPlayerPos(posX, posY);
                console.log(board.getBoardState());
                const pred = agent
                    .predict(board.getBoardState())
                    .arraySync()[0];
                console.log(pred);
                actionsStat = actionsStat.map((info, index) => {
                    info.value = pred[index].toFixed(2);
                    return info;
                });
                maxActionStat = maxBy(actionsStat, ({ value }) => value);
                console.log(maxActionStat);
            } else if ($boardControlState.addObstacle) {
                // console.log("Obs Pos", posX, posY);
                board.setObstacle(posX, posY);
            }
        });

        // const test = setInterval(async () => {
        //     env.step(env.actionSample());
        //     //console.log(board.getBoardState());
        //     agent.predict(board.getBoardState()).print();
        //     // await agent.fit(board.getBoardState(), [[0, 10, 20, 30]]);
        // }, 1000);
    });

    onDestroy(unsubscribeBoardControl);
</script>

<div class="board">
    <div class="container">
        <div class="stats">
            <div class={`train-status ${trainStatus}`}>
                <h3>Train status: {trainStatus}</h3>
            </div>
            <div class="commands">
                {#each actionsStat as actionStat}
                    <div
                        class={`command ${
                            actionStat.name === maxActionStat.name && "max"
                        }`}
                    >
                        <p>
                            {actionStat.name}: <span>{actionStat.value}</span>
                        </p>
                    </div>
                {/each}
            </div>
        </div>
        <div id="container" />
    </div>

    <RewardEnvChart />
</div>

<style lang="scss">
    .board {
        display: flex;
        flex-direction: column;
        .container {
            max-width: 100%;
            border: 1px solid #aaa;
            display: flex;
            flex-direction: row;

            .stats {
                display: flex;
                flex-direction: column;
                width: max-content;

                .train-status {
                    padding: 5px;
                    margin: 10px;
                    border-radius: 10px;
                    font-family: Georgia, "Times New Roman", Times, serif;
                    h3 {
                        color: white;
                        font-size: 16px;
                    }
                    &.idle {
                        background-color: sandybrown;
                    }

                    &.completed {
                        background-color: green;
                    }

                    &.progress {
                        background-color: red;
                    }
                }

                .commands {
                    margin: 10px;
                    padding: 15px;
                    border: 3px dashed #aaa;
                    display: flex;
                    flex-direction: column;
                    width: max-content;
                    transition: all 0.5s;

                    .command {
                        width: 100%;
                        display: flex;
                        justify-content: flex-end;
                        padding: 5px;
                        p {
                            font-family: "Courier New", Courier, monospace;
                            color: black;
                            font-weight: 600;
                            margin: 3px 0px;
                            span {
                                padding: 5px;
                                color: white;
                                background-color: cornflowerblue;
                                border-radius: 10px;
                                box-sizing: content-box;
                                width: 70px;
                                display: inline-block;
                            }
                        }

                        &.max {
                            background-color: darkcyan;
                            border-radius: 10px;
                            p {
                                color: white;
                            }
                        }
                    }
                }
            }
        }
    }
</style>
