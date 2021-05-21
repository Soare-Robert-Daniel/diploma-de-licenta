import Target from './target'
import Vector from './vector'
import { cloneDeep, flatMap, sampleSize } from 'lodash'
class Agent {
    /**
     * 
     * @param {Vector} pos 
     * @param {Vector} direction 
     * @param {number} size
     * @param {boolean} isRunner
     */
    constructor(pos, direction, size, isRunner = false) {
        this.pos = cloneDeep(pos)
        this.dir = cloneDeep(direction)
        this.max_turn_rate = 5
        this.min_turn_rate = 1
        this.turnRate = 5 * Math.PI / 180
        this.speed = 1
        this.size = size
        this.target = undefined
        this.taskCompleted = false
        this.memory = []
        this.isRunner = isRunner
    }

    move() {
        // console.log("dir", this.dir, this.dir.clone())
        if (this.target !== undefined && this.target !== null) {
            this.rotateTowardTarget(this.target.pos)
        }
        const displacement = this.dir.clone().mult(this.speed)
        // console.log(displacement)
        this.pos.add(displacement).round()
        this.distanceToTarget()
    }

    /**
     * Roteste agentul catre obiectiv
     * @param {Vector} target 
     */
    rotateTowardTarget(target) {
        const angleDiff = this.dir.angleWith(target.clone().substract(this.pos))

        //console.log("Diff", angleDiff * 180 / Math.PI)
        if (Math.abs(angleDiff) < this.turnRate) {
            //console.log("NO ROTATION", Math.abs(angleDiff), this.turnRate)
            return
        }

        this.dir = Vector.rotate(((angleDiff > 0) ? 1 : - 1) * this.turnRate, this.dir)
    }

    /**
     * 
     * @param {Target} target 
     */
    setTarget(target) {
        //console.log("New Target", target)

        this.target = target
        this.taskCompleted = false

        if (target && !this.isRunner) {
            document.dispatchEvent(new CustomEvent('agent-switch-target', {
                detail: {
                    data: this.createRunner().setTarget(target).runToTarget().dumpMemory()
                }

            }))
        }

        return this
    }

    distanceToTarget() {
        if (this.target !== undefined && this.target !== null) {
            const dist = this.pos.distTo(this.target.pos)
            // console.log(dist)
            if (dist - this.size - this.target.size <= 0) {
                //console.log("Completed")
                this.taskCompleted = true
            }
        }
    }

    runToTarget() {
        //console.log("RUN!")
        if (!this.target) {
            throw "Target was not set!"
        }
        this.memory = []
        for (let iter = 0; iter < 600; iter++) {

            this.memory.push({
                pos: cloneDeep(this.pos),
                dir: cloneDeep(this.dir),
                size: cloneDeep(this.size),
                posTarget: cloneDeep(this.target.pos),
                sizeTarget: cloneDeep(this.target.size)
            })
            this.move()

            if (this.taskCompleted) {
                // console.log("Run Complet!")
                break
            }
        }
        if (!this.taskCompleted) {
            console.log("Run failed!")
        }
        return this
    }

    createRunner() {
        return new Agent(this.pos, this.dir, this.size, true)
    }

    createRunnerWalkedPath() {
        if (this.memory.length > 0) {
            const path = flatMap(this.memory, experience => {
                // console.log([experience.pos.x, experience.pos.y])
                return [experience.pos.x, experience.pos.y]
            })
            // console.log("Path", path, this.memory)
            return path
        } else {
            console.log("Empty Memory", this)
            return []
        }
    }

    dumpMemory() {
        return this.memory
    }
}

export default Agent