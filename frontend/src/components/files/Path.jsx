import React from 'react';
import { ChevronRight } from "lucide-react"

function Path({path}) {
    let path_items = path.split("/")
    path_items = path_items.filter(item => item !== "")
    path_items.splice(0, 0, "Диск")

    return (
        <div className="relative w-full overflow-hidden">
            <div className="flex flex-row gap-1 overflow-x-auto no-scrollbar">
                {
                    path_items.map((item, index) => (
                        <div key={index} className="flex justify-center text-[0.7rem] items-center gap-0.5 dark:text-neutral-400 font-medium whitespace-nowrap">
                            <div>{item}</div>
                            <ChevronRight width={"12px"} height={"12px"} className="mt-0.5"/>
                        </div>))
                }
            </div>
            <div className="absolute right-0 top-0 h-full w-14 bg-gradient-to-r from-transparent to-neutral-900 pointer-events-none"></div>
        </div>
    )
}

export default Path
