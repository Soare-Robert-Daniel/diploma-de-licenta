import * as tf from '@tensorflow/tfjs';

class DNNAgent {
    /**
     * @type {tf.Sequential | undefined}
     */
    model = undefined

    /**
     * 
     * @param {tf.Sequential} model 
     */
    constructor(model = undefined) {

        if (model) {
            this.model = model
        }
    }

    static buildModel() {
        tf.setBackend('webgl');
        console.log("Backend", tf.getBackend());
        const model = tf.sequential()

        model.add(tf.layers.inputLayer({ inputShape: [8] }))

        model.add(tf.layers.dense({
            units: 12,
            activation: 'relu'
        }))

        model.add(tf.layers.dense({
            units: 24,
            activation: 'relu'
        }))

        model.add(tf.layers.dense({
            units: 6,
            activation: 'relu'
        }))

        model.add(tf.layers.dense({
            units: 2,
            activation: 'relu'
        }))

        model.compile({
            optimizer: tf.train.adam(),
            loss: tf.losses.meanSquaredError,
            metrics: ['mse']
        })

        model.summary()

        return new DNNAgent(model)
    }

    async train(inputs, outputs) {
        return await this.model.fit(inputs, outputs, {
            batchSize: 32,
            epochs: 1,
            shuffle: true
        })
    }

    predict(inputs) {
        return this.model.predict(inputs)
    }
}

export default DNNAgent