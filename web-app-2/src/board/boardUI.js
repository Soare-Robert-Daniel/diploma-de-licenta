import Board from './board'
import Konva from 'konva'

class BoardUI {
    /**
     * 
     * @param {Board} board 
     * @param {Konva.Stage} stage
     */
    constructor(board, stage) {
        this.board = board
        this.stage = stage

        this.mapLayer = new Konva.Layer()
        this.valueLayer = new Konva.Layer()
        this.playerLayer = new Konva.Layer()
        this.pathLayer = new Konva.Layer()
        this.agentValuesLayer = new Konva.Layer()

        this.stage.add(this.mapLayer)
        this.stage.add(this.playerLayer)
        // this.stage.add(this.valueLayer)
        // this.stage.add(this.pathLayer)
        // this.stage.add(this.agentValuesLayer)

        this.cellWidth = Math.round(this.stage.width() / this.board.cols)
        this.cellHeight = Math.round(this.stage.height() / this.board.rows)

        this.playerCell = undefined
        this.obstacleCells = []
    }

    createBoard() {
        if (this.board === undefined || this.stage === undefined) {
            throw `Unitialized board: ${this.board}  or state: ${this.stage}`
        }

        this.board.board.forEach((row, rowIdx) => {
            row.forEach((cellInfo, colIdx) => {
                //console.log(cellInfo, colIdx, rowIdx, this.cellHeight, this.cellWidth)

                if (cellInfo.cellType === 'empty') {
                    const cell = new Konva.Rect({
                        id: `empty_${colIdx}x${rowIdx}`,
                        x: colIdx * this.cellWidth,
                        y: rowIdx * this.cellHeight,
                        fill: '#aaa',
                        width: this.cellWidth,
                        height: this.cellHeight,
                        stroke: 'black',
                        strokeWidth: 1
                    })
                    this.mapLayer.add(cell)
                } else if (cellInfo.cellType === 'player') {
                    const cell = new Konva.Rect({
                        id: `empty_${colIdx}x${rowIdx}`,
                        x: colIdx * this.cellWidth,
                        y: rowIdx * this.cellHeight,
                        fill: '#aaa',
                        width: this.cellWidth,
                        height: this.cellHeight,
                        stroke: 'black',
                        strokeWidth: 1
                    })
                    this.mapLayer.add(cell)

                } else if (cellInfo.cellType === 'exit') {
                    const cell = new Konva.Rect({
                        id: 'exit',
                        x: colIdx * this.cellWidth,
                        y: rowIdx * this.cellHeight,
                        fill: '#564787 ',
                        width: this.cellWidth,
                        height: this.cellHeight,
                        stroke: 'black',
                        strokeWidth: 1
                    })
                    this.mapLayer.add(cell)
                }
            })
        })

        this.playerCell = new Konva.Circle({
            id: 'player',
            x: this.board.playerPos.x * this.cellWidth + this.cellWidth / 2,
            y: this.board.playerPos.y * this.cellHeight + this.cellHeight / 2,
            radius: Math.min(this.cellHeight, this.cellWidth) * 0.5,
            fill: '#2B59C3',
            width: this.cellWidth,
            height: this.cellHeight,
            stroke: 'black',
            strokeWidth: 1
        })
        this.playerLayer.add(this.playerCell)

        // console.log(this.mapLayer)
        this.mapLayer.draw()
        this.playerLayer.draw()

        this.board.addListener('player', (playerPos) => {
            // console.log('redraw player', playerPos)
            this.playerCell.x(playerPos.x * this.cellWidth + this.cellWidth / 2)
            this.playerCell.y(playerPos.y * this.cellHeight + this.cellHeight / 2)
            this.playerLayer.draw()
        })

        this.board.addListener('add_obstacle', (obsPos) => {
            console.log('Add Obs', obsPos)
            const cell = this.stage.find(`#empty_${obsPos.x}x${obsPos.y}`)[0]
            if (cell) {
                cell.destroy()
                this.mapLayer.draw()
            } else {
                console.error(cell)
            }
        })

        this.board.addListener('reset', () => {
            console.log('Reset')
            this.reset()
        })
    }

    reset() {
        this.mapLayer.destroy()
        this.playerLayer.destroy()
        this.valueLayer.destroy()
        this.pathLayer.destroy()

        this.mapLayer = new Konva.Layer()
        this.valueLayer = new Konva.Layer()
        this.playerLayer = new Konva.Layer()
        this.pathLayer = new Konva.Layer()
        this.agentValuesLayer = new Konva.Layer()

        this.stage.add(this.mapLayer)
        this.stage.add(this.valueLayer)
        this.stage.add(this.playerLayer)
        this.stage.add(this.pathLayer)
        this.stage.add(this.agentValuesLayer)

        this.createBoard()
    }

    draw() {
        this.mapLayer.draw()
        this.playerLayer.draw()
        this.valueLayer.draw()
        this.pathLayer.draw()
    }

    getLayers() {
        return [
            this.mapLayer,
            this.valueLayer,
            this.playerLayer,
            this.pathLayer,
            this.agentValuesLayer,
        ]
    }
}

export default BoardUI