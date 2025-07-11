import React from 'react';


function Main({ children }) {
    return (
        <div className="dark:bg-neutral-900 text-white rounded-2xl dark:border dark:border-neutral-800 h-full">
            {children}
        </div>
    )
}

export default Main