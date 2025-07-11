import React from 'react';
import LargeContainer from '../containers/LargeContainer.jsx';

function Main({ children }) {
    return (
        <main className="h-full">
            <LargeContainer className="h-full flex flex-row p-[0.7rem] pt-[0.8rem]">
                {children}
            </LargeContainer>
        </main>
    )
}

export default Main