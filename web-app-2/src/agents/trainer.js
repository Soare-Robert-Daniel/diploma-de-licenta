import Env from './env'
import Agent from './agent'
import Memory from './memory'
import * as tf from '@tensorflow/tfjs';

class Trainer {
    totalEnvs = 2
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

        this.envs = []
    }

    async train(episodes = 150, cb = () => { }) {
        this.createMultipleEnvs()
        const discount = 0.985;
        // const lr = 0.1
        let epsilon = 1
        const epsilon_min = 0.0
        const epsilon_decay = (epsilon - epsilon_min) / episodes
        const maxIterations = 75
        console.time('Train')
        console.log('Env', this.envs)
        for (let eps = 0; eps < episodes; eps++) {
            console.time('Episode')
            const t0 = performance.now()
            console.log('Episode', eps, epsilon)

            const rewardsAnaly = {}
            this.envs.forEach(({ id, env }) => {
                let state = env.reset()

                for (let iter = 0; iter < maxIterations; iter++) {
                    const action = Math.random() < epsilon ? env.actionSample() : this.agent.getAction(state)
                    const [nextState, reward, done] = env.step(action)
                    this.memory.add({ state, nextState, reward, done, action })

                    // Analytics
                    rewardsAnaly[id] = rewardsAnaly[id] ? rewardsAnaly[id] + reward : reward
                    if (done) {
                        break
                    }

                    state = nextState
                }
            })

            for (const exper of this.memory.sample(100)) {
                const { nextState, reward, done, state, action } = exper
                const nextQ = (this.agent.predict(nextState).arraySync())[0]
                const newCurrentQ = (this.agent.predict(state).arraySync())[0]

                if (reward === 100) {
                    console.count('PUNCT ATINS')
                }
                newCurrentQ[action] = done ? reward : reward + discount * Math.max(...nextQ)
                await this.agent.fit(state, tf.tensor2d([newCurrentQ]))
            }


            if (epsilon > epsilon_min) {
                epsilon -= epsilon_decay
                epsilon = Math.max(epsilon, 0)
            }
            const t1 = performance.now()
            console.timeEnd('Episode')
            console.log(t1 - t0)
            cb({
                episodeTime: t1 - t0,
                episodeRewards: rewardsAnaly
            })
            console.log('---')
        }
        console.timeEnd('Train')
        return 'completed'
    }

    createMultipleEnvs() {
        this.envs = []
        let id = 1
        const uniqPos = []

        this.envs.push({ id: id++, env: this.env })
        for (let n = 0; n < this.totalEnvs; n++) {
            let pair = [Math.floor(Math.random() * this.env.board.cols), Math.floor(Math.random() * this.env.board.rows)]
            let isUniq = uniqPos.filter(p => p[0] !== pair[0] && p[1] !== pair[1]).length === 0
            while (!isUniq) {
                pair = [Math.floor(Math.random() * this.env.board.cols), Math.floor(Math.random() * this.env.board.rows)]
                isUniq = uniqPos.filter(([x, y]) => x !== pair[0] && y !== pair[1]).length === 0
            }
            uniqPos.push(pair)
        }

        uniqPos.forEach(pos => {
            const clone = this.env.clone()
            console.log('clone', clone)
            clone.setAgentStartPosition({
                x: pos[0],
                y: pos[1]
            })
            clone.reset()
            this.envs.push({ id: id++, env: clone })
        })

    }

    static run(env, agent) {
        console.log(env, agent)
        const maxIterations = 75
        let state = env.reset()

        for (let iter = 0; iter < maxIterations; iter++) {
            const action = agent.getAction(state)
            const [nextState, reward, done] = env.step(action)

            if (done) {
                break
            }

            state = nextState
        }
    }
}

export default Trainer