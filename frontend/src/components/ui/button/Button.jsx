import React from "react";

function Button({ children, className, ...props }) {
    return (
        <button className={
            `font-medium hover:cursor-pointer
             text-[0.8rem] items-center px-1.5
             py-1.5 md:py-2 gap-1 justify-center
             flex flex-row shadow-md ${className}`
        } {...props}
        >
            {children}
        </button>

    )
}

export default Button;