import Board from '../board/board'

class Env {
    ACTIONS = ['UP', 'DOWN', 'RIGHT', 'LEFT']
    invalidState = false
    /**
     * 
     * @param {Board} board 
     */
    constructor(board) {
        this.board = board
    }

    step(action) {
        this._applyAction(action)
        return [this._getState(), this._getReward(), this._isDone()]
    }

    reset() {
        this.board.playerReset()
        return this._getState()
    }

    actionSample() {
        return Math.floor(Math.random() * this.ACTIONS.length)
    }

    _getState() {
        return this.board.getBoardState()
    }

    _getReward() {
        return (this.invalidState && !this.board.isOnExit() && -100) || this.board.getPlayerCellValue()
    }

    _applyAction(action) {
        if (this.ACTIONS[action] === undefined) {

            console.warn(action)
        }
        this.invalidState = !this.board.move(this.ACTIONS[action])
    }

    _isDone() {
        return this.board.isOnExit() || this.invalidState
    }

    clone() {
        return new Env(this.board.clone())
    }
}

export default Env