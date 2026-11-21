"use client";
import { useState } from "react";
import { Meteors, Marquee, BorderBeam } from "../components/efeitos";
import { MenuDrawer } from "../components/menu-drawer";
import { CommandMenu } from "../components/command-menu";

export default function Cadastro() {
  const [toasts, setToasts] = useState<string[]>([]);

  function salvar() {
    setToasts((lista) => [...lista, "Cadastro salvo"]);
    setTimeout(() => setToasts([]), 800);
  }

  return (
    <main>
      <Meteors />
      <Marquee>Oficina gratuita</Marquee>
      <h1>Cadastro</h1>
      <BorderBeam />
      <input placeholder="Nome" />
      <input placeholder="E-mail" />
      <div className="botao" onClick={salvar}>Salvar</div>
      {toasts.map((t, i) => (
        <p key={i} className="toast fixed bottom-4 right-4">{t}</p>
      ))}
      <MenuDrawer />
      <CommandMenu />
    </main>
  );
}
