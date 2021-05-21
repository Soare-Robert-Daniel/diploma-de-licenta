class Board {

    constructor(numRows, numCols, playerDefaultPos = { x: 0, y: 0 }) {
        this.rows = numRows
        this.cols = numCols
        this.board = []

        this.initialize()
        this.playerDefaultPos = playerDefaultPos
        this.playerPos = playerDefaultPos

        this.eventListeners = []
    }

    reset() {
        this.initialize()
        this.dispatchEvent('reset')
    }

    playerReset() {
        this.playerPos = { ...this.playerDefaultPos }
    }

    initialize() {
        this.board = Array(this.rows).fill().map(() => Array(this.cols).fill({
            cellType: 'empty',
            value: -1,
            agentValue: undefined
        }))
        this.board[this.rows - 5][this.cols - 5] = {
            cellType: 'exit',
            value: 100,
            agentValue: 0
        }

        this.playerPos = {
            x: 0,
            y: 0
        }
    }

    getBoardState() {
        const state = this.board.map(row => row.map(cell => {
            return (cell.cellType === 'empty' && 1) || (cell.cellType === 'obstacle' && 2) || (cell.cellType === 'exit' && 3) || -1
        }))
        state[this.playerPos.y][this.playerPos.x] += 10

        return state
    }

    getShape() {
        return [this.rows, this.cols]
    }

    setPlayerPos(x, y) {
        // console.log(x, y)
        if (0 <= x && x < this.cols && 0 <= y && y < this.rows) {
            this.playerPos.x = x;
            this.playerPos.y = y;
            this.dispatchEvent('player', this.playerPos)
            return true
        }
        return false
    }

    getPlayerCellValue() {
        return this.board[this.playerPos.y][this.playerPos.x].value
    }

    setCellAgentValue(x, y, agentValue) {
        if ((0 <= x && x < this.cols && 0 <= y && y < this.rows) && (this.board[y][x].cellType !== 'obstacle')) {
            this.board[y][x].agentValue = agentValue
            return true
        }
        return false
    }

    isOnExit() {
        return this.board[this.playerPos.y][this.playerPos.x].cellType === 'exit'
    }

    setObstacle(x, y) {
        if (this.isLocationValid(x, y)) {
            this.board[y][x] = {
                cellType: 'obstacle',
                value: -100,
                agentValue: undefined
            }
            this.dispatchEvent('add_obstacle', { x, y })
            return true
        }
        return false
    }

    move(command) {
        switch (command) {
            case 'UP':
                return this.setPlayerPos(this.playerPos.x, this.playerPos.y - 1)
            case 'DOWN':
                return this.setPlayerPos(this.playerPos.x, this.playerPos.y + 1)
            case 'LEFT':
                return this.setPlayerPos(this.playerPos.x - 1, this.playerPos.y)
            case 'RIGHT':
                return this.setPlayerPos(this.playerPos.x + 1, this.playerPos.y)
            default:
                console.log(command)
                console.error("Invalid Action Move!")
        }
    }

    addListener(eventName, listener) {
        this.eventListeners.push({
            eventName, listener
        })
    }

    dispatchEvent(eventName, payload) {
        this.eventListeners.filter((l) => l.eventName === eventName).forEach(
            ({ listener }) => listener(payload)
        )
    }

    isLocationValid(x, y) {
        if ((0 <= x && x < this.cols && 0 <= y && y < this.rows) && (this.board[y][x].cellType !== 'player' && this.board[y][x].cellType !== 'exit' && this.board[y][x].cellType !== 'obstacle')) {
            return true
        }
        return false
    }

    clone() {
        const clone = new Board(this.rows, this.cols)
        clone.board = [...this.board]
        return clone
    }
}

export default Board