import React, { useState, useRef, useEffect, useMemo } from 'react';
import { useMenuContext } from '../../contexts/MenuContext';

function useIsMobile() {
    const [isMobile, setIsMobile] = useState(false);

    useEffect(() => {
        const checkIsMobile = () => {
            setIsMobile(window.innerWidth < 768);
        };

        checkIsMobile();

        window.addEventListener('resize', checkIsMobile);

        return () => window.removeEventListener('resize', checkIsMobile);
    }, []);

    return isMobile;
}

function ContextMenu({children, actionElement, borderElementRef}) {
    const [actionElementSize, setActionElementSize] = useState({ width: 0, height: 0 });
    const [menuPosition, setMenuPosition] = useState({ left: 0 });
    const [positionCalculated, setPositionCalculated] = useState(false);
    const [touchStartY, setTouchStartY] = useState(null);
    const [swipeOffset, setSwipeOffset] = useState(0);
    const actionElementRef = useRef(null);
    const { openMenuKey, setOpenMenuKey } = useMenuContext();
    const isMobile = useIsMobile();

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

    const calculateDesktopPosition = () => {
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
    };

    useEffect(() => {
        if (!isMobile) {
            calculateDesktopPosition();
        } else if (isOpened) {
            setPositionCalculated(true);
            setSwipeOffset(0);
        } else {
            setPositionCalculated(false);
        }
    }, [isOpened, actionElementSize, borderElementRef, isMobile]);

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

    const handleTouchStart = (e) => {
        if (isMobile) {
            setTouchStartY(e.touches[0].clientY);
            setSwipeOffset(0);
        }
    };

    const handleTouchMove = (e) => {
        if (isMobile && touchStartY !== null) {
            const touchY = e.touches[0].clientY;
            const diff = touchY - touchStartY;

            if (diff > 0) {
                setSwipeOffset(diff * 1.5);
            }
        }
    };

    const handleTouchEnd = () => {
        if (swipeOffset > 50) {
            setOpenMenuKey(null);
        }

        setTouchStartY(null);
        if (swipeOffset < 100) {
            setSwipeOffset(0);
        }
    };

    const getMenuStyle = () => {
        if (isMobile) {
            const swipeOpacity = swipeOffset > 0 
                ? Math.max(1 - (swipeOffset / 200), 0.5)
                : 1;

            return {
                position: 'fixed',
                bottom: 0,
                left: 0,
                right: 0,
                zIndex: 9999,
                visibility: isOpened && positionCalculated ? 'visible' : 'hidden',
                transform: swipeOffset > 0 ? `translateY(${swipeOffset}px)` : 'none',
                opacity: swipeOpacity,
                height: '50%',
                boxShadow: swipeOffset > 0 ? 'none' : '0 -4px 12px rgba(0, 0, 0, 0.1)'
            };
        } else {
            return {
                top: (+actionElementSize.height + 5) + 'px',
                left: menuPosition.left + 'px',
                zIndex: 9999,
                visibility: isOpened && !positionCalculated ? 'hidden' : 'visible'
            };
        }
    };

    const getMenuClassName = () => {
        const baseClasses = 'dark:bg-neutral-900 text-white dark:border-[1.3px] dark:border-neutral-800';
        const transitionClasses = swipeOffset > 0 ? 'transition-transform' : 'transition-all duration-300 ease-in-out';

        const desktopStateClasses = isOpened && positionCalculated
            ? "opacity-100 translate-y-0 scale-100" 
            : "opacity-0 translate-y-1 scale-95 pointer-events-none";

        const mobileStateClasses = isOpened && positionCalculated
            ? "opacity-100 translate-y-0" 
            : "opacity-0 translate-y-full pointer-events-none";

        if (isMobile) {
            return `${baseClasses} ${transitionClasses} ${mobileStateClasses} fixed bottom-0 left-0 right-0 w-full rounded-t-2xl overflow-auto`;
        } else {
            return `${baseClasses} ${transitionClasses} ${desktopStateClasses} absolute w-60 h-96 rounded-2xl`;
        }
    };

    return (
        <div className="relative">
            {enhancedActionElement}
            <div
                ref={menuRef}
                className={getMenuClassName()}
                style={getMenuStyle()}
                onTouchStart={handleTouchStart}
                onTouchMove={handleTouchMove}
                onTouchEnd={handleTouchEnd}
            >
                {isMobile && (
                    <div className="w-12 h-1 bg-gray-300 rounded-full mx-auto mt-2 mb-4" />
                )}
                {children}
            </div>
        </div>
    );
}

export default ContextMenu;
