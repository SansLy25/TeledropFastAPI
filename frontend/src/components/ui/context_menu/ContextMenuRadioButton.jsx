import React, {useContext} from "react"
import ContextMenuButton from "./ContextMenuButton.jsx";
import {MenuRadioContext} from "./ContextMenuRadioGroup.jsx"

function ContextMenuRadioButton({value, ...props}) {
    const {currentValue, onChange} = useContext(MenuRadioContext);

    return <ContextMenuButton active={value === currentValue} onClick={() => onChange(value)} {...props}/>
}

export default ContextMenuRadioButton
