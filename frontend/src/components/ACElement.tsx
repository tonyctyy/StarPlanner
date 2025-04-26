import React, { FC } from 'react';
import {styled} from '@stitches/react';
import { MDBRow, MDBCol } from 'mdb-react-ui-kit';
import { Separator } from './Utils';




export const AC_Element = () => {
    interface ACElement {
        content: string;
        bgColor?: string;
        textColor?: string;
    }
    
    const Element: FC<ACElement> = ({content, bgColor, textColor  }) => {
        const ElementWrapper = styled("div", {
            background: bgColor?bgColor:"#f6f6f6",
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
        const ElementText = styled("h3", {
            color: textColor?textColor:"#000",
            fontSize: "1rem",
            fontWeight: 600,
            textWrap: "wrap",
            textAlign: "center",
            textJustify: "center",
        
        });
        return (
            <ElementWrapper>
                <ElementText>{content}</ElementText>
            </ElementWrapper>
        );
    }
    const colors = [
        "#FFA69E", // Coral
        "#A4E4B5", // Mint Green
        "#F4A261", // Orange
        "#FFDDC1", // Peach
        "#E9C46A", // Mustard
        "#70C1B3", // Turquoise


    ];
    
    const textColors = [
        "#452E3C", // Dark Purple
        "#153243", // Dark Blue
        "#011627", // Dark Purple
        "#4A4E69", // Charcoal
        "#264653", // Dark Teal
        "#011627", // Navy Blue

    ];

    

    const content = [
        "學習策略",
        "目標設定",
        "組織管理",
        "動機與責任",
        "時間管理",
        "生活平衡"
    ]

    return (
        <>
            {colors.map((color, index) => (
            <>
                <MDBRow>
                    <MDBCol>
                        <Element content={content[index]} bgColor={color} textColor={textColors[index]}/>
                    </MDBCol>
                </MDBRow>
                <Separator thickness={3}/>
            </>
        ))}
        </>
        // <>
        // <MDBRow>
        //     <MDBCol>
        //         <Element content="學習策略" color="#9893DA"/>
        //     </MDBCol>
        // </MDBRow>

        // <Separator thickness={3}/>

        // <MDBRow>
        //     <MDBCol>
        //         <Element content="目標設定" color="#F96F5D"/>
        //     </MDBCol>
        // </MDBRow>   

        // <Separator thickness={3}/>

        // <MDBRow>
        //     <MDBCol>
        //         <Element content="組織管理" color="#F9C784"/>
        //     </MDBCol>
        // </MDBRow>

        // <Separator thickness={3}/>

        // <MDBRow>
        //     <MDBCol>
        //         <Element content="動機與責任" color="#F9C784"/>
        //     </MDBCol>
        // </MDBRow>

        // <Separator thickness={3}/>

        // <MDBRow>
        //     <MDBCol>
        //         <Element content="時間管理" color="#6DD3CE"/>
        //     </MDBCol>
        // </MDBRow>

        // <Separator thickness={3}/>
        
        // <MDBRow>
        //     <MDBCol>
        //         <Element content="生活平衡" color="#F9C784"/>
        //     </MDBCol>
        // </MDBRow>
        // </>
    );
};
