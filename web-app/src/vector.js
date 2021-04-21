class Vector {
    /**
     * Creaza un vector 2D
     * @param {number} x 
     * @param {number} y 
     */
    constructor(x, y) {
        this.x = x
        this.y = y
    }

    add(other) {
        this.x += other.x
        this.y += other.y
        return this
    }

    substract(other) {
        this.x -= other.x
        this.y -= other.y
        return this
    }

    dot(other) {
        return this.x * other.x + this.y * other.y
    }

    mag() {
        return Math.sqrt(this.x * this.x + this.y * this.y)
    }

    mult(k) {
        this.x *= k;
        this.y *= k;
        return this
    }

    distSqrtTo(other) {
        const x = other.x - this.x
        const y = other.y - this.y
        return x * x + y * y
    }

    distTo(other) {
        return Math.sqrt(this.distSqrtTo(other))
    }



    clone() {
        return new Vector(this.x, this.y)
    }

    /**
     * 
     * @param {Vector} other 
     * @returns 
     */
    angleWith(other) {
        // cosAlpha = this.dot(other) / ( this.mag() * other.mag() )
        //const angle = Math.atan2(other.y, other.x) - Math.atan2(this.y, this.x)
        const angle = Math.atan2(other.y * this.x - this.y * other.x, other.x * this.x + this.y * other.y)

        // console.log("Angle", angle * 180 / Math.PI, this, other)
        return angle
    }

    /**
     * 
     * @param {number} turnRat 
     * @param {Vector} v 
     * @returns 
     */
    static rotate(turnRate, v) {
        const cosT = Math.cos(turnRate)
        const sinT = Math.sin(turnRate)
        const x = v.x * cosT - v.y * sinT
        const y = v.x * sinT + v.y * cosT
        return new Vector(x, y)
    }

    static fromPoints(a, b) {
        return Vector(b.x - a.x, b.y - a.y)
    }
}

export default Vector