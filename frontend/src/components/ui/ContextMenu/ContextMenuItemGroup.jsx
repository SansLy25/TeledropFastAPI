import React from "react"


function ContextMenuItemGroup({children, isLast = false}) {
    return (
        <div className="flex flex-col gap-1.5">
            {children}
            {!isLast && <hr className="dark:bg-neutral-800 dark:border-neutral-800 m-1"/>}
        </div>
    )
}

export default ContextMenuItemGroup
