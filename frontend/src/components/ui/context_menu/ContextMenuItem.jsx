import React from "react"
import {Check} from "lucide-react"


function ContextMenuItem({text, icon = null, active = false, ...props}) {
    return (
        <button {...props} className="flex flex-row w-full justify-between items-center">
            <span>{text}</span>
            <div className="flex flex-row justify-end items-center">
                {active && <Check width="23px" height="23px" className="mr-2" />}
                {icon}
            </div>
        </button>
    )
}

export default ContextMenuItem