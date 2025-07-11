import React from 'react';
import LargeContainer from '../containers/LargeContainer.jsx';

function Main({ children }) {
    return (
        <main className="h-full">
            <LargeContainer className="h-full flex flex-row">
                {children}
            </LargeContainer>
        </main>
    )
}

export default Main