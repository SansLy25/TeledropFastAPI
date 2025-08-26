import React, { forwardRef } from 'react';
import LargeContainer from '../containers/LargeContainer.jsx';

const Main = forwardRef(({ children, ...props }, ref) => {
    return (
        <main className="h-full">
            <LargeContainer ref={ref} {...props} className="h-full flex flex-col py-4 px-3">
                {children}
            </LargeContainer>
        </main>
    )
});

export default Main;
