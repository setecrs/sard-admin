import React, { Fragment, useState } from 'react'

import { Worker } from '../data/fetcher'

export function WorkerList({ workers }: { workers: Worker[] }) {
  return <ul>
    {workers
      .sort((a, b) => a.node_name.localeCompare(b.node_name))
      .map(w => (
        <li key={w.node_name}>
          <OneWorker worker={w} />
        </li>
      ))}
  </ul>
}

export function OneWorker({ worker }: { worker: Worker }) {
  const [expanded, setExpanded] = useState(false)
  return <Fragment>
    {(expanded) ?
      <span onClick={() => setExpanded(!expanded)}>
        - {worker.node_name} - {worker.name} - {worker.evidence || 'no evidence'}
        <div> Host name: {worker.node_name} </div>
        <div> Host IP: {worker.host_ip} </div>
        <div> Image: {worker.image} </div>
        <div> Pod name: {worker.name} </div>
        <div> Pod IP: {worker.pod_ip} </div>
        <div> Ready: {worker.ready.toString()} </div>
        <div> Evidence: {worker.evidence} </div>
      </span>
      : <span onClick={() => setExpanded(!expanded)}>
        + {worker.node_name} - {worker.name} - {worker.evidence || 'no evidence'}
      </span>
    }
  </Fragment>
}