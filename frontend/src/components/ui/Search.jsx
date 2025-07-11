import React from 'react';
import { Search as SearchIcon } from 'lucide-react'

function Search({placeholder}) {
    return (
        <div className="flex flex-row h-full justify-between items-center w-full pr-2">
            <div className="flex-grow"></div>
            <div className="text-[0.9rem] text-center font-medium mr-[-0.3rem]">{placeholder}</div>
            <div className="flex-grow flex justify-end">
                <SearchIcon width={"28px"} height={"28px"}/>
            </div>
        </div>
    )
}

export default Search
