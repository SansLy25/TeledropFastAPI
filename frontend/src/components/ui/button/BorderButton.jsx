import React from "react";
import LargeContainer from "../../containers/LargeContainer.jsx";
import Button from "./Button.jsx";

function BorderButton({ children, className, ...props }) {
    return (
        <LargeContainer
            className="rounded-xl hover:dark:bg-neutral-800
                       transition-transform duration-200 ease-in-out
                       active:scale-95 hover:scale-102 touch-manipulation">
            <Button className={`w-full h-full ${className}`} {...props}>
                {children}
            </Button>
        </LargeContainer>
    );
}

export default BorderButton;