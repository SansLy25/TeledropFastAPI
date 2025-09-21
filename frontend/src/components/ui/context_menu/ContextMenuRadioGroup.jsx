import React, {createContext, useState} from "react"
import ContextMenuItemGroup from "./ContextMenuItemGroup.jsx";

export const MenuRadioContext = createContext();

function ContextMenuRadioGroup({initialValue = "", onChange, ...props}) {
    let [currentValue, setValue] = useState(initialValue);


    return (
        <MenuRadioContext.Provider value={{currentValue, setValue}}>
            <ContextMenuItemGroup {...props}/>
        </MenuRadioContext.Provider>
    )
}

export default ContextMenuRadioGroup

