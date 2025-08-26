import React, { forwardRef } from 'react';

const LargeContainer = forwardRef(({ children, className = '' }, ref) => {
    return (
        <div ref={ref} className={`dark:bg-neutral-900 text-white rounded-2xl dark:border-[1.3px] dark:border-neutral-800 ${className}`}>
            {children}
        </div>
    );
});

export default LargeContainer;
