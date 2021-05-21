import { writable } from 'svelte/store';
import { v4 as uuidv4 } from 'uuid';

function createBordControlBusEvent() {
    const { subscribe, set, update } = writable([])

    return {
        subscribe,
        addEvent: (eventName, payload) => {
            update(s => [...s, { eventName, id: uuidv4(), payload }])
        },
        consumeEvent: (eventId) => {
            update(s => s.filter(({ id }) => id !== eventId))
        },
        consumeEvents: (eventsId) => {
            update(s => s.filter(({ id }) => !eventsId.includes(id)))
        },
        clear: () => set([])
    }
}

export const boardControlEvents = createBordControlBusEvent()

export const boardControlState = writable({
    movePlayer: false,
    addObstacle: false
})

export const analyticsData = writable({ boardData: [] })