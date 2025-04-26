/**
 * DraggableElement.tsx
 * 
 * Renders a draggable element for the calendar tasks.
 * 
 * Wraps the element text in a Draggable component from react-dnd. 
 * Implements styled component for the wrapper.
 *  
 * @key Renders draggable element
 * @key Wraps element in Draggable 
 * @key Implements wrapper styled component
*/

import React,{ FC, useMemo } from "react";
import { styled } from "@stitches/react";
import ReactDOM from "react-dom";
import { Draggable } from "../primitives/Draggable";

interface IDraggableElement {
    identifier: string;
    content: string;
    color?: string;
}

export const DraggableElement: FC<IDraggableElement> = ({
    identifier,
    content,
    color,
}) => {
    const itemIdentifier = useMemo(() => identifier, [identifier]);

    const ElementWrapperStyle = {
        background: color ? color : "#f6f6f6",
        
    }
    const ElementWrapper = styled("div", {
        background: color?color:"#f6f6f6",
        borderRadius: 3,
        height: "fit-content",
        width: "100%",
        display: "flex",
        justifyContent: "center",
        textAlign: "center",
        textJustify: "center",
        alignItems: "center",
        marginBottom: 5,
        marginTop: 5,
        border: "solid 1px #000",
        padding: 5,
        fontFamily: "sans-serif"
    });

    return (
        <Draggable id={itemIdentifier}>
            <ElementWrapper >
                <ElementText>{content}</ElementText>
            </ElementWrapper>
        </Draggable>
    );
};



const ElementText = styled("h3", {
    fontSize: 12,
    fontWeight: 600,
    textWrap: "wrap",
    textAlign: "center",
    textJustify: "center",

});