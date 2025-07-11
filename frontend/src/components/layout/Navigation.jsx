import React from 'react';
import { Folder, Image, Blocks, Users } from 'lucide-react'
import NavigationItem from "../ui/NavigationItem.jsx";

function Navigation() {
    const NAVIGATION_ITEMS = [
        {
            "link": "/",
            "icon": Image,
            "text": "Фото"
        },
        {
            "link": "/",
            "icon": Folder,
            "text": "Файлы"
        },
        {
            "link": "/",
            "icon": Blocks,
            "text": "Каналы"
        },
        {
            "link": "/",
            "icon": Users,
            "text": "Доступ"
        }
    ]
    return (
        <div className="flex justify-center gap-10 align-middle dark:bg-neutral-900 rounded-2xl dark:border dark:border-neutral-800 h-[5.5rem]">
            {NAVIGATION_ITEMS.map((item) => (<NavigationItem {...item} />))}
        </div>
    )
}

export default Navigation
