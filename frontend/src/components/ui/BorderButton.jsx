import React from "react";
import LargeContainer from "../containers/LargeContainer.jsx";
import Button from "./Button.jsx";

function BorderButton({ children, className, ...props }) {
    return (
        <LargeContainer className="rounded-xl">
            <Button className={`w-full h-full ${className}`} {...props}>
                {children}
            </Button>
        </LargeContainer>
    );
}

export default BorderButton;