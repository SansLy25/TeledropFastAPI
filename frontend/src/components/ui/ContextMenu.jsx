import React, { useState, useRef, useEffect } from 'react';

function ContextMenu({children, actionElement}) {
    const [isOpened, setIsOpened] = useState(false);
    const [actionElementSize, setActionElementSize] = useState({ width: 0, height: 0 });
    const actionElementRef = useRef(null);

    function onActionElementClick(event) {
        setIsOpened(!isOpened);
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
