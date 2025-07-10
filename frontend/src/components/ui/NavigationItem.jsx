import React from 'react';

function NavigationItem({link = "/", icon, text}) {
    return (
        <div className="flex flex-row justify-center dark:text-white">
            {text}
        </div>
    )
}

export default NavigationItem;
