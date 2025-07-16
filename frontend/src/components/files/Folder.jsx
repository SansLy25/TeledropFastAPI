import React from "react";
import FileSystemItem from "./FileSystemItem";

function Folder({ name, view = "big", editable = true }) {
    return (
        <FileSystemItem
            name={name}
            icon="/images/folder.svg"
            alt="Folder"
            view={view}
            editable={editable}
        />
    );
}

export default Folder;
