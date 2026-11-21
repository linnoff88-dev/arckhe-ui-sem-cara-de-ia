"use client";
import { Command } from "cmdk";
import { useEffect, useState } from "react";

// As setas, o Enter e a busca vêm prontos.
export function Busca() {
  const [aberto, setAberto] = useState(false);
  useEffect(() => {
    const tecla = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") setAberto((v) => !v);
    };
    window.addEventListener("keydown", tecla);
    return () => window.removeEventListener("keydown", tecla);
  }, []);
  return (
    <Command.Dialog open={aberto} onOpenChange={setAberto} label="Buscar ações">
      <Command.Input />
      <Command.List>
        <Command.Item>Novo cadastro</Command.Item>
        <Command.Item>Sair</Command.Item>
      </Command.List>
    </Command.Dialog>
  );
}
