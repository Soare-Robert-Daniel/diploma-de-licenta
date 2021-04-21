import Target from './target'
import Vector from './vector'

class Agent {
    /**
     * 
     * @param {Vector} pos 
     * @param {Vector} direction 
     * @param {number} size
     */
    constructor(pos, direction, size) {
        this.pos = pos
        this.dir = direction
        this.max_turn_rate = 5
        this.min_turn_rate = 1
        this.turnRate = 5 * Math.PI / 180
        this.speed = 1
        this.size = size
        this.target = undefined
        this.taskCompleted = false
    }

    move() {
        // console.log("dir", this.dir, this.dir.clone())
        if (this.target !== undefined && this.target !== null) {
            this.rotateTowardTarget(this.target.pos)
        }
        const displacement = this.dir.clone().mult(this.speed)
        // console.log(displacement)
        this.pos.add(displacement)
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
        console.log("New Target", target)

        this.target = target
        this.taskCompleted = false
    }

    distanceToTarget() {
        if (this.target !== undefined && this.target !== null) {
            const dist = this.pos.distTo(this.target.pos)
            // console.log(dist)
            if (dist - this.size - this.target.size <= 0) {
                console.log("Completed")
                this.taskCompleted = true
            }
        }
    }
}

export default Agent