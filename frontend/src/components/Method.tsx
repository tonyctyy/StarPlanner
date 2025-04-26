/**
 * Methods.tsx
 * 
 * Renders the methods section.
 * 
 * Displays method name and related subjects. 
 * Can expand method to show details.
 * Implements Method generator column.
 *
 * @key Displays method info
 * @key Expandable details 
 * @key Method generator column
*/

import React from 'react';
import { useState } from 'react';
import { Separator, BlockTitle } from './Utils';

import 'react-circular-progressbar/dist/styles.css';
import { MDBCol, MDBContainer, MDBRow } from 'mdb-react-ui-kit';
import moment from 'moment';
import { Method } from '../Interface';
import styles from '../styles/styles.module.css';
import { getSize } from './Responsive';
import { Generator, IElement } from './Column';
import { nanoid } from 'nanoid';
import { camelCase, filter } from 'lodash';



export default function MethodContent({ methods, dndData, setDndData }: { methods: Method[], dndData: IElement[], setDndData: React.Dispatch<React.SetStateAction<IElement[]>> }) {
    const [expanded, setExpanded] = useState<number[]>([]);

    function isExpanded(method: Method) {
        return expanded.includes(method.id);
    }

    function toggleExpanded(method: Method) {
        if (isExpanded(method)) {
            setExpanded(expanded.filter((id) => id !== method.id));
        } else {
            setExpanded([...expanded, method.id]);
        }
    }

    const handleGeneratorMount = (name: string, col: string) => {
        if (dndData.some(elm => elm.content === name && elm.column === col)) {
            // console.log('already exists')
            return;
        }


        const newElement = {
            id: nanoid(),
            content: name,
            column: col,
            shouldCopy: true,
            color: '#c4c3f5',
        };
        setDndData(prevData => [...prevData, newElement]);
    };


    return (
        <MDBContainer>
            <BlockTitle titles={['', '相關科目']} />
            <Separator thickness={4} />
            <MDBContainer>
                {methods.map((method, index) => {
                    return (
                        <div key={nanoid()}>
                            <MDBRow
                                onClick={() => toggleExpanded(method)}
                                style={{ cursor: 'pointer', }}
                            >
                                {index !== 0 && <Separator thickness={2} />}
                                <MDBCol className={`section-content ${getSize()}`}>
                                    <Generator
                                        key={`method-column-${method.name}${index}`}

                                        heading={`method-column-${method.name}${index}`}
                                        elements={filter(dndData, (elm) =>
                                            elm.column === camelCase(`method-column-${method.name}${index}`)
                                        )}
                                        title={method.name}
                                        col={camelCase(`method-column-${method.name}${index}`)}
                                        onMount={handleGeneratorMount}
                                    />
                                    
                                </MDBCol>
                                <MDBCol className={`section-content ${getSize()}`}>
                                    <span style={{
                                        textAlign: 'center',
                                        justifyContent: 'center',
                                        width: '100%',
                                    }}>
                                        {method.subject.map((subject, index) => {
                                            return (
                                                <div key={nanoid()}>
                                                    {index != 0 && <>/</>}{subject.name_chin}
                                                </div>
                                            )
                                        })}
                                    </span>
                                </MDBCol>

                            </MDBRow>
                            {isExpanded(method) &&
                                <MDBRow>
                                    <MDBContainer>
                                        描述：{method.description}
                                    </MDBContainer>
                                    <br />
                                </MDBRow>}
                        </div>
                    )
                })}
            </MDBContainer>
        </MDBContainer>)
}

// const styles = {
//     method: {

//         paddingBottom: 0,
//         marginBottom: 0,
//         justifyItems: 'center',
//         justifyContent: 'space-between',
//         alignItems: 'center',
//         display: 'flex',


//     },

//     background: {
//         background: '#e6f7ff',
//         borderRadius: 10,
//         padding: 20,
//         marginTop: 20,


//     },

//     title: {
//         fontWeight: 'bold',

//         left: '20px',
//     },

//     col: {
//         minWidth: 432,
//     },

//     tag: {
//         borderRadius: 10,
//         width: 'fit-content',
//         height: 'fit-content',
//     },


//     goalTag: {
//         background: '#f5c3c4',
//         borderRadius: 10,
//         width: 'fit-content',
//         height: 'fit-content',
//     },
//     taskTag: {
//         background: '#c3f5c4',
//         borderRadius: 10,
//         width: 'fit-content',
//         height: 'fit-content',
//     },
//     methodTag: {
//         background: '#c4c3f5',
//         borderRadius: 10,
//         width: 'fit-content',
//         height: 'fit-content',
//     },
//     tagRow: {
//         justifyContent: 'space-between',
//     },

// }
