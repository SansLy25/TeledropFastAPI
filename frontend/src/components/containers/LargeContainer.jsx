import React from 'react';

function LargeContainer({ children, className = '' }) {
    return (
        <div className={`dark:bg-neutral-900 text-white rounded-2xl dark:border-[1.3px] dark:border-neutral-800 ${className}`}>
            {children}
        </div>
    );
}

export default LargeContainer;