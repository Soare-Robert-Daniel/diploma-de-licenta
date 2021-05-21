import { Circle } from "konva/types/shapes/Circle"
import Vector from "./vector"

class Target {
    /**
     * 
     * @param {Vector} position 
     * @param {Circle} shape 
     * @param {number} size
     */
    constructor(position, shape, size) {
        this.pos = position
        this.shape = shape
        this.size = size
    }
}

export default Target