import React from 'react';
import Header from "../components/layout/Header.jsx";
import Main from "../components/layout/Main.jsx";
import Navigation from "../components/layout/Navigation.jsx";
import Path from "../components/files/Path.jsx";
import {ArrowLeft, Menu, ArrowDownNarrowWide, Grip} from "lucide-react";
import ContextMenu from "../components/ui/ContextMenu.jsx";
import BorderButton from "../components/ui/BorderButton.jsx";


function Files() {
    return (
        <div className="flex flex-col dark:bg-neutral-950 h-screen w-screen p-2 py-2 gap-2.5">
            <Header/>
            <Main>
                <div className="w-full">
                    <div>
                        <Path path="/море2077/"/>
                    </div>
                    <div className="flex flex-row justify-between mt-[0.6rem]">
                        <div className="flex flex-row items-center ml-[-0.25rem] gap-1">
                            <button onClick={(e) => {alert("клик")}} className="flex items-center justify-center">
                                <ArrowLeft width={"27px"} height={"27px"}/>
                            </button>
                            <div className="text-xl font-medium">
                                Новая папка
                            </div>
                            <Menu width={"25px"} height={"25px"} className="mt-0.5"/>
                        </div>
                        <div className="flex flex-row items-start gap-1.5">
                            <ContextMenu actionElement={<BorderButton><ArrowDownNarrowWide width={"22px"} height={"22px"}/><div>Сорт.</div></BorderButton>}>
                                <div></div>
                            </ContextMenu>
                            <ContextMenu actionElement={<BorderButton><Grip width={"22px"} height={"22px"}/><div>Вид</div></BorderButton>}>
                                <div></div>
                            </ContextMenu>
                        </div>
                    </div>
                </div>
            </Main>
            <Navigation/>
        </div>
    )
}

export default Files
