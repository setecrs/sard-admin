import React, { Fragment, useState } from 'react'

import { Worker } from '../data/fetcher'

export function WorkerList({ workers, isLocked, isRunning }: { workers: Worker[], isLocked: (x: string | undefined) => boolean, isRunning: (x: string | undefined) => boolean }) {
  return <ul>
    {workers
      .sort((a, b) => a.node_name.localeCompare(b.node_name))
      .map(w => (
        <li key={w.node_name}>
          <OneWorker worker={w} isLocked={isLocked} isRunning={isRunning} />
        </li>
      ))}
  </ul>
}

export function OneWorker({ worker, isLocked, isRunning }: { worker: Worker, isLocked: (x: string | undefined) => boolean, isRunning: (x: string | undefined) => boolean }) {
  const [expanded, setExpanded] = useState(false)
  const header = <Fragment>
    {worker.node_name}
    {" - "}
    {worker.name}
    {" - "}
    {worker.evidence ?
      <Fragment>
        worker.evidence
        {" - "}
        {isRunning(worker.evidence) ?
          <span style={{ color: 'green' }}>running</span>
          : <span style={{ color: 'red' }}>not running</span>}
        {" - "}
        {isLocked(worker.evidence) ?
          <span style={{ color: 'green' }}> locked</span>
          : <span style={{ color: 'red' }}>not locked</span>}
      </Fragment>
      : 'no evidence'}

  </Fragment>
  return <Fragment>
    {(expanded) ?
      <span onClick={() => setExpanded(!expanded)}>
        - {header}
        <div> Host name: {worker.node_name} </div>
        <div> Host IP: {worker.host_ip} </div>
        <div> Image: {worker.image} </div>
        <div> Pod name: {worker.name} </div>
        <div> Pod IP: {worker.pod_ip} </div>
        <div> Ready: {worker.ready.toString()} </div>
        <div> Evidence: {worker.evidence} </div>
      </span>
      : <span onClick={() => setExpanded(!expanded)}>
        + {header}
      </span>
    }
  </Fragment>
}