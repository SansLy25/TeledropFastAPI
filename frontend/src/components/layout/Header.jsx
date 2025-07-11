import React from 'react';
import {Book} from "lucide-react";
import Search from "../ui/Search.jsx";
import LargeContainer from '../containers/LargeContainer.jsx';

function Header() {
    return (
        <div className="flex flex-row gap-2  h-[3.9rem]">
            <LargeContainer className="flex gap-3 items-center px-1 border w-[9.5rem] h-full">
                <img src="/images/test-profile.png" alt="" className="rounded-full w-10"/>
                <div className="text-[0.9rem] font-medium">Профиль</div>
            </LargeContainer>
            <LargeContainer className="py-2 flex-1 flex items-center justify-between px-1 dark:border h-full">
                <div className="flex-shrink-0 ml-1">
                    <Book width={"25px"} height={"25px"}/>
                </div>
                <div className="flex-grow">
                    <Search placeholder="Поиск по диску"/>
                </div>
            </LargeContainer>
        </div>
    )
}

export default Header