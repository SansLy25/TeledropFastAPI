import React from "react"


function ContextMenuItem({text, Icon = null}) {
    return <div className="flex flex-row w-full justify-between items-center">
        <span>{text}</span>
        {<Icon/> ? Icon: ""}
    </div>
}

export default ContextMenuItem