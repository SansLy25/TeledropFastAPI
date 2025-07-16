import React from "react";

function FileSystemItem({ name, icon, alt, view = "big", editable = true }) {
    if (view === "big") {
        return (
            <div className="flex flex-col items-center justify-center p-3 cursor-pointer hover:bg-gray-100 dark:hover:bg-neutral-900 rounded-lg transition-colors">
                <img src={icon} alt={alt} className="w-21 h-21" />
                <div className="mt-1 text-center text-[0.65rem] font-medium truncate max-w-[120px] sm:max-w-[150px]">
                    {name}
                </div>
            </div>
        );
    } else if (view === "list") {
        return (
            <div className="flex items-center p-3 cursor-pointer hover:bg-gray-100 dark:hover:bg-neutral-900 rounded-lg transition-colors">
                <img src={icon} alt={alt} className="w-8 h-8 mr-4" />
                <div className="text-base font-medium truncate">
                    {name}
                </div>
            </div>
        );
    }
}

export default FileSystemItem;