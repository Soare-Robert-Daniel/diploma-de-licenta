import * as tf from '@tensorflow/tfjs';
import DNNModel from './DNNAgent'

class DataPipeline {
    constructor(maxSize = 1000) {
        this.maxSize = maxSize
        this.agentsData = []
        this.agentModel = DNNModel.buildModel()
    }

    /**
     * 
     * @param {array} agentData 
     */
    addDataFromAgent(agentData) {
        // if (this.agentsData.length + agentData.length > this.maxSize) {
        //     this.agentsData = this.agentsData.slice(this.maxSize - (this.agentsData.length + agentData.length))
        // }
        this.agentsData.push(...agentData)

        console.log("Added", this.agentsData.length)
    }

    convertToTensor() {
        if (this.agentsData.length < 2) {
            throw "Not enough data!"
        }
        return tf.tidy(() => {
            const inputData = []
            const outputData = []

            for (let idx = 0; idx < this.agentsData.length - 1; idx++) {
                inputData.push(this.agentsData[idx])
                outputData.push(this.agentsData[idx + 1])
            }

            const inputTensor = inputData.map(d => [d.pos.x, d.pos.y, d.dir.x, d.dir.y, d.size, d.posTarget.x, d.posTarget.y, d.sizeTarget])
            const outputTensor = outputData.map(d => [d.posTarget.y, d.sizeTarget])

            return {
                input: tf.tensor2d(inputTensor, [inputTensor.length, 8]),
                output: tf.tensor2d(outputTensor, [outputTensor.length, 2])
            }
        })
    }

    getStatus() {
        return {
            totalData: this.agentsData.length,
            display: `${this.agentsData.length}/${this.maxSize}`
        }
    }

    async trainModels() {
        const { input, output } = this.convertToTensor()
        this.agentsData = []

        this.agentModel.train(input, output)
    }
}

export default DataPipeline