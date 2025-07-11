import React from 'react';
import {Book} from "lucide-react";
import Search from "../ui/Search.jsx";

function Header() {
    return (
        <div className="flex flex-row gap-2  h-[3.9rem]">
            <div className="flex gap-3 items-center dark:bg-neutral-900 rounded-2xl px-1 border dark:border-neutral-800 w-[9.5rem] h-full">
                <img src="/images/test-profile.png" alt="" className="rounded-full w-10"/>
                <div className="text-[0.9rem] font-medium">Профиль</div>
            </div>
            <div className="py-2 flex-1 flex items-center justify-between dark:bg-neutral-900 rounded-2xl dark:border px-1 dark:border-neutral-800 h-full">
                <div className="flex-shrink-0 ml-1">
                    <Book width={"25px"} height={"25px"}/>
                </div>
                <div className="flex-grow">
                    <Search placeholder="Поиск по диску"/>
                </div>
            </div>
        </div>
    )
}

export default Header
