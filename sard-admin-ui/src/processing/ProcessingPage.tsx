import React, { useState, useEffect, Fragment } from 'react'
import { CardFetcherType, ProcessingCard } from '../data/card_fetcher'
import { LockFetcherType } from '../data/lock_fetcher'
import { FetcherReturn, Worker } from '../data/fetcher'
import { WorkerList } from './WorkerList'
import { RestartButton } from './RestartButton'

export function ProcessingPage({ fetcher, card_fetcher, lockFetcher }: { fetcher: FetcherReturn, card_fetcher: CardFetcherType, lockFetcher: LockFetcherType }) {
    const [locks, setLocks] = useState<string[]>([])
    const [cards, setCards] = useState<ProcessingCard[]>([])
    const [failed, setFailed] = useState<ProcessingCard[]>([])
    const [todo, setTodo] = useState<ProcessingCard[]>([])
    const [done, setDone] = useState<ProcessingCard[]>([])
    const [running, setRunning] = useState<ProcessingCard[]>([])
    const [workers, setWorkers] = useState<Worker[]>([])
    const [error, setError] = useState('')

    async function refresh() {
        try {
            const p_cards = card_fetcher.listProcessing()
            const p_locks = lockFetcher.getLocks()
            const p_workers = fetcher.listWorkers()
            try {
                const _cards = await p_cards
                setCards(_cards.sort((a, b) => a.id.localeCompare(b.id)))
            } catch (e) {
                console.log({e})
                setError("could not retrieve cards: " + e.stack)
            }
            try {
                const _locks = await p_locks
                setLocks(_locks.sort())
            } catch (e) {
                console.log({e})
                setError("could not retrieve locks: " + e.stack)
            }
            try {
                const _workers = await p_workers
                setWorkers(_workers.sort((a, b) => a.node_name.localeCompare(b.node_name)))
            } catch (e) {
                console.log({e})
                setError("could not retrieve workers: " + e.stack)
            }
        } catch (e) {
            console.log({e})
            setError(e.message)
        }
    }

    function isLocked(x: string | undefined) {
        if (!x) {
            return false
        }
        return locks.includes(x)
    }

    function isRunning(x: string | undefined) {
        if (!x) {
            return false
        }
        return running.filter(y => y.properties.path === x).length > 0
    }

    function inWorker(x: string | undefined) {
        if (!x) {
            return false
        }
        return workers.filter(w => w.evidence === x).length > 0
    }

    useEffect(() => {
        setFailed(cards.filter(x => x.properties.status === 'failed'))
        setTodo(cards.filter(x => [null, undefined, '', 'todo'].includes(x.properties.status)))
        setDone(cards.filter(x => x.properties.status === 'done'))
        setRunning(cards.filter(x => x.properties.status === 'running'))
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

        <h3>Todo - {todo.length}</h3>
        <ul>
            {todo.map(x => (
                <li key={x.id}>
                    {x.id} - {x.properties.path}
                </li>
            ))}
        </ul>

        <h3>Running - {running.length}</h3>
        <ul>
            {running.map(x => (
                <li key={x.id}>
                    {x.id}
                    {" - "}
                    {x.properties.path}
                    {" - "}
                    {isLocked(x.properties.path) ?
                        <span style={{ color: 'green' }}>locked</span>
                        : <span style={{ color: 'red' }}>not locked</span>}
                    {" - "}
                    {inWorker(x.properties.path) ?
                        <span style={{ color: 'green' }}>in worker</span>
                        : <span style={{ color: 'red' }}>not in worker</span>}
                </li>
            ))}
        </ul>

        <h3>Locks - {locks.length}</h3>
        <ul>
            {locks.map(x => (
                <li key={x}>
                    {x}
                    {" - "}
                    {isRunning(x) ?
                        <span style={{ color: 'green' }}>running</span>
                        : <span style={{ color: 'red' }}>not running</span>}
                    {" - "}
                    {inWorker(x) ?
                        <span style={{ color: 'green' }}>in worker</span>
                        : <span style={{ color: 'red' }}>not in worker</span>}
                </li>
            ))}
        </ul>

        <h3>IPED workers - {workers.length}</h3>
        <WorkerList workers={workers} isRunning={isRunning} isLocked={isLocked} />

        <h3>Failed - {failed.length}</h3>
        <ul>
            {failed.map(x => (
                <li key={x.id}>
                    {x.id} - {x.properties.path}
                    {'  '}
                    {
                        (x.properties.path) ? <RestartButton
                            imagepath={x.properties.path || ''}
                            folders_count={fetcher.folders_count}
                            folders_rename={fetcher.folders_rename}
                        />
                            : ''
                    }
                </li>
            ))}
        </ul>

        <h3>Done - {done.length}</h3>
        <ul>
            {done.map(x => (
                <li key={x.id}>
                    {x.id} - {x.properties.path}
                </li>
            ))}
        </ul>
    </div>
}