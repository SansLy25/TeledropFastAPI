import React from 'react';

function NavigationItem({link = "/", icon: Icon, text}) {
    return (
        <div className="flex items-center text-sm font-normal justify-center flex-col align-middle dark:text-white">
            {<Icon size={"25px"}/>}
            {text}
        </div>
    )
}

export default NavigationItem;
