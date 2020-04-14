import React, { Fragment } from "react";

export function Errors({ errors }: { errors: any[]}) {
    if (!errors || errors.length === 0){
        return <Fragment></Fragment>
    }
    return <Fragment>
        <h2>Errors:</h2>
        <ul>
            {errors.map((x:any, i:number) =>
                <li key={i}>
                    {x.toString()}
                </li>
            )}
        </ul>

    </Fragment>
}