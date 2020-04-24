import React, { useState, useEffect, Fragment } from 'react'
import { CardFetcherType, ProcessingCard } from '../data/card_fetcher'
import { LockFetcherType } from '../data/lock_fetcher'

export function ProcessingPage({ card_fetcher, lockFetcher }: { card_fetcher: CardFetcherType, lockFetcher: LockFetcherType }) {
    const [locks, setLocks] = useState<string[]>([])
    const [cards, setCards] = useState<ProcessingCard[]>([])
    const [failed, setFailed] = useState<ProcessingCard[]>([])
    const [todo, setTodo] = useState<ProcessingCard[]>([])
    const [done, setDone] = useState<ProcessingCard[]>([])
    const [running, setRunning] = useState<ProcessingCard[]>([])
    const [error, setError] = useState('')

    async function refresh() {
        try {
            const p_cards = card_fetcher.listProcessing()
            const p_locks = lockFetcher.getLocks()
            setCards(await p_cards)
            setLocks(await p_locks)
        } catch (e) {
            setError(e.message)
        }
    }

    function isLocked(x: string | undefined) {
        if (!x) {
            return false
        }
        return locks.includes(x)
    }

    function isRunning(x: string) {
        return running.filter(y => y.properties.path == x).length > 0
    }

    useEffect(() => {
        setFailed(cards.filter(x => x.properties.status == 'failed'))
        setTodo(cards.filter(x => [null, undefined, '', 'todo'].includes(x.properties.status)))
        setDone(cards.filter(x => x.properties.status == 'done'))
        setRunning(cards.filter(x => x.properties.status == 'running'))
    }, [cards])

    useEffect(() => {
        refresh()
    }, [])

    return <div>
        {(error) ?
            <span style={{ color: 'red' }}>Error: {error}</span>
            : <Fragment />}

        <div style={{ textAlign: "right" }}>
            <button
                className="button btn btn-primary"
                onClick={refresh}
            >Refresh</button>
        </div>

        <h2>Todo - {todo.length}</h2>
        <ul>
            {todo.map(x => (
                <li key={x.id}>
                    {x.id} - {x.properties.path}
                </li>
            ))}
        </ul>

        <h2>Running - {running.length}</h2>
        <ul>
            {running.map(x => (
                <li key={x.id}>
                    {x.id} - {x.properties.path} - {
                        isLocked(x.properties.path) ?
                            <span>locked</span>
                            : <span style={{ color: 'red' }}>not locked</span>
                    }
                </li>
            ))}
        </ul>

        <h2>Locks - {locks.length}</h2>
        <ul>
            {locks.map(x => (
                <li key={x}>
                    {x} - {
                        isRunning(x) ?
                            <span>running</span>
                            : <span style={{ color: 'red' }}>not running</span>
                    }
                </li>
            ))}
        </ul>

        <h2>Failed - {failed.length}</h2>
        <ul>
            {failed.map(x => (
                <li key={x.id}>
                    {x.id} - {x.properties.path}
                </li>
            ))}
        </ul>

        <h2>Done - {done.length}</h2>
        <ul>
            {done.map(x => (
                <li key={x.id}>
                    {x.id} - {x.properties.path}
                </li>
            ))}
        </ul>
    </div>
}