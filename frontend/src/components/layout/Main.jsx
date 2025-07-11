import React from 'react';
import LargeContainer from '../components/components/LargeContainer.jsx';

function Main({ children }) {
    return (
        <LargeContainer className="h-full">
            {children}
        </LargeContainer>
    )
}

export default Main