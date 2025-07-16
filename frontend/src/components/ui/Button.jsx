import React from "react";

function Button({ children, className, ...props }) {
    return (
        <button className={`font-medium text-[0.8rem] items-center px-1.5 py-1.5 gap-1 justify-center flex flex-row ${className}`} {...props}>
            {children}
        </button>

    )
}

export default Button;