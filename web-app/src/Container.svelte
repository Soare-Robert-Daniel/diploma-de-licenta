<script>
    import Konva from "konva";
    import { onMount } from "svelte";
    import Vector from "./vector";
    import Agent from "./agent";
import Target from "./target";
    let stage;
    let anim;
    const mapSize = {
        width: 600,
        height: 600,
    };

    onMount(() => {
        stage = new Konva.Stage({
            container: "konva-container", // id of container <div>
            ...mapSize,
        });
        const targets = [];

        // add canvas element
        const agentsLayer = new Konva.Layer();
        const targetsLayer = new Konva.Layer();
        stage.add(agentsLayer);
        stage.add(targetsLayer);

        /**
         * Agent Props
         */
        const agentDir = new Vector(0, 1);
        const agentController = new Agent(new Vector(50, 50), agentDir, 20);
        const agent = new Konva.Circle({
            x: 50,
            y: 50,
            radius: 20,
            fill: "#00D2FF",
            stroke: "black",
            strokeWidth: 4,
        });
        const speed = -1;
        const dirX = 0;
        const dirY = 1;
        agentsLayer.add(agent);

        agentsLayer.draw();
        console.count("onMount");

        // add cursor styling
        stage.on("mouseover", function () {
            document.body.style.cursor = "crosshair";
        });
        stage.on("mouseout", function () {
            document.body.style.cursor = "default";
        });

        stage.on("click", () => {
            console.log(stage.getPointerPosition());
            const { x, y } = stage.getPointerPosition();
            console.log(agentDir.angleWith(new Vector(x, y)));
            agentController.rotateTowardTarget(new Vector(x, y));
            
            const target = new Konva.Circle({
                x: x,
                y: y,
                radius: 10,
                fill: "#FF1111",
                stroke: "black",
                strokeWidth: 2,
            });

            targetsLayer.add(target);
            targetsLayer.draw();
            targets.push(new Target(new Vector(x, y), target, 10));
        });

        anim = new Konva.Animation((frame) => {
            // agent.move({ x: dirX * speed, y: dirY * speed });
            // if (stage.getPointerPosition() && agentController.pos.x < 600) {
            //     const { x, y } = stage.getPointerPosition();
            //     console.log(x, y);
            //     agentController.rotateTowardTarget(new Vector(x, y));
            // }
            if( targets.length > 0 ) {
                if( agentController.taskCompleted ) {
                    if( agentController.target !== undefined ) {
                        agentController.target.shape.destroy()
                        targetsLayer.draw()
                    }
                    targets.shift()
                    console.log(targets)
                    agentController.setTarget(targets[0])
                } else if( agentController.target === undefined ) {
                    agentController.setTarget(targets[0])
                }
                agentController.move();
                agent.x(agentController.pos.x);
                agent.y(agentController.pos.y);
            }
            
            
        }, agentsLayer);

        anim.start();
    });
</script>

<div class="container">
    <div id="konva-container" class="app" />
</div>

<style lang="scss">
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 10px;
        .app {
            box-shadow: 0px 0px 8px 4px rgba(106, 95, 255, 0.75);
            width: max-content;
        }
    }
</style>
