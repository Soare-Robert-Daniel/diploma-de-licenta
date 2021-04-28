class Board {
    constructor(numRows, numCols) {
        this.rows = numRows
        this.cols = numCols
        this.board = []

        this.initialize()
        this.playerPos = {
            x: 0,
            y: 0
        }

        this.eventListeners = []
    }

    reset() {
        this.initialize()
        this.dispatchEvent('reset')
    }

    initialize() {
        this.board = Array(this.rows).fill().map(() => Array(this.cols).fill({
            cellType: 'empty',
            value: 0,
            agentValue: undefined
        }))
        this.board[0][0] = {
            cellType: 'player',
            value: 0,
            agentValue: 0
        }

        this.board[this.rows - 1][this.cols - 1] = {
            cellType: 'exit',
            value: 100,
            agentValue: 0
        }

        this.playerPos = {
            x: 0,
            y: 0
        }
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

    playerReset() {
        this.setPlayerPos(0, 0)
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
        if ((0 <= x && x < this.cols && 0 <= y && y < this.rows) && (x !== this.cols - 1 && y !== this.rows) && (this.board[y][x].cellType !== 'player' && this.board[y][x].cellType !== 'exit' && this.board[y][x].cellType !== 'obstacle')) {
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
                console.error("Invalid Move!")
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
}

export default Board