import React, {useContext} from "react"
import ContextMenuItem from "./ContextMenuItem.jsx";
import {MenuRadioContext} from "./ContextMenuRadioGroup.jsx"

function ContextMenuRadioButton({value, ...props}) {
    const {currentValue, onChange} = useContext(MenuRadioContext);

    return <ContextMenuItem active={value === currentValue} onClick={() => onChange(value)} {...props}/>
}

export default ContextMenuRadioButton
