import React from "react"
import {Check} from "lucide-react"


function ContextMenuButton({text, icon = null, active = false, ...props}) {
    return (
        <button {...props} className={`flex p-2 rounded-xl flex-row w-full justify-between items-center ${ active ? "dark:bg-neutral-800 shadow-md" : ""}`}>
            <div className="flex flex-row justify-end items-center gap-6 md:gap-3.5">
                {icon}
                <span>{text}</span>
            </div>
            {active && <Check width="23px" height="23px" className="mr-2" />}
        </button>
    )
}

export default ContextMenuButton