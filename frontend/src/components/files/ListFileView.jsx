import React from "react";
import File from "./File";
import Folder from "./Folder";

function ListFileView({files = [], folders = [], edit = true, view = "big"}) {
    return (
        <div className={view === "big" 
            ? "w-full ml-[-0.15rem] overflow-x-hidden grid grid-cols-3 h-[calc(100vh-17rem)] no-scrollbar overflow-y-auto sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 xl:grid-cols-7 gap-4 mt-2.5"
            : "w-full flex flex-col gap-2 mt-2 h-[calc(100vh-12rem)] overflow-y-auto"
        }>
            {folders.map((folder, index) => (
                <Folder 
                    key={`folder-${index}`} 
                    name={folder.name} 
                    view={view} 
                    editable={edit} 
                />
            ))}

            {files.map((file, index) => (
                <File 
                    key={`file-${index}`} 
                    name={file.name} 
                    view={view} 
                    editable={edit} 
                />
            ))}
        </div>
    );
}

export default ListFileView;
