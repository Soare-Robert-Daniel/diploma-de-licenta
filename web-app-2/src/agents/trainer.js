import Env from './env'
import Agent from './agent'
import Memory from './memory'
import * as tf from '@tensorflow/tfjs';

class Trainer {
    /**
     * 
     * @param {Env} env 
     * @param {Agent} agent 
     * @param {Memory} memory
     */
    constructor(env, agent, memory) {
        this.env = env
        this.agent = agent
        this.memory = memory
    }

    async train(episodes = 3) {
        const discount = 0.985;
        // const lr = 0.1
        let epsilon = 1
        const epsilon_min = 0.0
        const epsilon_decay = (epsilon - epsilon_min) / episodes
        const maxIterations = 75
        console.time('Train')
        for (let eps = 0; eps < episodes; eps++) {
            console.log('Episode', eps, epsilon)
            let state = this.env.reset()


            for (let iter = 0; iter < maxIterations; iter++) {
                const action = Math.random() < epsilon ? this.env.actionSample() : this.agent.getAction(state)

                // console.log('Action', action)

                const [nextState, reward, done] = this.env.step(action)

                this.memory.add({ state, nextState, reward, done })

                // const nextQ = (this.agent.predict(nextState).arraySync())[0]
                // let newCurrentQ = (this.agent.predict(state).arraySync())[0]


                // //console.log('---')
                // // console.log(newCurrentQ, nextQ.max().arraySync())
                // if (reward === 100) {
                //     console.count('PUNCT ATINS')
                //     console.log(state, nextState)
                //     console.table(newCurrentQ, state, nextState)
                //     console.table(this.env.board.playerPos)
                // }
                // newCurrentQ[action] = done ? reward : reward + discount * Math.max(...nextQ)
                // if (reward === 100) {
                //     console.table(newCurrentQ)
                // }
                // //console.log(newCurrentQ)
                // //console.log('---')
                // await this.agent.fit(state, tf.tensor2d([newCurrentQ]))


                if (!done) {

                } else {
                    break
                }

                state = nextState
            }

            if (epsilon > epsilon_min) {
                epsilon -= epsilon_decay
                epsilon = Math.max(epsilon, 0)

            }

            console.log('All the memory:', this.memory)
            console.log('Shuffle:', this.memory.sample(10))

        }
        console.timeEnd('Train')
        return 'completed'
    }
}

export default Trainer