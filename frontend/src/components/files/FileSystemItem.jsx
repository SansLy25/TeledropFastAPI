import React from "react";
import { EllipsisVertical } from "lucide-react";

function FileSystemItem({ name, icon, alt, view = "big", editable = true }) {
    if (view === "big") {
        return (
            <div draggable={true} className="flex flex-col items-center justify-start p-3 cursor-pointer hover:bg-gray-100 dark:hover:bg-neutral-900 rounded-lg transition-colors">
                <div className="relative">
                    <img src={icon} alt={alt} className="w-21 h-24" />
                    <button onClick={() => alert("клик")} className="absolute right-[-1.0rem] top-3/5 -translate-y-1/2">
                        <EllipsisVertical width="20px" height="20px"/>
                    </button>
                </div>
                <div className="mt-1 text-center line-clamp-2 text-[0.65rem] font-medium max-w-[120px] sm:max-w-[150px]">
                    {name}
                </div>
            </div>
        );
    } else if (view === "list") {
        return (
            <div className="flex items-center p-3 cursor-pointer hover:bg-gray-100 dark:hover:bg-neutral-900 rounded-lg transition-colors">
                <img src={icon} alt={alt} className="w-8 h-8 mr-4" />
                <div className="text-sm font-medium truncate">
                    {name}
                </div>
            </div>
        );
    }
}

export default FileSystemItem;
