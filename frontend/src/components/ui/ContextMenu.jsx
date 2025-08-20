import React, { useState, useRef, useEffect } from 'react';
import { useMenuContext } from '../../contexts/MenuContext';

function ContextMenu({children, actionElement}) {
    const [actionElementSize, setActionElementSize] = useState({ width: 0, height: 0 });
    const actionElementRef = useRef(null);
    const { openMenuKey, setOpenMenuKey } = useMenuContext();

    const keyRef = useRef(null);
    const menuRef = useRef(null);

    useEffect(() => {
        if (keyRef.current === null) {
            keyRef.current = Symbol("menu");
        }
    }, []);

    const isOpened = openMenuKey === keyRef.current;

    function onActionElementClick() {
        if (openMenuKey === keyRef.current) {
            setOpenMenuKey(null);
        } else {
            setOpenMenuKey(keyRef.current);
        }
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
            <div
                ref={menuRef}
                className={`dark:bg-neutral-900 text-white rounded-2xl dark:border-[1.3px] dark:border-neutral-800 absolute w-60 h-96 transition-all duration-150 ease-in-out ${
                    isOpened 
                    ? "opacity-100 translate-y-0 scale-100" 
                    : "opacity-0 translate-y-1 scale-95 pointer-events-none"
                }`}
                style={{ top: (+actionElementSize.height + 5) + 'px', left: "0",  zIndex: "9999"}}
            >
                {children}
            </div>
        </div>
    );
}

export default ContextMenu;
