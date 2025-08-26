import React, { useState, useRef, useEffect } from 'react';
import { useMenuContext } from '../../contexts/MenuContext';

function ContextMenu({children, actionElement, borderElementRef}) {
    const [actionElementSize, setActionElementSize] = useState({ width: 0, height: 0 });
    const [menuPosition, setMenuPosition] = useState({ left: 0 });
    const [positionCalculated, setPositionCalculated] = useState(false);
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
        if (isOpened && menuRef.current && borderElementRef && borderElementRef.current) {
            const menuWidth = menuRef.current.offsetWidth;

            const borderRect = borderElementRef.current.getBoundingClientRect();
            const actionRect = actionElementRef.current.getBoundingClientRect();

            const actionRelativeLeft = actionRect.left - borderRect.left;
            const actionElementWidth = actionElementSize.width;

            const borderStyles = window.getComputedStyle(borderElementRef.current);
            const paddingLeft = parseFloat(borderStyles.paddingLeft);
            const paddingRight = parseFloat(borderStyles.paddingRight);

            const containerWidth = borderRect.width - paddingLeft - paddingRight;
            const actionRelativeLeftWithPadding = actionRelativeLeft - paddingLeft;

            let left = 0;

            if (actionRelativeLeftWithPadding + menuWidth > containerWidth) {
                left = containerWidth - menuWidth - (actionRelativeLeftWithPadding - left);

                if (left < -(actionElementWidth)) {
                    left = -(menuWidth - actionElementWidth);
                }
            }

            if (actionRelativeLeftWithPadding + left < 0) {
                left = -actionRelativeLeftWithPadding;
            }

            setMenuPosition({ left });
            setPositionCalculated(true);
        } else if (!isOpened) {
            setPositionCalculated(false);
        }
    }, [isOpened, actionElementSize, borderElementRef]);

    useEffect(() => {
        function handleClickOutside(e) {
            if (
                menuRef.current &&
                !menuRef.current.contains(e.target) &&
                !actionElementRef.current.contains(e.target)
            ) {
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
                    isOpened && positionCalculated
                    ? "opacity-100 translate-y-0 scale-100" 
                    : "opacity-0 translate-y-1 scale-95 pointer-events-none"
                }`}
                style={{ top: (+actionElementSize.height + 5) + 'px', left: menuPosition.left + 'px',  zIndex: "9999", visibility: isOpened && !positionCalculated ? 'hidden' : 'visible' }}
            >
                {children}
            </div>
        </div>
    );
}

export default ContextMenu;
