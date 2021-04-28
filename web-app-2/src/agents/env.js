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

    _getState() {
        const { x, y } = this.board.playerPos
        return [x, y]
    }

    _getReward() {
        return this.board.getPlayerCellValue()
    }

    _applyAction(action) {
        this.invalidState = !this.board.move(this.ACTIONS[action])
    }

    _isDone() {
        return this.board.isOnExit() || (this.invalidState && -100)
    }
}

export default Env