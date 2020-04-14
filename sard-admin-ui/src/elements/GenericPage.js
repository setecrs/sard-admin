import React from 'react'

export function GenericPage({
    elemCreate,
    elemList,
    elemDetail,

}) {
    return <div className="container">
        {elemCreate}
        <div className="row my-3 p-3">
            <div className="col-md-3">
                {elemList}
            </div>
            <div className="col-md-9">
                {elemDetail}
            </div>
        </div>
    </div>
}