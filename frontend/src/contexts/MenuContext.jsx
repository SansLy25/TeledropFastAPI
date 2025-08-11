import React, { createContext, useContext, useState } from 'react';

const MenuContext = createContext();

export function MenuProvider({ children }) {
    const [openMenuKey, setOpenMenuKey] = useState(null);
    return (
        <MenuContext.Provider value={{ openMenuKey, setOpenMenuKey }}>
            {children}
        </MenuContext.Provider>
    );
}

export function useMenuContext() {
    return useContext(MenuContext);
}