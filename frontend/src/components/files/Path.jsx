import React from 'react';
import { ChevronRight } from "lucide-react"

function Path({path}) {
    let path_items = path.split("/")
    path_items = path_items.filter(item => item !== "")
    path_items.splice(0, 0, "Диск")

    return (
        <div className="flex flex-row gap-1">
            {
                path_items.map((item, index) => (
                    <div key={index} className="flex justify-center text-[0.65rem] items-center gap-0.5 dark:text-neutral-400 font-medium">
                        <div>{item}</div>
                        <ChevronRight width={"12px"} height={"12px"} className="mt-0.5"/>
                    </div>))
            }
        </div>
    )
}

export default Path
