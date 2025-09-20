import React from 'react';
import { Folder, Image, Blocks, Users } from 'lucide-react'
import NavigationItem from "../ui/NavigationItem.jsx";
import LargeContainer from '../containers/LargeContainer.jsx';

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
        <LargeContainer className="flex justify-center gap-10 align-middle h-[5.5rem]">
            {NAVIGATION_ITEMS.map((item, i) => (<NavigationItem key={i} {...item} />))}
        </LargeContainer>
    )
}

export default Navigation