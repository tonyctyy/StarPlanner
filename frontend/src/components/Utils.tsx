/**
 * Utils.tsx
 *
 * Shared UI utility components.
 * 
 * Exports Separator and BlockTitle components.
 * Implements responsive styled components.
 *
 * @key Separator component
 * @key BlockTitle component
 * @key Responsive styles  
*/


import { MDBCol, MDBRow } from 'mdb-react-ui-kit'
import React from 'react'
import { getSize } from './Responsive'
import "../styles/styles.css"
import { nanoid } from 'nanoid'

export function Separator({ thickness, margin }: { thickness: number, margin: number }) {
    return (
        <div style={{
            borderTop: `${thickness}px solid #ccc`,
            margin: `${margin}px 0`,
            width: '100%' as const,
        }}
        >
        </div>
    )
}

Separator.defaultProps = {
    thickness: 2,
    margin: 10,

}

export function BlockTitle({ titles }: { titles: string[] }) {
    return (
        <MDBRow>
            {titles.map((title) => (
                <MDBCol
                    className={`section-title ${getSize()}`}
                    key={nanoid()}
                >
                    <h5
                        className={`section-title ${getSize()}`}>{title}</h5>
                </MDBCol>
            ))}
        </MDBRow>
    )
}

