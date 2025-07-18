import React from 'react';
import Header from "../components/layout/Header.jsx";
import Main from "../components/layout/Main.jsx";
import Navigation from "../components/layout/Navigation.jsx";
import Path from "../components/files/Path.jsx";
import {ArrowLeft, Menu, ArrowDownNarrowWide, Grip} from "lucide-react";
import ContextMenu from "../components/ui/ContextMenu.jsx";
import BorderButton from "../components/ui/BorderButton.jsx";
import ListFileView from "../components/files/ListFileView.jsx";

function Files() {
    return (
        <div className="flex flex-col dark:bg-neutral-950 h-screen w-screen p-2 py-2 gap-2.5">
            <Header/>
            <Main>
                <div className="w-full flex flex-col">
                    <div>
                        <Path path="/море2077/"/>
                    </div>
                    <div className="flex flex-row justify-between mt-[0.5rem]">
                        <div className="flex flex-row items-center gap-2">
                            <button onClick={(e) => {alert("клик")}} className="flex items-center justify-center ml-[-0.2rem]">
                                <ArrowLeft width={"26px"} height={"26px"}/>
                            </button>
                            <div className="text-xl font-medium">
                                Новая папка
                            </div>
                            <Menu width={"25px"} height={"25px"} className="mt-0.5"/>
                        </div>
                        <div className="flex flex-row items-start gap-2">
                            <ContextMenu actionElement={<BorderButton><ArrowDownNarrowWide width={"20px"} height={"20px"}/><div>Сорт.</div></BorderButton>}>
                                <div></div>
                            </ContextMenu>
                            <ContextMenu actionElement={<BorderButton><Grip width={"20px"} height={"20px"}/><div>Вид</div></BorderButton>}>
                                <div></div>
                            </ContextMenu>
                        </div>
                    </div>
                    <ListFileView
                        files={[{name: "Видео.mov"}, {name: "Изображение.png"}, {name: "текст.txt"}]}
                        folders={[{name: "Море"}, {name: "Моя любимая папка"}, {name: "Папка с большим названием c еще большим названием"}]}
                        view="big"
                    />
                </div>
            </Main>
            <Navigation/>
        </div>
    )
}

export default Files
