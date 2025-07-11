import React from 'react';
import Header from "../components/layout/Header.jsx";
import Main from "../components/layout/Main.jsx";
import Navigation from "../components/layout/Navigation.jsx";
import Path from "../components/files/Path.jsx";


function Files() {
    return (
        <div className="flex flex-col dark:bg-neutral-950 h-screen w-screen p-2 py-2.75 gap-2.5">
            <Header/>
            <Main>
                <div>
                    <div>
                        <Path path="/дом/новая папка/документы"/>
                    </div>
                </div>
            </Main>
            <Navigation/>
        </div>
    )
}

export default Files