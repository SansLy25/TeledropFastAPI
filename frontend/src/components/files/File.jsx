import React from "react";
import FileSystemItem from "./FileSystemItem";

function File({ name, view = "big", editable = true }) {
    return (
        <FileSystemItem
            name={name}
            icon="/images/file.svg"
            alt="File"
            view={view}
            editable={editable}
        />
    );
}

export default File;
