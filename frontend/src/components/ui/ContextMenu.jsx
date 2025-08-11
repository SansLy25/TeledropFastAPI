import React, { useState, useRef, useEffect } from 'react';
import { useMenuContext } from '../../contexts/MenuContext';

function ContextMenu({children, actionElement}) {
    const [actionElementSize, setActionElementSize] = useState({ width: 0, height: 0 });
    const actionElementRef = useRef(null);
    const { openMenuKey, setOpenMenuKey } = useMenuContext();

    const keyRef = useRef(Symbol("menu"));
    const menuRef = useRef(null);
    const isOpened = openMenuKey === keyRef.current;

    function onActionElementClick() {
        setOpenMenuKey(isOpened ? null : keyRef.current);
    }

    const enhancedActionElement = React.cloneElement(actionElement, {
        onClick: onActionElementClick,
        ref: actionElementRef,
    });

    useEffect(() => {
        if (actionElementRef.current) {
            const { offsetWidth, offsetHeight } = actionElementRef.current;
            setActionElementSize({ width: offsetWidth, height: offsetHeight });
        }
    }, [isOpened]);

    useEffect(() => {
        function handleClickOutside(e) {
            if (menuRef.current && !menuRef.current.contains(e.target)) {
                setOpenMenuKey(null);
            }
        }

        if (isOpened) {
            document.addEventListener("mousedown", handleClickOutside);
        }
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [isOpened, setOpenMenuKey]);

    return (
        <div className="relative">
            {enhancedActionElement}
            {isOpened && (
                <div
                    className="absolute size-10 rounded-xl bg-amber-100"
                    style={{ top: actionElementSize.height + 'px', left: "0",  zIndex: "9999"}}
                >
                    {children}
                </div>
            )}
        </div>
    );
}

export default ContextMenu;
