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
                    <div key={index} className="flex justify-center items-center gap-1">
                        <div>{item}</div>
                        <ChevronRight width={"15px"} height={"15px"}/>
                    </div>))
            }
        </div>
    )
}

export default Path
