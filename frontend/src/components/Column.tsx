/** 
 * Column.tsx
 * 
 * Renders a column component for the calendar tasks drag and drop.
 * 
 * It has a header and renders DraggableElement components inside a Droppable area.
 * Implements styled components for layout.
 * 
 * @key Renders column layout 
 * @key Wraps DraggableElements in Droppable
 * @key Implements column styled components
*/

import React, { useEffect } from "react";
import { FC, useMemo } from "react";
import { styled } from "@stitches/react";
import _ from "lodash";
import { Droppable } from "../primitives/Droppable";
import { DraggableElement } from "./DraggableElement";
import { nanoid } from "nanoid";
import moment from "moment";

export interface IElement {
    id: string;
    content: string;
    column?: string;
    shouldCopy: boolean;
    color?: string;
}

interface IColumn {
    heading: string;
    title?: string;
    elements: IElement[];
    overCol?: string | null;
}

interface IGenerator {
    heading: string;
    title: string;
    elements: IElement[];
    col: string;
    onMount: (title: string, col: string) => void;
}



export const Column: FC<IColumn> = ({ heading, elements, overCol }) => {
    const columnIdentifier = useMemo(() => _.camelCase(heading), [heading]);

    const amounts = useMemo(
        () => elements.filter((elm) => elm.column === columnIdentifier).length,
        [elements, columnIdentifier]
    );

    const ColumnDroppableWrapper = styled("div", {
        padding: 3,
    });

    const ColumnWrapper = styled("div", {
        width: "12.5%",
        padding: 0,
        border: "solid #CCC",
        borderWidth: 0.5,
        borderRadius: 0,
        background: overCol === columnIdentifier ? "#CCCC" : "transparent",
        

    });

    return (
        <ColumnWrapper>
            <ColumnHeaderWrapper variant={columnIdentifier === "overdue"
                ? "overdue"
                : columnIdentifier === moment().format('DDMddd')
                    ? "today" :
                    "default"}>
                <Heading>
                    {heading}
                </Heading>
            </ColumnHeaderWrapper>
            <ColumnDroppableWrapper

            >
                <Droppable id={columnIdentifier}>
                    {elements.map((elm, elmIndex) => (

                        <DraggableElement
                            key={`draggable-element-${elmIndex}-${columnIdentifier}`}
                            identifier={elm.id}
                            content={elm.content}
                            color={elm.color}
                        />
                    ))}
                    <DropPlaceholder />
                </Droppable>
            </ColumnDroppableWrapper>
        </ColumnWrapper>
    );
};

export const Generator: FC<IGenerator> = ({ heading, title, elements, col, onMount }) => {
    const columnIdentifier = useMemo(() => _.camelCase(heading), [heading]);

    const amounts = useMemo(
        () => elements.filter((elm) => elm.column === columnIdentifier).length,
        [elements, columnIdentifier]
    );

    useEffect(() => {
        onMount(title, columnIdentifier);
    }, [])

    const ColumnDroppableWrapper = styled("div", {
        padding: 3,
        width: "100%",

    });
    if (elements.length > 0) {
        elements = elements.slice(0, 1)
    }

    return (
        <GeneratorWrapper>
            <ColumnDroppableWrapper>

                {elements.map((elm, elmIndex) => (
                    <div key={nanoid()}>
                        {
                            <DraggableElement
                                key={`draggable-element-${elmIndex}-${columnIdentifier}`}
                                identifier={elm.id}
                                content={elm.content}
                                color={elm.color}
                            />

                        }
                    </div>
                ))}
            </ColumnDroppableWrapper>
        </GeneratorWrapper>
    );
};



const GeneratorWrapper = styled("div", {
    width: "100%",
    position: "absolute",
    height: "100%",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
});



const Heading = styled("h3", {
    color: "#FFF",
    margin: 'auto 0',
    textAlign: "center",
    justifyContent: "center",
    alignItems: "center",
    fontSize:  18 ,
    height: "30%",

});





const DropPlaceholder = styled("div", {
    height: 35,
    backgroundColor: "transparent",
    marginTop: 15,
});


const ResponsiveColumnWrapper = styled("div", {
    variants: {
        variant: {
            phone: {
                fontSize: 12,
            },
            tablet: {
                fontSize: 14,
            },
            desktop: {
                fontSize: 16,
            },
        }
    }
})

const ColumnHeaderWrapper = styled("span", {
    display: "flex",
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    justifyItems: "center",
    textAlign: "center",
    textAlignLast: "center",
    defaultVariants: {
        variant: 'default',
    },
    variants: {
        variant: {
            default: { background: "#249CD1CC", },
            overdue: {
                background: "#FF0000CC",
            },
            today: {
                background: "#24A19CCC",
            },
        },

    },

    margin: 0,
    padding: 10,
    borderRadius: 0,
    width: "100%",
});

const ColumnTasksAmount = styled("span", {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    width: 30,
    height: 30,
    borderRadius: 6,
    color: "#FFF",
    background: "rgba( 255, 255, 255, 0.25 )",
    boxShadow: "0 8px 32px 0 rgba( 255, 255, 255, 0.18 )",
    backdropFilter: "blur(5px)",
    border: "1px solid rgba( 255, 255, 255, 0.18 )",
});