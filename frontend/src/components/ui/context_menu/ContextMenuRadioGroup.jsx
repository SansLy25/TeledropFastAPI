import React, {createContext} from "react"
import ContextMenuItemGroup from "./ContextMenuItemGroup.jsx";

export const MenuRadioContext = createContext();

function ContextMenuRadioGroup({value = "", onChange, isLast = false, ...props}) {
    return (
        <MenuRadioContext.Provider value={{currentValue: value, onChange}}>
            <ContextMenuItemGroup isLast={isLast} {...props}/>
        </MenuRadioContext.Provider>
    )
}

export default ContextMenuRadioGroup
