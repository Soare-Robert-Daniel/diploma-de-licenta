class Memory {
    constructor(capacity) {
        this.capacity = capacity || 5000
        this.experiences = []
    }

    add(exper) {
        if (this.experiences.length + 1 > this.capacity) {
            this.experiences.shift()
        }
        this.experiences.push(exper)
    }

    sample(batch) {
        const randomExperiences = Memory.shuffle([...this.experiences])
        return randomExperiences.slice(0, batch)
    }

    /**
     * Shuffle the array using Fisher–Yates Shuffle
     * @param {Array} array 
     * @returns 
     */
    static shuffle(array) {
        // https://bost.ocks.org/mike/shuffle/
        let m = array.length, t, i;

        // While there remain elements to shuffle…
        while (m) {

            // Pick a remaining element…
            i = Math.floor(Math.random() * m--);

            // And swap it with the current element.
            t = array[m];
            array[m] = array[i];
            array[i] = t;
        }

        return array;
    }
}

export default Memory