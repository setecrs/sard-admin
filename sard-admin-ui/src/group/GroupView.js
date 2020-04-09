import React, { Fragment } from 'react';

function GroupView({groups}) {
    return <Fragment>
        <ul>
            {(groups||[]).map((x,i) => {
                return <li key={i}>
                    {x}
                </li>
            })}
        </ul>
    </Fragment>
}

export default GroupView