import React from "react"


function ContextMenuItemGroup({children, isLast = false}) {
    return (
        <div className="flex flex-col gap-6 md:gap-3 text-[1rem] md:text-sm">
            {children}
            {!isLast && <hr className="dark:bg-neutral-800 dark:border-neutral-800 mb-6 md:m-1 md:mb-3"/>}
        </div>
    )
}

export default ContextMenuItemGroup
