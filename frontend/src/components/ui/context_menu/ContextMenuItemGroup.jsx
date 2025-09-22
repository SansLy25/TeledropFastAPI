import React from "react"


function ContextMenuItemGroup({children, isLast = false}) {
    return (
        <div className="flex flex-col gap-2 md:gap-0.5 text-[1rem] md:text-sm">
            {children}
            {!isLast && <hr className="dark:bg-neutral-800 dark:border-neutral-800 mb-6 md:m-1 md:mb-2"/>}
        </div>
    )
}

export default ContextMenuItemGroup
