import { styled } from "@stitches/react";


export const Modal = styled("div", {
    background: '#eaf0fa',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 100,
    marginTop: '10px',
    width: '100%', // Adjust the percentage as needed
    padding: '20px', // Add padding for better spacing
})

export const MainWrapper = styled("div", {
    display: "flex",
    justifyContent: "center",
    height: "100%",
    width: "90%"
});

export const DnDWrapper = styled("div", {
    display: "flex",
    justifyContent: "space-evenly",
    backgroundColor: "#eef7ffff",
    paddingTop: 0,
    paddingBottom: 0,
    fontFamily: "Anek Telugu",
    borderRadius: 10,
    height: "100%",
    width: "100%"
});

export const contentStyle = {
    display: 'flex',
    flexDirection: 'row',
    flexWrap: 'nowrap',
    overflowX: 'auto',
    justifyContent: 'center',
    gap: 'calc(0.5%)',
    width: '98vw',
    top: 0,
    position: 'absolute',
}